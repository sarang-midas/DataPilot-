from __future__ import annotations

import pandas as pd
import streamlit as st

from components.ui import kpi_card, section_title, insight_card
from core.kpi_engine import generate_kpis
from core.visualization_engine import auto_charts, custom_chart
from core.insight_engine import deterministic_insights


def _filtered(df: pd.DataFrame, profile: dict) -> pd.DataFrame:
    if df.empty:
        return df
    with st.expander("Dashboard filters", expanded=True):
        filt = df.copy()
        dataset_key = str(st.session_state.get("active_dataset", "dataset"))
        cat_cols = [c for c, m in profile.items() if m["type"] in {"Categorical", "Geographic", "Boolean"}]
        date_cols = [c for c, m in profile.items() if m["type"] == "Date"]
        filter_cols = st.columns(4)
        for i, c in enumerate(cat_cols[:3]):
            vals = sorted(filt[c].dropna().astype(str).unique().tolist())[:500]
            key = f"dashboard_filter_{dataset_key}_{c}"
            pick = filter_cols[i].multiselect(c, vals, key=key, placeholder="All values")
            if pick:
                filt = filt[filt[c].astype(str).isin(pick)]
        if date_cols:
            d = date_cols[0]
            dates = pd.to_datetime(filt[d], errors="coerce").dropna()
            if not dates.empty:
                mn, mx = dates.min().date(), dates.max().date()
                selected = filter_cols[3].date_input("Date range", value=(mn, mx), min_value=mn, max_value=mx, key=f"dashboard_date_{dataset_key}_{d}")
                if isinstance(selected, tuple) and len(selected) == 2:
                    start, end = selected
                    parsed = pd.to_datetime(filt[d], errors="coerce")
                    filt = filt[(parsed.dt.date >= start) & (parsed.dt.date <= end)]
    return filt


def render_dashboard(df: pd.DataFrame, profile: dict, quality: dict):
    section_title("Executive dashboard", "A fast, automatically generated BI view that adapts to the active dataset and filters.")
    filtered = _filtered(df, profile)

    if filtered.empty:
        st.warning("No rows match the current filters. Clear a filter to continue.")
        return

    kpis = generate_kpis(filtered, profile)
    cols = st.columns(min(6, max(1, len(kpis))))
    for col, kpi in zip(cols, kpis):
        with col:
            kpi_card(kpi["label"], kpi["value"], kpi["sub"])

    section_title("Performance overview")
    chart_count = st.slider("Number of automatic charts", 2, 5, 4, key="dashboard_chart_count")
    charts = auto_charts(filtered, profile, max_rows=20_000)[:chart_count]
    if charts:
        for i in range(0, len(charts), 2):
            pair = charts[i:i + 2]
            chart_cols = st.columns(len(pair))
            for col, (title, fig) in zip(chart_cols, pair):
                with col:
                    st.markdown(f"**{title}**")
                    st.plotly_chart(fig, width="stretch", config={"displaylogo": False, "responsive": True})
    else:
        st.info("Not enough compatible columns were detected to build automatic charts.")

    with st.expander("Visualization Studio · build a custom chart"):
        all_cols = list(filtered.columns)
        numeric_cols = [c for c, m in profile.items() if m["type"] in {"Numeric", "Currency", "Percentage"}]
        chart_type = st.selectbox("Chart type", ["bar", "line", "area", "pie", "donut", "histogram", "scatter", "box"], key="custom_chart_type")
        x_default = all_cols[0] if all_cols else None
        x_col = st.selectbox("X / category", all_cols, index=0 if all_cols else None, key="custom_chart_x") if all_cols else None
        needs_y = chart_type not in {"histogram", "box"}
        y_col = st.selectbox("Y / metric", numeric_cols, key="custom_chart_y") if needs_y and numeric_cols else None
        aggregation = st.selectbox("Aggregation", ["sum", "mean", "count"], key="custom_chart_agg") if chart_type in {"bar", "line", "area"} and y_col else "sum"
        if chart_type in {"bar", "line", "area", "pie", "donut", "scatter"} and not y_col:
            st.info("Select a numeric metric for this chart type.")
        else:
            fig = custom_chart(filtered, chart_type, x_col, y_col, aggregation)
            st.plotly_chart(fig, width="stretch", config={"displaylogo": False, "responsive": True})

    section_title("Data story", "Evidence-based observations from the currently visible data.")
    insights = deterministic_insights(filtered, profile)
    if not insights:
        st.info("More data is needed to generate meaningful business insights.")
    else:
        for item in insights:
            insight_card(item["title"], item["body"], item["priority"])

    st.markdown(
        f"<div class='footer-note'>Quality score {quality.get('score', 0)}/100 · {len(filtered):,} visible rows · {filtered.shape[1]:,} columns</div>",
        unsafe_allow_html=True,
    )
