from __future__ import annotations

import re

import pandas as pd

from core.column_detector import detect_columns
from core.kpi_engine import find_col


def _mentioned_column(question: str, columns: list[str]) -> str | None:
    q = re.sub(r"[^a-z0-9]+", " ", question.lower()).strip()
    tokens = set(q.split())
    exact = sorted(columns, key=lambda c: len(str(c)), reverse=True)
    for col in exact:
        normalized = re.sub(r"[^a-z0-9]+", " ", str(col).lower()).strip()
        if normalized and normalized in q:
            return col
        if normalized and set(normalized.split()).issubset(tokens):
            return col
    return None


def answer_question(df: pd.DataFrame, question: str) -> str:
    q = question.lower().strip()
    if not q:
        return "Type a question about the current dataset."
    if df.empty:
        return "The current filtered dataset has no rows. Clear the dashboard filters and try again."

    profile = detect_columns(df)
    numeric = [c for c, m in profile.items() if m["type"] in {"Numeric", "Currency", "Percentage"}]
    date_cols = [c for c, m in profile.items() if m["type"] == "Date"]
    dimensions = [c for c, m in profile.items() if m["type"] in {"Categorical", "Geographic", "Boolean", "Text"}]

    if any(k in q for k in ["how many rows", "number of rows", "record count", "row count"]):
        return f"The current filtered dataset contains {len(df):,} rows."

    metric = _mentioned_column(q, numeric) or find_col(df, ["sales", "revenue", "amount", "profit", "cost", "price", "value"])
    dimension = _mentioned_column(q, dimensions)

    if any(k in q for k in ["highest", "maximum", "max", "top", "best"]):
        if metric and dimension:
            values = pd.to_numeric(df[metric], errors="coerce")
            grouped = df.assign(_metric=values).groupby(dimension, dropna=False)["_metric"].sum().sort_values(ascending=False)
            if not grouped.empty:
                return f"{grouped.index[0]} has the highest {metric} at {grouped.iloc[0]:,.2f}."
        if metric:
            value = pd.to_numeric(df[metric], errors="coerce").max()
            return f"The maximum {metric} is {value:,.2f}."

    if any(k in q for k in ["lowest", "minimum", "min", "worst"]):
        if metric and dimension:
            values = pd.to_numeric(df[metric], errors="coerce")
            grouped = df.assign(_metric=values).groupby(dimension, dropna=False)["_metric"].sum().sort_values()
            if not grouped.empty:
                return f"{grouped.index[0]} has the lowest {metric} at {grouped.iloc[0]:,.2f}."
        if metric:
            value = pd.to_numeric(df[metric], errors="coerce").min()
            return f"The minimum {metric} is {value:,.2f}."

    if any(k in q for k in ["average", "mean", "avg"]):
        if metric:
            value = pd.to_numeric(df[metric], errors="coerce").mean()
            return f"Average {metric} is {value:,.2f}."
        return "I found numeric fields, but could not identify which one you want to average."

    if any(k in q for k in ["total", "sum"]):
        if metric:
            value = pd.to_numeric(df[metric], errors="coerce").sum()
            return f"Total {metric} is {value:,.2f}."

    if "correlation" in q and len(numeric) >= 2:
        corr = df[numeric].apply(pd.to_numeric, errors="coerce").corr()
        pairs = []
        for i, a in enumerate(numeric):
            for b in numeric[i + 1:]:
                value = corr.loc[a, b]
                if pd.notna(value):
                    pairs.append((abs(value), a, b, value))
        if pairs:
            _, a, b, value = max(pairs)
            return f"The strongest correlation is between {a} and {b}: {value:.2f}. Correlation does not prove causation."

    if date_cols and numeric and any(k in q for k in ["monthly", "month", "trend"]):
        d = _mentioned_column(q, date_cols) or date_cols[0]
        n = metric or numeric[0]
        tmp = df[[d, n]].copy()
        tmp[d] = pd.to_datetime(tmp[d], errors="coerce")
        tmp[n] = pd.to_numeric(tmp[n], errors="coerce")
        tmp = tmp.dropna()
        monthly = tmp.groupby(pd.Grouper(key=d, freq="ME"))[n].sum().tail(6)
        if not monthly.empty:
            return "Monthly trend (last 6 periods): " + "; ".join(f"{idx:%b %Y}: {value:,.0f}" for idx, value in monthly.items())

    return "I can safely answer row counts, totals, averages, highest/lowest values, correlations, and simple monthly trends. Try: 'What is total sales?', 'Which product has the highest sales?', or 'average price'."
