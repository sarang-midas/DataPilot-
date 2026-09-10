from __future__ import annotations

import re
from typing import Any

import pandas as pd

CURRENCY_WORDS = ("revenue", "sales", "amount", "price", "cost", "profit", "income", "salary", "budget", "spend", "expense", "value", "fee")
PERCENT_WORDS = ("percent", "percentage", "pct", "margin", "rate", "ratio")
ID_WORDS = ("id", "code", "key", "uuid", "identifier")
GEO_WORDS = ("country", "state", "city", "region", "province", "postal", "zip", "latitude", "longitude", "lat", "lon", "location")
DATE_WORDS = ("date", "time", "timestamp", "created", "updated", "month", "year")
BOOL_WORDS = ("is_", "has_", "active", "enabled", "flag", "boolean")


def _name_has(name: str, words: tuple[str, ...]) -> bool:
    normalized = re.sub(r"[^a-z0-9]+", " ", name.lower()).strip()
    return any(re.search(rf"\b{re.escape(w)}\b", normalized) for w in words) or any(w in normalized for w in words if len(w) > 4)


def _numeric_values(s: pd.Series) -> pd.Series:
    return pd.to_numeric(
        s.astype("string").str.strip().str.replace(",", "", regex=False).str.replace(r"[$₹€£]", "", regex=True).str.replace("%", "", regex=False),
        errors="coerce",
    )


def _date_ratio(s: pd.Series) -> float:
    if pd.api.types.is_datetime64_any_dtype(s):
        return 1.0
    sample = s.dropna().astype("string").str.strip().head(300)
    if sample.empty or not float(sample.str.contains(r"[-/:]", regex=True).mean()) >= 0.5:
        return 0.0
    parsed = pd.to_datetime(sample, errors="coerce", dayfirst=True, format="mixed")
    return float(parsed.notna().mean())


def detect_type(name: str, s: pd.Series) -> str:
    clean = s.dropna()
    if clean.empty:
        return "Text"
    if _name_has(name, GEO_WORDS) and not pd.api.types.is_numeric_dtype(s):
        return "Geographic"
    if _name_has(name, ID_WORDS) and s.nunique(dropna=True) >= max(3, int(len(clean) * 0.7)):
        return "ID"
    if _name_has(name, DATE_WORDS) and _date_ratio(s) >= 0.65:
        return "Date"

    bool_ratio = clean.astype("string").str.lower().isin(["true", "false", "yes", "no", "y", "n", "0", "1"]).mean()
    if pd.api.types.is_bool_dtype(s) or (bool_ratio >= 0.98 and s.nunique(dropna=True) <= 2 and _name_has(name, BOOL_WORDS)):
        return "Boolean"

    numeric = _numeric_values(clean)
    numeric_ratio = float(numeric.notna().mean())
    if pd.api.types.is_numeric_dtype(s) or numeric_ratio >= 0.85:
        if _name_has(name, PERCENT_WORDS):
            return "Percentage"
        if _name_has(name, CURRENCY_WORDS):
            return "Currency"
        return "Numeric"
    if _name_has(name, PERCENT_WORDS):
        return "Percentage"
    if s.nunique(dropna=True) <= min(30, max(2, int(len(clean) * 0.1))):
        return "Categorical"
    return "Text"


def detect_columns(df: pd.DataFrame) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for col in df.columns:
        name = str(col)
        ctype = detect_type(name, df[col])
        result[name] = {
            "type": ctype,
            "unique": int(df[col].nunique(dropna=True)),
            "missing": int(df[col].isna().sum()),
            "potential_metric": ctype in {"Numeric", "Currency", "Percentage"},
            "potential_dimension": ctype in {"Categorical", "Geographic", "Date", "Boolean", "Text"},
        }
    return result


def type_columns(profile: dict[str, dict[str, Any]], types: set[str]) -> list[str]:
    return [c for c, meta in profile.items() if meta["type"] in types]
