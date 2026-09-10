from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
import streamlit as st

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

try:
    for _key in (
        "APP_NAME",
        "BRAND_NAME",
        "APP_ACCESS_CODE",
        "OPENAI_API_KEY",
        "OPENAI_MODEL",
        "MAX_UPLOAD_MB",
    ):
        if _key in st.secrets and _key not in os.environ:
            os.environ[_key] = str(st.secrets[_key])
except Exception:
    pass

from config.settings import APP_CONFIG
from components.sidebar import render_sidebar
from components.ui import apply_global_css, page_header, section_title, empty_state
from core.data_loader import load_uploaded_bytes
from core.data_quality import quality_report
from core.column_detector import detect_columns
from core.data_cleaner import CleaningConfig, clean_dataframe
from pages.dashboard import render_dashboard
from pages.cleaning import render_cleaning
from pages.profiling import render_profiling
from pages.statistics import render_statistics
from pages.insights import render_insights
from pages.ask_data import render_ask_data
from pages.anomalies import render_anomalies
from pages.reports import render_reports
from pages.merge import render_merge
from pages.settings_page import render_settings
from utils.logger import configure_logging


configure_logging()

_NAV_DASHBOARD_PAGE = None
st.set_page_config(
    page_title=APP_CONFIG["name"],
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

def init_state() -> None:
    defaults = {
        "datasets": {},
        "processed_uploads": set(),
        "active_dataset": None,
        "loaded_dataset_name": None,
        "raw_df": None,
        "clean_df": None,
        "before_quality": None,
        "after_quality": None,
        "column_profile": None,
        "cleaning_log": [],
        "last_clean_config": CleaningConfig().__dict__.copy(),
        "dashboard_title": "Executive Analytics",
        "brand_name": APP_CONFIG["brand_name"],
        "logo_url": "",
        "access_granted": False,
        "theme": "Dark",
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


def access_gate() -> bool:
    required = os.getenv("APP_ACCESS_CODE", "").strip()
    if not required:
        return True

    if st.session_state.get("access_granted"):
        return True

    st.markdown("<div class='login-shell'>", unsafe_allow_html=True)
    st.markdown(
        "<div class='login-card'>"
        "<div class='eyebrow'>CLIENT PORTAL</div>"
        "<h1>Secure Analytics Workspace</h1>"
        "<p>Enter the access code provided by the workspace owner.</p>"
        "</div>",
        unsafe_allow_html=True,
    )
    code = st.text_input("Access code", type="password", key="access_code")
    if st.button("Enter workspace", width="stretch", type="primary"):
        if code == required:
            st.session_state["access_granted"] = True
            st.rerun()
        st.error("Access code is not correct.")

    st.markdown("</div>", unsafe_allow_html=True)
    return False


def register_uploaded_files(uploaded_files) -> bool:
    """Replace the working dataset set with the latest upload selection."""
    if not uploaded_files:
        return False

    fresh_datasets: dict[str, pd.DataFrame] = {}
    fresh_signatures: set[str] = set()
    changed = False

    for uploaded in uploaded_files or []:
        name = Path(uploaded.name).name
        try:
            file_id = getattr(uploaded, "file_id", None)
            size = int(getattr(uploaded, "size", 0) or 0)
            quick_signature = f"{name}:{size}:{file_id or 'no-id'}"
            payload = uploaded.getvalue()
            if file_id:
                signature = quick_signature
            else:
                import hashlib
                edge = payload[:65536] + payload[-65536:]
                signature = f"{quick_signature}:{hashlib.sha256(edge).hexdigest()}"

            processed_uploads = st.session_state.get("processed_uploads", set())
            if signature in fresh_signatures or signature in processed_uploads:
                continue

            loaded = load_uploaded_bytes(name, payload)
            for dataset_name, frame in loaded.items():
                fresh_datasets[dataset_name] = frame
            fresh_signatures.add(signature)
            if file_id:
                fresh_signatures.add(quick_signature)
            changed = changed or bool(loaded)
        except Exception as exc:
            st.error(f"Could not read **{name}**: {exc}")

    if not fresh_datasets:
        return False

    st.session_state["datasets"] = fresh_datasets
    st.session_state["processed_uploads"] = fresh_signatures
    selected_name = next(iter(fresh_datasets))
    activate_dataset(selected_name)
    return changed


def activate_dataset(name: str) -> None:
    if name not in st.session_state["datasets"]:
        return

    raw = st.session_state["datasets"][name].copy()
    st.session_state["active_dataset"] = name
    st.session_state["loaded_dataset_name"] = name
    st.session_state["raw_df"] = raw
    st.session_state["clean_df"] = raw.copy()

    profile = detect_columns(raw)
    st.session_state["column_profile"] = profile
    st.session_state["before_quality"] = quality_report(raw, profile)
    st.session_state["after_quality"] = quality_report(raw, profile)
    st.session_state["cleaning_log"] = []


def load_demo() -> None:
    sample_path = Path(__file__).parent / "assets" / "sample_data" / "sales_demo.csv"
    df = pd.read_csv(sample_path, parse_dates=["order_date"])

    st.session_state["datasets"] = {"Sales Demo": df}
    st.session_state["processed_uploads"] = set()
    activate_dataset("Sales Demo")

    cleaned, log, before_quality, after_quality = clean_dataframe(
        df, CleaningConfig()
    )
    st.session_state["clean_df"] = cleaned
    st.session_state["before_quality"] = before_quality
    st.session_state["after_quality"] = after_quality
    st.session_state["column_profile"] = detect_columns(cleaned)
    st.session_state["cleaning_log"] = log


def render_home() -> None:
    """Landing page that replaces the old app-only route."""
    page_header(
        st.session_state["dashboard_title"],
        f"{st.session_state['brand_name']} · AI-assisted data quality, analytics and reporting",
    )

    col1, col2 = st.columns([1.4, 1])
    with col1:
        st.markdown(
            """
            <div class="glass-card">
                <div class="eyebrow">GLOBAL ANALYTICS WORKSPACE</div>
                <h1 style="margin-bottom:0.35rem;">From messy files to client-ready BI.</h1>
                <p style="font-size:1.05rem;">
                    Upload Excel/CSV data, clean it automatically, generate KPIs and
                    interactive charts, explore anomalies, ask questions, and export
                    professional reports.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("▶ Start with Demo Dashboard", type="primary", width="stretch"):
            load_demo()
            if _NAV_DASHBOARD_PAGE is not None:
                st.switch_page(_NAV_DASHBOARD_PAGE)
            st.rerun()
        st.caption("The demo works without uploading your own files.")

    with col2:
        st.markdown(
            """
            <div class="glass-card">
                <h3>Workspace flow</h3>
                <p>Upload → Validate → Clean → Profile → Dashboard → Insights → Export</p>
                <hr>
                <p><b>Client-ready:</b> responsive SaaS layout, charts, KPIs, reports and
                optional access-code protection.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if st.session_state.get("clean_df") is not None:
        section_title("Current workspace")
        df = st.session_state["clean_df"]
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Rows", f"{len(df):,}")
        c2.metric("Columns", f"{df.shape[1]:,}")
        c3.metric("Datasets", f"{len(st.session_state['datasets']):,}")
        c4.metric("Active", st.session_state.get("active_dataset") or "—")


def no_dataset_page(page_title: str, description: str) -> bool:
    """Render a friendly empty state and return True when no data is available."""
    page_header(
        st.session_state["dashboard_title"],
        f"{st.session_state['brand_name']} · {page_title}",
    )

    if st.session_state.get("clean_df") is None:
        empty_state(
            "No dataset loaded",
            description,
            "Load the built-in Sales Demo from Home or upload a CSV/Excel file from the sidebar.",
        )
        if st.button("Load Sales Demo", type="primary"):
            load_demo()
            st.rerun()
        return True

    return False


def dashboard_page() -> None:
    if no_dataset_page("Dashboard", "Your KPIs and interactive analytics will appear here."):
        return
    render_dashboard(
        st.session_state["clean_df"],
        st.session_state["column_profile"],
        st.session_state["after_quality"],
    )


def cleaning_page() -> None:
    if no_dataset_page("Cleaning Studio", "Inspect and clean your uploaded dataset."):
        return
    render_cleaning()


def profiling_page() -> None:
    if no_dataset_page("Data Profile", "Profile columns, quality and dataset structure."):
        return
    render_profiling(
        st.session_state["clean_df"],
        st.session_state["column_profile"],
        st.session_state["after_quality"],
    )


def statistics_page() -> None:
    if no_dataset_page("Statistics", "Explore descriptive statistics and correlations."):
        return
    render_statistics(
        st.session_state["clean_df"],
        st.session_state["column_profile"],
    )


def insights_page() -> None:
    if no_dataset_page("Insights", "Generate evidence-based trends and recommendations."):
        return
    render_insights(
        st.session_state["clean_df"],
        st.session_state["column_profile"],
    )


def ask_data_page() -> None:
    if no_dataset_page("Ask Your Data", "Ask natural-language questions about the active dataset."):
        return
    render_ask_data(
        st.session_state["clean_df"],
        st.session_state["column_profile"],
    )


def anomalies_page() -> None:
    if no_dataset_page("Anomalies & Forecast", "Detect anomalies and explore usable time-series forecasts."):
        return
    render_anomalies(
        st.session_state["clean_df"],
        st.session_state["column_profile"],
    )


def reports_page() -> None:
    if no_dataset_page("Reports", "Generate downloadable Excel, CSV and PDF outputs."):
        return
    render_reports()


def merge_page() -> None:
    page_header(
        st.session_state["dashboard_title"],
        f"{st.session_state['brand_name']} · Merge Datasets",
    )
    if not st.session_state.get("datasets"):
        empty_state(
            "No datasets loaded",
            "Upload at least two CSV/Excel datasets from the sidebar before opening the merge workspace.",
            "Upload datasets",
        )
        return
    render_merge(st.session_state["datasets"])


def settings_page() -> None:
    page_header(
        st.session_state["dashboard_title"],
        f"{st.session_state['brand_name']} · Settings",
    )
    render_settings()


def render_app() -> None:
    init_state()
    apply_global_css()

    if not access_gate():
        st.stop()

    uploaded_files, theme, dashboard_title, brand_name = render_sidebar(
        dataset_names=list(st.session_state["datasets"].keys()),
        active_dataset=st.session_state.get("active_dataset"),
        current_theme=st.session_state.get("theme", "Dark"),
    )

    theme_changed = theme != st.session_state.get("theme", "Dark")
    st.session_state["theme"] = theme
    st.session_state["dashboard_title"] = (dashboard_title or "Executive Analytics").strip() or "Executive Analytics"
    st.session_state["brand_name"] = (brand_name or APP_CONFIG["brand_name"]).strip() or APP_CONFIG["brand_name"]
    apply_global_css()

    uploads_changed = register_uploaded_files(uploaded_files)
    if uploads_changed or theme_changed:
        st.rerun()

    if st.session_state["datasets"]:
        selected = st.session_state.get("active_dataset")
        if selected not in st.session_state["datasets"]:
            selected = next(iter(st.session_state["datasets"]))

        if (
            st.session_state.get("raw_df") is None
            or st.session_state.get("loaded_dataset_name") != selected
        ):
            activate_dataset(selected)

    pages = {
        "Workspace": [
            st.Page(
                render_home,
                title="Home",
                icon="🏠",
                url_path="",
                default=True,
            ),
        ],
        "Analytics": [
            st.Page(
                dashboard_page,
                title="Dashboard",
                icon="📊",
                url_path="dashboard",
            ),
            st.Page(
                cleaning_page,
                title="Cleaning Studio",
                icon="🧹",
                url_path="cleaning",
            ),
            st.Page(
                profiling_page,
                title="Data Profile",
                icon="🔎",
                url_path="profiling",
            ),
            st.Page(
                statistics_page,
                title="Statistics",
                icon="📈",
                url_path="statistics",
            ),
            st.Page(
                insights_page,
                title="Insights",
                icon="💡",
                url_path="insights",
            ),
            st.Page(
                ask_data_page,
                title="Ask Your Data",
                icon="💬",
                url_path="ask_data",
            ),
            st.Page(
                anomalies_page,
                title="Anomalies & Forecast",
                icon="⚡",
                url_path="anomalies",
            ),
        ],
        "Workspace Tools": [
            st.Page(
                reports_page,
                title="Reports",
                icon="📄",
                url_path="reports",
            ),
            st.Page(
                merge_page,
                title="Merge Datasets",
                icon="🔗",
                url_path="merge",
            ),
            st.Page(
                settings_page,
                title="Settings",
                icon="⚙️",
                url_path="settings_page",
            ),
        ],
    }

    global _NAV_DASHBOARD_PAGE
    _NAV_DASHBOARD_PAGE = pages["Analytics"][0]
    pg = st.navigation(pages, position="sidebar", expanded=True)
    pg.run()


if __name__ == "__main__":
    render_app()
