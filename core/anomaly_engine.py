from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest


def detect_anomalies(df: pd.DataFrame, profile: dict, method: str = "IQR", contamination: float = 0.05) -> pd.DataFrame:
    numeric_cols = [c for c, m in profile.items() if m["type"] in {"Numeric", "Currency", "Percentage"}]
    columns = ["row_index", "metric", "value", "score", "direction"]
    if not numeric_cols or df.empty:
        return pd.DataFrame(columns=columns)

    frame = df.reset_index(drop=False).rename(columns={"index": "_original_index"})
    rows: list[dict] = []
    if method == "Isolation Forest":
        base = frame[numeric_cols].apply(pd.to_numeric, errors="coerce")
        base = base.fillna(base.median()).fillna(0)
        model = IsolationForest(random_state=42, contamination=min(max(contamination, 0.01), 0.49), n_estimators=120, n_jobs=-1)
        labels = model.fit_predict(base)
        scores = model.decision_function(base)
        for pos, (label, score) in enumerate(zip(labels, scores)):
            if label == -1:
                vals = base.iloc[pos]
                metric = str(vals.abs().sort_values(ascending=False).index[0])
                rows.append({"row_index": int(frame.iloc[pos]["_original_index"]), "metric": metric, "value": float(vals[metric]), "score": float(abs(score)), "direction": "multivariate"})
    else:
        for col in numeric_cols:
            s = pd.to_numeric(frame[col], errors="coerce")
            if method == "Z-score":
                sd = s.std()
                z = (s - s.mean()) / sd if sd and not np.isnan(sd) else pd.Series(0.0, index=s.index)
                mask = z.abs() > 3
                scores = z.abs()
                direction = np.where(z >= 0, "high", "low")
            else:
                q1, q3 = s.quantile([0.25, 0.75])
                iqr = q3 - q1
                if pd.isna(iqr) or iqr == 0:
                    continue
                lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
                mask = (s < lo) | (s > hi)
                scores = (s - q1).abs() / iqr
                direction = np.where(s > hi, "high", "low")
            for pos in frame.index[mask.fillna(False)]:
                rows.append({"row_index": int(frame.loc[pos, "_original_index"]), "metric": col, "value": float(s.loc[pos]), "score": float(scores.loc[pos]), "direction": str(direction[pos])})
    return pd.DataFrame(rows, columns=columns)


def forecast_linear(df: pd.DataFrame, date_col: str, metric_col: str, periods: int = 6) -> pd.DataFrame:
    if periods < 1 or date_col not in df.columns or metric_col not in df.columns:
        return pd.DataFrame()
    x = pd.DataFrame({"date": pd.to_datetime(df[date_col], errors="coerce"), "value": pd.to_numeric(df[metric_col], errors="coerce")}).dropna().sort_values("date")
    if len(x) < 8:
        return pd.DataFrame()
    grouped = x.groupby("date", as_index=False)["value"].sum()
    if len(grouped) < 4:
        return pd.DataFrame()
    grouped["t"] = np.arange(len(grouped), dtype=float)
    slope, intercept = np.polyfit(grouped["t"], grouped["value"], 1)
    future_t = np.arange(len(grouped), len(grouped) + periods, dtype=float)
    delta = grouped["date"].diff().dropna().median()
    if pd.isna(delta) or delta <= pd.Timedelta(0):
        delta = pd.Timedelta(days=1)
    dates = [grouped["date"].iloc[-1] + delta * (i + 1) for i in range(periods)]
    pred = np.polyval([slope, intercept], future_t)
    return pd.DataFrame({"date": dates, "forecast": pred})
