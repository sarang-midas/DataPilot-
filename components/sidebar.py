from __future__ import annotations

import streamlit as st


def render_sidebar(dataset_names: list[str], active_dataset: str | None, current_theme: str):
    with st.sidebar:
        st.markdown(
            "<div class='brand-wrap'><span class='brand-mark'>✦</span><span class='brand-name'>DataPilot Global</span><div class='brand-sub'>AI data cleaning · BI workspace</div></div>",
            unsafe_allow_html=True,
        )

        st.markdown("**Data workspace**")
        uploaded = st.file_uploader(
            "Upload CSV / Excel",
            type=["csv", "xlsx", "xlsm", "xls"],
            accept_multiple_files=True,
            label_visibility="collapsed",
            help="CSV, XLSX, XLSM and XLS. Multiple files and Excel sheets are supported.",
        )
        if dataset_names:
            current_index = dataset_names.index(active_dataset) if active_dataset in dataset_names else 0
            selected = st.selectbox("Active dataset", dataset_names, index=current_index, key="active_dataset_selector")
            if selected != active_dataset:
                st.session_state["active_dataset"] = selected
                st.session_state["loaded_dataset_name"] = None
                st.rerun()
            st.caption(f"{len(dataset_names)} dataset(s) in this session")
        else:
            st.info("No dataset loaded. Try the Demo Dashboard on Home.")

        st.divider()
        st.markdown("**Appearance**")
        theme = st.radio("Theme", ["Dark", "Light"], index=0 if current_theme == "Dark" else 1, horizontal=True, label_visibility="collapsed")

        st.markdown("**Client branding**")
        title = st.text_input("Dashboard title", value=st.session_state.get("dashboard_title", "Executive Analytics"), label_visibility="collapsed", placeholder="Dashboard title")
        brand = st.text_input("Brand name", value=st.session_state.get("brand_name", "DataPilot Analytics"), label_visibility="collapsed", placeholder="Brand name")

        st.divider()
        st.caption("Session-scoped analysis · uploads are processed in memory")
        return uploaded, theme, title, brand
