from __future__ import annotations
from typing import Any
import difflib
import numpy as np
import pandas as pd


def _outlier_count(s: pd.Series) -> int:
    x = pd.to_numeric(s, errors="coerce").dropna()
    if len(x) < 8:
        return 0
    q1, q3 = x.quantile([0.25, 0.75])
    iqr = q3 - q1
    if iqr == 0:
        return 0
    return int(((x < q1 - 1.5 * iqr) | (x > q3 + 1.5 * iqr)).sum())


def _category_inconsistency(s: pd.Series) -> int:
    vals = s.dropna().astype(str).str.strip()
    if vals.empty:
        return 0
    unique = list(pd.unique(vals))
    lower_map = {}
    count = 0
    for v in unique:
        key = v.lower()
        lower_map.setdefault(key, []).append(v)
    for variants in lower_map.values():
        if len(variants) > 1:
            count += len(variants) - 1
    return count


def quality_report(df: pd.DataFrame, profile: dict[str, dict[str, Any]]) -> dict[str, Any]:
    rows, cols = df.shape
    cells = max(1, rows * max(1, cols))
    missing = int(df.isna().sum().sum())
    duplicates = int(df.duplicated().sum())
    invalid = 0
    outliers = 0
    inconsistencies = 0
    duplicate_ids = 0
    by_column = {}
    for col, meta in profile.items():
        s = df[col]
        numeric_bad = 0
        if meta["type"] in {"Numeric","Currency","Percentage"}:
            converted = pd.to_numeric(s.astype(str).str.replace(",", "", regex=False).str.replace(r"[$₹€£]", "", regex=True), errors="coerce")
            numeric_bad = int(((s.notna()) & converted.isna()).sum())
            name_low = str(col).lower()
            if meta["type"] == "Percentage":
                invalid_pct = int(((converted.notna()) & ((converted < 0) | (converted > 100))).sum())
                numeric_bad += invalid_pct
            # Semantic validity checks for common business fields.
            if any(k in name_low for k in ("age", "years_old")):
                numeric_bad += int(((converted.notna()) & ((converted < 0) | (converted > 120))).sum())
            if any(k in name_low for k in ("price","revenue","sales","amount","cost","profit","salary","wage","spend","expense","budget")):
                numeric_bad += int(((converted.notna()) & (converted < 0)).sum())
            outliers += _outlier_count(converted)
        date_bad = 0
        if meta["type"] == "Date":
            parsed = pd.to_datetime(s, errors="coerce", dayfirst=True, format="mixed")
            date_bad = int(((s.notna()) & parsed.isna()).sum())
        inconsistent = _category_inconsistency(s) if meta["type"] in {"Categorical","Geographic","Text"} else 0
        invalid += numeric_bad + date_bad
        inconsistencies += inconsistent
        if meta["type"] == "ID":
            dup_id = int(s.notna().sum() - s.dropna().nunique())
            duplicate_ids += max(0, dup_id)
        by_column[col] = {"missing": int(s.isna().sum()), "invalid": numeric_bad + date_bad, "unique": int(s.nunique(dropna=True)), "outliers": _outlier_count(s) if meta["type"] in {"Numeric","Currency","Percentage"} else 0, "inconsistent_variants": inconsistent, "duplicate_id_values": int(dup_id) if meta["type"] == "ID" else 0}
    completeness = max(0.0, 1 - missing / cells)
    validity = max(0.0, 1 - invalid / cells)
    duplicates = max(duplicates, duplicate_ids)
    uniqueness = 1.0 if rows == 0 else max(0.0, 1 - duplicates / rows)
    consistency = 1.0 if cols == 0 else max(0.0, 1 - inconsistencies / max(1, sum(v["unique"] for v in by_column.values())))
    numeric_cells = max(1, sum(1 for m in profile.values() if m["type"] in {"Numeric","Currency","Percentage"}) * max(1, rows))
    outlier_quality = max(0.0, 1 - outliers / numeric_cells)
    raw_score = (completeness * .30 + uniqueness * .20 + validity * .20 + consistency * .15 + outlier_quality * .15) * 100
    score = int(np.floor(raw_score)) if raw_score < 100 else 100
    return {
        "rows": rows,
        "columns": cols,
        "missing": missing,
        "duplicates": duplicates,
        "duplicate_ids": duplicate_ids,
        "invalid": invalid,
        "outliers": outliers,
        "inconsistencies": inconsistencies,
        "score": int(score),
        "completeness": round(completeness * 100, 1),
        "validity": round(validity * 100, 1),
        "uniqueness": round(uniqueness * 100, 1),
        "consistency": round(consistency * 100, 1),
        "outlier_quality": round(outlier_quality * 100, 1),
        "by_column": by_column,
    }
