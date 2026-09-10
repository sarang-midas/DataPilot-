import streamlit as st
import pandas as pd
from components.ui import section_title, kpi_card


def render_profiling(df, profile, quality):
    section_title("Data Profile","Automatic column intelligence, cardinality, quality flags and descriptive summaries.")
    cols=st.columns(6)
    values=[("Rows",len(df)),("Columns",len(df.columns)),("Missing",quality["missing"]),("Duplicate IDs / rows",quality["duplicates"]),("Numeric",sum(m["type"] in {"Numeric","Currency","Percentage"} for m in profile.values())),("Categorical",sum(m["type"] in {"Categorical","Geographic","Boolean"} for m in profile.values()))]
    for c,(label,v) in zip(cols,values):
        with c:kpi_card(label,f"{v:,}","profile scan")
    rows=[]
    for c,m in profile.items():
        q=quality["by_column"].get(c,{})
        rows.append({"Column":c,"Detected type":m["type"],"Missing":q.get("missing",0),"Unique":q.get("unique",0),"Invalid":q.get("invalid",0),"Outliers":q.get("outliers",0),"Potential metric":m["potential_metric"],"Potential dimension":m["potential_dimension"]})
    section_title("Column intelligence")
    st.dataframe(pd.DataFrame(rows),width="stretch",hide_index=True)
    section_title("Sample records")
    st.dataframe(df.head(100),width="stretch",hide_index=True)
