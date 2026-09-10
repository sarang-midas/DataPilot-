from __future__ import annotations
import re
import pandas as pd


def human_bytes(n:int) -> str:
    x=float(n)
    for unit in ("B","KB","MB","GB"):
        if x<1024 or unit=="GB": return f"{x:.1f} {unit}"
        x/=1024


def safe_name(s:str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+","-",s).strip("-") or "export"


def date_columns(df:pd.DataFrame):
    return [c for c in df.columns if pd.api.types.is_datetime64_any_dtype(df[c])]
