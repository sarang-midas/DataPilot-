from __future__ import annotations

import io
from pathlib import Path
from typing import Dict

import pandas as pd

from config.settings import ALLOWED_EXTENSIONS, APP_CONFIG


def _clean_headers(df: pd.DataFrame) -> pd.DataFrame:
    frame = df.copy()
    seen: dict[str, int] = {}
    new: list[str] = []
    for col in frame.columns:
        base = str(col).strip() or "Unnamed"
        count = seen.get(base, 0) + 1
        seen[base] = count
        new.append(base if count == 1 else f"{base}_{count}")
    frame.columns = new
    return frame


def _validate_table(df: pd.DataFrame, source: str) -> pd.DataFrame:
    df = _clean_headers(df)
    if df.shape[1] == 0:
        raise ValueError(f"{source} does not contain any columns.")
    if df.empty:
        raise ValueError(f"{source} contains no data rows.")
    # Drop columns that pandas created for completely empty trailing content.
    df = df.dropna(axis=1, how="all")
    if df.shape[1] == 0:
        raise ValueError(f"{source} contains only empty columns.")
    return df


def read_csv_bytes(payload: bytes) -> pd.DataFrame:
    last_exc: Exception | None = None
    for encoding in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
        try:
            df = pd.read_csv(
                io.BytesIO(payload),
                sep=None,
                engine="python",
                encoding=encoding,
                on_bad_lines="warn",
            )
            return _validate_table(df, "CSV file")
        except Exception as exc:
            last_exc = exc
    raise ValueError(f"CSV could not be parsed: {last_exc}")


def read_excel_bytes(payload: bytes) -> dict[str, pd.DataFrame]:
    try:
        book = pd.ExcelFile(io.BytesIO(payload))
    except Exception as exc:
        raise ValueError(f"Excel workbook could not be opened: {exc}") from exc

    result: dict[str, pd.DataFrame] = {}
    for sheet in book.sheet_names:
        try:
            frame = pd.read_excel(book, sheet_name=sheet)
            if frame.empty or frame.shape[1] == 0:
                continue
            result[str(sheet)] = _validate_table(frame, f"Excel sheet '{sheet}'")
        except Exception as exc:
            raise ValueError(f"Excel sheet '{sheet}' could not be read: {exc}") from exc
    if not result:
        raise ValueError("The workbook contains no non-empty sheets.")
    return result


def load_uploaded_bytes(filename: str, payload: bytes) -> Dict[str, pd.DataFrame]:
    safe_name = Path(filename).name
    ext = Path(safe_name).suffix.lower().lstrip(".")
    if ext not in ALLOWED_EXTENSIONS:
        allowed = ", ".join(sorted(ALLOWED_EXTENSIONS))
        raise ValueError(f"Unsupported file type '.{ext}'. Allowed: {allowed}")
    if not payload:
        raise ValueError("The uploaded file is empty.")
    size_mb = len(payload) / (1024 * 1024)
    if size_mb > APP_CONFIG["max_upload_mb"]:
        raise ValueError(f"File is {size_mb:.1f} MB. Maximum configured size is {APP_CONFIG['max_upload_mb']} MB.")

    if ext == "csv":
        return {Path(safe_name).stem or "dataset": read_csv_bytes(payload)}

    sheets = read_excel_bytes(payload)
    stem = Path(safe_name).stem or "workbook"
    return {f"{stem} · {sheet}": df for sheet, df in sheets.items()}
