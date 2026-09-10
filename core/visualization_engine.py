from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

PALETTE = ["#7c5cff", "#22d3ee", "#34d399", "#f59e0b", "#fb7185", "#60a5fa", "#a78bfa", "#2dd4bf"]


def _numeric(profile):
    return [c for c, m in profile.items() if m["type"] in {"Numeric", "Currency", "Percentage"}]


def _cat(profile):
    return [c for c, m in profile.items() if m["type"] in {"Categorical", "Geographic", "Boolean", "Text"}]


def _date(profile):
    return [c for c, m in profile.items() if m["type"] == "Date"]


def style(fig, title: str | None = None):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=46 if title else 10, b=10),
        font=dict(family="Inter, sans-serif", color="#dbeafe"),
        title=title,
        hovermode="x unified",
        legend=dict(orientation="h", y=1.02, x=0),
    )
    fig.update_xaxes(showgrid=True, gridcolor="rgba(148,163,184,.10)", zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor="rgba(148,163,184,.10)", zeroline=False)
    return fig


def _safe_numeric(df: pd.DataFrame, col: str) -> pd.Series:
    return pd.to_numeric(df[col], errors="coerce")


def _aggregate_by_category(
    df: pd.DataFrame,
    category: str,
    metric: str,
    aggregation: str = "sum",
) -> pd.DataFrame:
    """Aggregate through private names so category and metric may be the same column."""
    grouped = pd.DataFrame(
        {
            "_chart_category": df[category].where(df[category].notna(), "Unknown"),
            "_chart_metric": _safe_numeric(df, metric),
        }
    )
    agg_func = {"mean": "mean", "count": "count", "sum": "sum"}.get(aggregation, "sum")
    result = (
        grouped.groupby("_chart_category", dropna=False)["_chart_metric"]
        .agg(agg_func)
        .rename("_chart_value")
        .reset_index()
        .dropna(subset=["_chart_value"])
    )
    return result


def auto_charts(df: pd.DataFrame, profile: dict, max_rows: int = 20_000) -> list[tuple[str, object]]:
    if df.empty:
        return []
    d = df.head(max_rows).copy()
    figs: list[tuple[str, object]] = []
    dates, nums, cats = _date(profile), _numeric(profile), _cat(profile)

    if dates and nums:
        date_col, num_col = dates[0], nums[0]
        plot = pd.DataFrame({date_col: pd.to_datetime(d[date_col], errors="coerce"), num_col: _safe_numeric(d, num_col)}).dropna()
        if not plot.empty:
            agg = plot.groupby(pd.Grouper(key=date_col, freq="ME"))[num_col].sum().reset_index()
            figs.append(("Trend over time", style(px.area(agg, x=date_col, y=num_col, markers=True, color_discrete_sequence=[PALETTE[1]]))))

    if cats and nums:
        c, n = cats[0], nums[0]
        tmp = d[[c]].copy()
        tmp["_metric"] = _safe_numeric(d, n)
        tmp[c] = tmp[c].fillna("Unknown").astype(str)
        tmp = tmp.groupby(c, dropna=False)["_metric"].sum().reset_index().sort_values("_metric", ascending=False).head(12)
        figs.append((f"{n} by {c}", style(px.bar(tmp, x=c, y="_metric", color="_metric", color_continuous_scale="Purples"))))

    if nums:
        n = nums[0]
        vals = _safe_numeric(d, n).dropna()
        if not vals.empty:
            figs.append((f"Distribution · {n}", style(px.histogram(pd.DataFrame({n: vals}), x=n, nbins=24, color_discrete_sequence=[PALETTE[0]]))))

    if len(nums) >= 2:
        a, b = nums[:2]
        tmp = pd.DataFrame({a: _safe_numeric(d, a), b: _safe_numeric(d, b)}).dropna().head(2500)
        if not tmp.empty:
            figs.append((f"{a} vs {b}", style(px.scatter(tmp, x=a, y=b, color_discrete_sequence=[PALETTE[1]]))))

    if len(nums) >= 3:
        corr = d[nums[:12]].apply(pd.to_numeric, errors="coerce").corr()
        if not corr.empty:
            figs.append(("Correlation heatmap", style(px.imshow(corr, text_auto=".2f", color_continuous_scale="Purples"))))
    return figs[:5]


def custom_chart(df: pd.DataFrame, chart_type: str, x_col: str, y_col: str | None, aggregation: str = "sum"):
    if df.empty or not x_col or x_col not in df.columns:
        return go.Figure()
    d = df.copy()
    if chart_type in {"bar", "line", "area"} and y_col and y_col in d.columns:
        agg = _aggregate_by_category(d, x_col, y_col, aggregation)
        if chart_type == "bar":
            return style(px.bar(agg, x="_chart_category", y="_chart_value", color="_chart_value", color_continuous_scale="Purples"))
        if chart_type == "line":
            return style(px.line(agg, x="_chart_category", y="_chart_value", markers=True, color_discrete_sequence=[PALETTE[1]]))
        return style(px.area(agg, x="_chart_category", y="_chart_value", markers=True, color_discrete_sequence=[PALETTE[1]]))
    if chart_type in {"pie", "donut"} and y_col and y_col in d.columns:
        agg = _aggregate_by_category(d, x_col, y_col, "sum").sort_values("_chart_value", ascending=False).head(12)
        return style(px.pie(agg, names="_chart_category", values="_chart_value", hole=.55 if chart_type == "donut" else 0, color_discrete_sequence=PALETTE))
    if chart_type == "histogram":
        return style(px.histogram(d, x=x_col, nbins=24, color_discrete_sequence=[PALETTE[0]]))
    if chart_type == "scatter" and y_col and y_col in d.columns:
        d[x_col] = pd.to_numeric(d[x_col], errors="coerce")
        d[y_col] = pd.to_numeric(d[y_col], errors="coerce")
        return style(px.scatter(d.dropna(subset=[x_col, y_col]), x=x_col, y=y_col, color_discrete_sequence=[PALETTE[1]]))
    if chart_type == "box":
        d[x_col] = pd.to_numeric(d[x_col], errors="coerce")
        return style(px.box(d, y=x_col, color_discrete_sequence=[PALETTE[0]]))
    return go.Figure()
