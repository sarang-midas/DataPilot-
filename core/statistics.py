from __future__ import annotations
import pandas as pd
import numpy as np
from scipy.stats import skew, kurtosis


def numeric_summary(df: pd.DataFrame, profile: dict) -> pd.DataFrame:
    rows=[]
    for col, meta in profile.items():
        if meta["type"] not in {"Numeric","Currency","Percentage"}: continue
        s=pd.to_numeric(df[col], errors="coerce").dropna()
        if s.empty: continue
        rows.append({
            "Column": col, "Count": int(s.size), "Mean": s.mean(), "Median": s.median(), "Mode": s.mode().iloc[0] if not s.mode().empty else np.nan,
            "Std Dev": s.std(), "Variance": s.var(), "Min": s.min(), "Q1": s.quantile(.25), "Q3": s.quantile(.75), "Max": s.max(),
            "Skewness": skew(s) if len(s)>2 else np.nan, "Kurtosis": kurtosis(s) if len(s)>3 else np.nan,
        })
    return pd.DataFrame(rows)


def correlation_matrix(df: pd.DataFrame, profile: dict) -> pd.DataFrame:
    cols=[c for c,m in profile.items() if m["type"] in {"Numeric","Currency","Percentage"}]
    return df[cols].apply(pd.to_numeric, errors="coerce").corr() if cols else pd.DataFrame()
