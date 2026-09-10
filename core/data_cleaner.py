from __future__ import annotations

from dataclasses import dataclass, fields

import numpy as np
import pandas as pd

from core.column_detector import detect_columns
from core.data_quality import quality_report


@dataclass
class CleaningConfig:
    trim_whitespace: bool = True
    normalize_case: str = "Keep"
    normalize_numeric: bool = True
    parse_dates: bool = True
    fill_missing: bool = True
    missing_numeric: str = "Median"
    missing_text: str = "Mode"
    missing_constant: str = "Unknown"
    duplicate_action: str = "Remove"
    outlier_method: str = "Keep"
    outlier_factor: float = 1.5
    negative_action: str = "Flag"
    drop_empty_columns: bool = True


def _clean_numeric(series: pd.Series) -> pd.Series:
    text = series.astype("string").str.strip()
    text = text.str.replace(",", "", regex=False).str.replace(r"[$₹€£]", "", regex=True).str.replace("%", "", regex=False)
    return pd.to_numeric(text, errors="coerce")


def _unique_headers(columns) -> list[str]:
    seen: dict[str, int] = {}
    output: list[str] = []
    for col in columns:
        base = str(col).strip() or "Unnamed"
        count = seen.get(base, 0) + 1
        seen[base] = count
        output.append(base if count == 1 else f"{base}_{count}")
    return output


def _fill_series(s: pd.Series, strategy: str, constant: str, numeric: bool = False) -> pd.Series:
    if strategy == "Mean":
        return s.fillna(s.mean())
    if strategy == "Median":
        return s.fillna(s.median())
    if strategy == "Forward fill":
        return s.ffill().bfill()
    if strategy == "Backward fill":
        return s.bfill().ffill()
    if strategy == "Constant":
        value = constant
        if numeric:
            parsed = pd.to_numeric(pd.Series([constant]), errors="coerce").iloc[0]
            value = parsed if pd.notna(parsed) else 0
        return s.fillna(value)
    if strategy == "Drop rows":
        return s
    mode = s.mode(dropna=True)
    return s.fillna(mode.iloc[0] if not mode.empty else (0 if numeric else constant))


def _iqr_bounds(s: pd.Series, factor: float) -> tuple[float, float] | None:
    x = pd.to_numeric(s, errors="coerce").dropna()
    if len(x) < 4:
        return None
    q1, q3 = x.quantile([0.25, 0.75])
    iqr = q3 - q1
    if pd.isna(iqr) or iqr <= 0:
        return None
    return float(q1 - factor * iqr), float(q3 + factor * iqr)


