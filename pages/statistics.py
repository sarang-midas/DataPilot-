import streamlit as st
import plotly.express as px
from components.ui import section_title
from core.statistics import numeric_summary, correlation_matrix


def render_statistics(df,profile):
    section_title("Statistical Lab","Descriptive statistics and relationships selected from detected numeric fields.")
    table=numeric_summary(df,profile)
    if table.empty:
        st.info("No numeric columns were detected for statistical analysis.")
        return
    st.dataframe(table.style.format(precision=3),width="stretch",hide_index=True)
    corr=correlation_matrix(df,profile)
    if not corr.empty and corr.shape[0]>1:
        st.markdown("**Correlation matrix**")
        st.plotly_chart(px.imshow(corr,text_auto=".2f",color_continuous_scale="Purples"),width="stretch",config={"displaylogo":False})
