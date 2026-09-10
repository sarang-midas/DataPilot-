import streamlit as st
from components.ui import section_title
from core.kpi_engine import generate_kpis
from core.insight_engine import deterministic_insights
from core.recommendation_engine import recommendations
from core.exporters import excel_report_bytes, pdf_report_bytes, csv_bytes
from core.data_quality import quality_report


def render_reports():
    df=st.session_state["clean_df"]; profile=st.session_state["column_profile"]; quality=st.session_state["after_quality"] or quality_report(df,profile)
    kpis=generate_kpis(df,profile); insights=deterministic_insights(df,profile); recs=recommendations(quality)
    section_title("Reports & Export","Generate client-ready Excel, CSV and PDF deliverables from the current dashboard state.")
    c1,c2,c3=st.columns(3)
    with c1: st.download_button("Download cleaned CSV",csv_bytes(df),"cleaned_dataset.csv","text/csv",width="stretch")
    with c2: st.download_button("Download Excel report",excel_report_bytes(df,quality,profile,kpis,insights,recs),"analytics_report.xlsx","application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",width="stretch")
    with c3: st.download_button("Download PDF report",pdf_report_bytes(st.session_state.get("dashboard_title","Executive Analytics"),df,quality,kpis,insights,recs),"analytics_report.pdf","application/pdf",width="stretch")
    section_title("Report contents")
    st.write("The export includes cleaned data, quality summary, data dictionary, KPIs, insights, recommendations and a cleaned-data preview.")
