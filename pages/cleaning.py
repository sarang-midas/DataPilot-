from __future__ import annotations

import streamlit as st

from components.ui import section_title, kpi_card
from core.column_detector import detect_columns
from core.data_cleaner import CleaningConfig, clean_dataframe
from core.data_quality import quality_report


def render_cleaning():
    raw = st.session_state["raw_df"]
    current = st.session_state["clean_df"]
    before = st.session_state["before_quality"]
    after = st.session_state["after_quality"]

    section_title("Cleaning Studio", "Conservative, explainable transformations with a restore point and before/after quality monitoring.")

    if raw is None or current is None:
        st.warning("No dataset is loaded.")
        return

    cfg = CleaningConfig(**st.session_state.get("last_clean_config", CleaningConfig().__dict__))
    left, right = st.columns(2)
    with left:
        cfg.trim_whitespace = st.checkbox("Trim whitespace", cfg.trim_whitespace)
        cfg.normalize_numeric = st.checkbox("Normalize numeric strings", cfg.normalize_numeric)
        cfg.parse_dates = st.checkbox("Parse date-like columns", cfg.parse_dates)
        cfg.drop_empty_columns = st.checkbox("Drop fully empty columns", cfg.drop_empty_columns)
        case_options = ["Keep", "lower", "UPPER", "Title"]
        cfg.normalize_case = st.selectbox("Text case normalization", case_options, index=case_options.index(cfg.normalize_case) if cfg.normalize_case in case_options else 0)
    with right:
        numeric_options = ["Median", "Mean", "Forward fill", "Backward fill", "Constant", "Drop rows"]
        text_options = ["Mode", "Constant", "Drop rows"]
        outlier_options = ["Keep", "Remove", "Cap/Winsorize"]
        negative_options = ["Flag", "Keep", "Convert to absolute"]
        cfg.missing_numeric = st.selectbox("Numeric missing values", numeric_options, index=numeric_options.index(cfg.missing_numeric) if cfg.missing_numeric in numeric_options else 0)
        cfg.missing_text = st.selectbox("Text missing values", text_options, index=text_options.index(cfg.missing_text) if cfg.missing_text in text_options else 0)
        cfg.missing_constant = st.text_input("Constant fill value", cfg.missing_constant)
        cfg.duplicate_action = st.selectbox("Duplicates", ["Remove", "Keep"], index=0 if cfg.duplicate_action == "Remove" else 1)
        cfg.outlier_method = st.selectbox("Outliers", outlier_options, index=outlier_options.index(cfg.outlier_method) if cfg.outlier_method in outlier_options else 0)
        cfg.negative_action = st.selectbox("Negative numbers", negative_options, index=negative_options.index(cfg.negative_action) if cfg.negative_action in negative_options else 0)

    st.session_state["last_clean_config"] = cfg.__dict__.copy()

    action_cols = st.columns([2, 1, 1])
    with action_cols[0]:
        run_clean = st.button("✨ Clean & Generate Dashboard", type="primary", width="stretch")
    with action_cols[1]:
        restore = st.button("↩ Restore raw", width="stretch")
    with action_cols[2]:
        preview = st.button("Preview current", width="stretch")

    if run_clean:
        with st.spinner("Scanning, cleaning, profiling and scoring…"):
            cleaned, log, bq, aq = clean_dataframe(raw, cfg)
        st.session_state["clean_df"] = cleaned
        st.session_state["before_quality"] = bq
        st.session_state["after_quality"] = aq
        st.session_state["column_profile"] = detect_columns(cleaned)
        st.session_state["cleaning_log"] = log
        st.success("Cleaning complete. The dashboard now uses the cleaned dataset.")
        st.rerun()

    if restore:
        restored = raw.copy()
        profile = detect_columns(restored)
        st.session_state["clean_df"] = restored
        st.session_state["column_profile"] = profile
        st.session_state["before_quality"] = quality_report(raw, detect_columns(raw))
        st.session_state["after_quality"] = quality_report(restored, profile)
        st.session_state["cleaning_log"] = ["Restored the original uploaded dataset. No cleaning changes are currently applied."]
        st.rerun()

    if preview:
        st.dataframe(current.head(100), width="stretch", hide_index=True)

    cols = st.columns(4)
    for col, label, value, sub in [
        (cols[0], "Before score", before["score"], "quality monitor"),
        (cols[1], "After score", after["score"], f"{after['score'] - before['score']:+d} points"),
        (cols[2], "Missing cells", after["missing"], "remaining"),
        (cols[3], "Duplicates", after["duplicates"], "remaining"),
    ]:
        with col:
            kpi_card(label, f"{value:,}" if isinstance(value, int) else str(value), sub)

    section_title("Cleaning audit", "Every run leaves a concise transformation log.")
    for line in st.session_state.get("cleaning_log", []):
        st.info(line)
    if not st.session_state.get("cleaning_log"):
        st.info("No cleaning run yet. The uploaded data remains available as the restore point.")

    section_title("Before vs after", "A transparent view of quality movement.")
    st.dataframe(
        {
            "Metric": ["Rows", "Missing values", "Duplicates / IDs", "Invalid values", "Outliers", "Inconsistencies", "Quality score"],
            "Before": [before[k] for k in ["rows", "missing", "duplicates", "invalid", "outliers", "inconsistencies", "score"]],
            "After": [after[k] for k in ["rows", "missing", "duplicates", "invalid", "outliers", "inconsistencies", "score"]],
        },
        width="stretch",
        hide_index=True,
    )
    st.download_button("Download current cleaned CSV", current.to_csv(index=False).encode("utf-8-sig"), "cleaned_dataset.csv", "text/csv", width="stretch")
