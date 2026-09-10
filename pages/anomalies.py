import streamlit as st
import plotly.express as px
from components.ui import section_title, kpi_card
from core.anomaly_engine import detect_anomalies, forecast_linear


def render_anomalies(df,profile):
    section_title("Anomalies & Forecast","Use IQR/Z-score for explainable monitoring, or Isolation Forest for multivariate anomaly discovery.")
    method=st.selectbox("Anomaly method",["IQR","Z-score","Isolation Forest"])
    anomalies=detect_anomalies(df,profile,method)
    cols=st.columns(3)
    with cols[0]: kpi_card("Anomalies",f"{len(anomalies):,}","detected rows/metrics")
    with cols[1]: kpi_card("Anomaly rate",f"{(len(anomalies)/max(1,len(df))*100):.1f}%","of current rows")
    with cols[2]: kpi_card("Metrics monitored",f"{anomalies['metric'].nunique() if not anomalies.empty else 0}","numeric fields")
    if not anomalies.empty:
        st.dataframe(anomalies.head(200),width="stretch",hide_index=True)
        if "score" in anomalies:
            st.plotly_chart(px.bar(anomalies.head(20),x="metric",y="score",hover_data=["row_index","value"],color="score",color_continuous_scale="Purples"),width="stretch",config={"displaylogo":False})
    else: st.success("No anomalies found with the selected method.")
    section_title("Forecast")
    date_cols=[c for c,m in profile.items() if m["type"]=="Date"]
    nums=[c for c,m in profile.items() if m["type"] in {"Numeric","Currency","Percentage"}]
    if not date_cols or not nums:
        st.info("Forecasting needs at least one date/time column and one numeric metric.")
        return
    d=st.selectbox("Date column",date_cols); n=st.selectbox("Metric",nums); periods=st.slider("Future periods",3,18,6)
    forecast=forecast_linear(df,d,n,periods)
    if forecast.empty: st.warning("Not enough usable history to create a forecast.")
    else:
        actual=df[[d,n]].copy(); actual[d]=__import__('pandas').to_datetime(actual[d],errors='coerce'); actual[n]=__import__('pandas').to_numeric(actual[n],errors='coerce'); actual=actual.dropna().groupby(d,as_index=False)[n].sum()
        st.plotly_chart(__import__('plotly.express').express.line(actual,x=d,y=n,markers=True),width="stretch",config={"displaylogo":False})
        st.dataframe(forecast,width="stretch",hide_index=True)