def clean_dataframe(df: pd.DataFrame, config: CleaningConfig) -> tuple[pd.DataFrame, list[str], dict, dict]:
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Expected a pandas DataFrame.")
    frame = df.copy()
    frame.columns = _unique_headers(frame.columns)
    log: list[str] = []
    before_quality = quality_report(frame, detect_columns(frame))

    if frame.empty:
        return frame, ["Dataset is empty; no cleaning was applied."], before_quality, before_quality

    blank_before = int(frame.map(lambda x: isinstance(x, str) and not x.strip()).sum().sum())
    frame = frame.replace(r"^\s*$", np.nan, regex=True)
    if blank_before:
        log.append(f"Converted {blank_before:,} blank/whitespace cell(s) to missing values.")

    if config.trim_whitespace:
        old_cols = list(frame.columns)
        frame.columns = _unique_headers(frame.columns)
        changed = sum(str(a).strip() != str(b) for a, b in zip(old_cols, frame.columns))
        for col in frame.select_dtypes(include=["object", "string"]).columns:
            old = frame[col].astype("string")
            new = old.str.strip()
            changed += int((old.fillna("<NA>") != new.fillna("<NA>")).sum())
            frame[col] = new
        if changed:
            log.append(f"Trimmed {changed:,} header/value item(s).")

    profile = detect_columns(frame)
    if config.normalize_numeric:
        for col, meta in profile.items():
            if meta["type"] in {"Numeric", "Currency", "Percentage"}:
                converted = _clean_numeric(frame[col])
                if converted.notna().mean() >= 0.70:
                    frame[col] = converted

    if config.parse_dates:
        for col, meta in profile.items():
            if col not in frame.columns or meta["type"] != "Date":
                continue
            original_non_null = int(frame[col].notna().sum())
            parsed = pd.to_datetime(frame[col], errors="coerce", dayfirst=True, format="mixed")
            if original_non_null and parsed.notna().sum() >= original_non_null * 0.65:
                frame[col] = parsed

    if config.normalize_case in {"lower", "UPPER", "Title"}:
        for col in frame.select_dtypes(include=["object", "string"]).columns:
            if config.normalize_case == "lower":
                frame[col] = frame[col].str.lower()
            elif config.normalize_case == "UPPER":
                frame[col] = frame[col].str.upper()
            else:
                frame[col] = frame[col].str.title()
        log.append(f"Normalized text case using {config.normalize_case}.")

    if config.drop_empty_columns:
        empty_cols = [c for c in frame.columns if frame[c].isna().all()]
        if empty_cols:
            frame = frame.drop(columns=empty_cols)
            log.append(f"Dropped {len(empty_cols):,} fully empty column(s).")

    if config.fill_missing and not frame.empty:
        profile = detect_columns(frame)
        missing_cells = int(frame.isna().sum().sum())
        for col, meta in profile.items():
            if not frame[col].isna().any():
                continue
            if meta["type"] in {"Numeric", "Currency", "Percentage"}:
                frame[col] = _fill_series(frame[col], config.missing_numeric, config.missing_constant, numeric=True)
            elif meta["type"] == "Date":
                frame[col] = _fill_series(frame[col], "Mode" if config.missing_text == "Mode" else "Constant", config.missing_constant)
            else:
                frame[col] = _fill_series(frame[col], config.missing_text, config.missing_constant)
        if config.missing_numeric == "Drop rows" or config.missing_text == "Drop rows":
            before = len(frame)
            frame = frame.dropna(axis=0, how="any")
            if before != len(frame):
                log.append(f"Dropped {before - len(frame):,} row(s) containing unresolved missing values.")
        if missing_cells:
            log.append(f"Handled {missing_cells:,} missing cell(s) using the selected strategies.")

    if config.duplicate_action == "Remove":
        before = len(frame)
        frame = frame.drop_duplicates().reset_index(drop=True)
        if before != len(frame):
            log.append(f"Removed {before - len(frame):,} fully duplicated row(s).")

    if config.negative_action == "Convert to absolute":
        converted = 0
        for col, meta in detect_columns(frame).items():
            if meta["type"] in {"Numeric", "Currency", "Percentage"}:
                numeric = pd.to_numeric(frame[col], errors="coerce")
                mask = numeric < 0
                converted += int(mask.sum())
                frame.loc[mask, col] = numeric.loc[mask].abs()
        if converted:
            log.append(f"Converted {converted:,} negative numeric value(s) to absolute values.")

    if config.outlier_method in {"Remove", "Cap/Winsorize"} and not frame.empty:
        profile = detect_columns(frame)
        numeric_cols = [c for c, m in profile.items() if m["type"] in {"Numeric", "Currency", "Percentage"}]
        if config.outlier_method == "Remove":
            keep = pd.Series(True, index=frame.index)
            for col in numeric_cols:
                bounds = _iqr_bounds(frame[col], config.outlier_factor)
                if bounds:
                    lo, hi = bounds
                    s = pd.to_numeric(frame[col], errors="coerce")
                    keep &= s.between(lo, hi) | s.isna()
            removed = int((~keep).sum())
            frame = frame.loc[keep].reset_index(drop=True)
            if removed:
                log.append(f"Removed {removed:,} row(s) with IQR outliers.")
        else:
            capped = 0
            for col in numeric_cols:
                bounds = _iqr_bounds(frame[col], config.outlier_factor)
                if not bounds:
                    continue
                lo, hi = bounds
                s = pd.to_numeric(frame[col], errors="coerce")
                clipped = s.clip(lo, hi)
                capped += int((clipped != s).fillna(False).sum())
                frame[col] = clipped
            if capped:
                log.append(f"Winsorized {capped:,} outlier value(s) using IQR bounds.")

    frame = frame.reset_index(drop=True)
    after_quality = quality_report(frame, detect_columns(frame))
    if not log:
        log.append("No cleaning changes were required.")
    return frame, log, before_quality, after_quality


def config_from_dict(data: dict) -> CleaningConfig:
    allowed = {f.name for f in fields(CleaningConfig)}
    values = {k: v for k, v in data.items() if k in allowed}
    return CleaningConfig(**values)
