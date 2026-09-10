import os
import streamlit as st
from components.ui import section_title


def render_settings():
    section_title("Workspace Settings","Branding, security, session behavior and product configuration.")
    st.text_input("Application name",value=os.getenv("APP_NAME","DataPilot Global"),disabled=True)
    st.text_input("Optional access code",value="Configured via APP_ACCESS_CODE" if os.getenv("APP_ACCESS_CODE") else "Not configured",disabled=True)
    st.write("")
    st.info("For public sharing, deploy the project to Streamlit Community Cloud or a cloud container. For private client portals, set APP_ACCESS_CODE or use a platform-level authentication layer.")
    if st.button("Reset current analysis session"):
        for key in ["raw_df","clean_df","before_quality","after_quality","column_profile","cleaning_log","merge_preview"]:
            st.session_state.pop(key,None)
        st.success("Session analysis was reset. Uploaded dataset metadata remains in memory until the browser session ends.")
