import streamlit as st
from components.ui import section_title, insight_card
from core.insight_engine import deterministic_insights, ai_insights
from core.recommendation_engine import recommendations


def render_insights(df,profile):
    section_title("Insights & Recommendations","Deterministic insights run without an API. Optional AI adds narrative, but the dataset remains the source of truth.")
    ins=deterministic_insights(df,profile)
    for x in ins: insight_card(x["title"],x["body"],x["priority"])
    st.markdown("**Optional AI enhancement**")
    if st.button("Generate AI insights", width="content"):
        with st.spinner("Generating constrained narrative from the dataset sample…"):
            ai=ai_insights(df,profile)
        if ai:
            for x in ai: insight_card("AI insight",x,"info")
        else:
            st.warning("AI is not enabled. Add OPENAI_API_KEY to environment variables or Streamlit secrets to enable it; the core analytics still work without it.")
    quality=__import__('core.data_quality',fromlist=['quality_report']).quality_report(df,profile)
    section_title("Smart recommendations")
    recs=recommendations(quality)
    for r in recs: insight_card(r["title"],r["body"],r["priority"])
