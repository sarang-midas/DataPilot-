from __future__ import annotations

import html
import streamlit as st


def apply_global_css() -> None:
    dark = st.session_state.get("theme", "Dark") == "Dark"
    bg = "#07111f" if dark else "#f6f8fc"
    panel = "#0d1b2e" if dark else "#ffffff"
    panel2 = "#11243a" if dark else "#f1f5f9"
    text = "#f7fbff" if dark else "#102033"
    muted = "#8ea3bb" if dark else "#64748b"
    border = "rgba(148,163,184,.16)" if dark else "rgba(15,23,42,.09)"
    css = f"""
    <style>
    :root {{ --bg:{bg}; --panel:{panel}; --panel2:{panel2}; --text:{text}; --muted:{muted}; --border:{border}; --accent:#7c5cff; --cyan:#22d3ee; --green:#34d399; }}
    .stApp {{ background: radial-gradient(circle at 8% 0%, rgba(124,92,255,.16), transparent 27%), radial-gradient(circle at 95% 8%, rgba(34,211,238,.09), transparent 22%), {bg}; color:var(--text); }}
    .block-container {{ max-width:1480px; padding-top:1.25rem; padding-bottom:4rem; }}
    [data-testid="stSidebar"] {{ background:linear-gradient(180deg, #081426 0%, #07111f 100%); border-right:1px solid rgba(148,163,184,.12); }}
    [data-testid="stSidebar"] * {{ color:#dbeafe; }}
    [data-testid="stSidebar"] .stButton button {{ width:100%; }}
    .brand-wrap {{ padding:.2rem .2rem 1rem; }}
    .brand-mark {{ width:42px; height:42px; display:inline-flex; align-items:center; justify-content:center; border-radius:13px; background:linear-gradient(135deg,#7c5cff,#22d3ee); color:white; font-size:1.25rem; font-weight:900; margin-right:.65rem; vertical-align:middle; box-shadow:0 10px 28px rgba(124,92,255,.3); }}
    .brand-name {{ font-size:1.08rem; font-weight:850; letter-spacing:-.03em; vertical-align:middle; }}
    .brand-sub {{ color:#8ea3bb; font-size:.73rem; margin:.35rem 0 0 3.2rem; }}
    .hero {{ display:flex; align-items:flex-end; justify-content:space-between; gap:1.5rem; margin:.35rem 0 1.25rem; }}
    .hero h1 {{ font-size:2.35rem; line-height:1.02; margin:.15rem 0 .45rem; letter-spacing:-.055em; }}
    .hero p {{ color:var(--muted); margin:0; font-size:.95rem; }}
    .eyebrow {{ color:#a99cff; font-size:.68rem; letter-spacing:.14em; font-weight:850; text-transform:uppercase; }}
    .status-pill {{ display:inline-flex; align-items:center; gap:.4rem; padding:.34rem .7rem; border-radius:999px; font-size:.67rem; font-weight:850; background:rgba(52,211,153,.1); color:#6ee7b7; border:1px solid rgba(52,211,153,.2); white-space:nowrap; }}
    .status-pill:before {{ content:""; width:6px; height:6px; border-radius:50%; background:#34d399; box-shadow:0 0 0 4px rgba(52,211,153,.1); }}
    .glass-card {{ background:linear-gradient(145deg,rgba(255,255,255,.055),rgba(255,255,255,.018)); border:1px solid var(--border); border-radius:24px; padding:1.25rem; box-shadow:0 18px 55px rgba(0,0,0,.12); }}
    .kpi {{ background:linear-gradient(145deg,rgba(255,255,255,.065),rgba(255,255,255,.018)); border:1px solid var(--border); border-radius:18px; padding:1rem 1.05rem; min-height:116px; box-shadow:0 10px 32px rgba(0,0,0,.1); transition:transform .15s ease,border-color .15s ease; }}
    .kpi:hover {{ transform:translateY(-2px); border-color:rgba(124,92,255,.38); }}
    .kpi .label {{ color:var(--muted); font-size:.72rem; font-weight:750; text-transform:uppercase; letter-spacing:.04em; }}
    .kpi .value {{ font-size:1.85rem; font-weight:900; line-height:1.12; margin:.42rem 0 .14rem; letter-spacing:-.045em; }}
    .kpi .sub {{ color:var(--muted); font-size:.7rem; }}
    .section-title {{ margin:1.45rem 0 .32rem; font-size:1.08rem; font-weight:850; letter-spacing:-.025em; }}
    .small-muted {{ color:var(--muted); font-size:.78rem; }}
    .metric-grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(170px,1fr)); gap:.75rem; }}
    .insight-card {{ padding:1rem 1.05rem; margin:.55rem 0; border-radius:15px; background:var(--panel2); border:1px solid var(--border); }}
    .priority-critical {{ border-left:4px solid #fb7185; }} .priority-high {{ border-left:4px solid #f59e0b; }} .priority-medium {{ border-left:4px solid #38bdf8; }} .priority-low {{ border-left:4px solid #34d399; }} .priority-info {{ border-left:4px solid #a78bfa; }}
    .empty {{ text-align:center; padding:3rem 1.5rem; border:1px dashed rgba(148,163,184,.25); border-radius:24px; background:rgba(255,255,255,.02); }}
    .footer-note {{ color:var(--muted); font-size:.7rem; text-align:center; margin-top:2rem; }}
    .stButton > button, .stDownloadButton > button {{ border-radius:11px; min-height:2.55rem; font-weight:700; }}
    div[data-testid="stMetric"] {{ background:transparent; }}
    @media (max-width: 800px) {{ .hero {{ align-items:flex-start; flex-direction:column; }} .hero h1 {{ font-size:1.8rem; }} }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def page_header(title: str, subtitle: str) -> None:
    st.markdown(
        f"<div class='hero'><div><div class='eyebrow'>DATAPILOT GLOBAL · ANALYTICS</div><h1>{html.escape(title)}</h1><p>{html.escape(subtitle)}</p></div><span class='status-pill'>Workspace active</span></div>",
        unsafe_allow_html=True,
    )


def kpi_card(label: str, value: str, sub: str = "") -> None:
    st.markdown(
        f"<div class='kpi'><div class='label'>{html.escape(str(label))}</div><div class='value'>{html.escape(str(value))}</div><div class='sub'>{html.escape(str(sub))}</div></div>",
        unsafe_allow_html=True,
    )


def section_title(title: str, subtitle: str | None = None) -> None:
    st.markdown(f"<div class='section-title'>{html.escape(title)}</div>", unsafe_allow_html=True)
    if subtitle:
        st.markdown(f"<div class='small-muted'>{html.escape(subtitle)}</div>", unsafe_allow_html=True)


def empty_state(title: str, text: str, button_text: str | None = None) -> None:
    st.markdown(
        f"<div class='empty'><div class='eyebrow'>READY WHEN YOU ARE</div><h2>{html.escape(title)}</h2><p class='small-muted'>{html.escape(text)}</p></div>",
        unsafe_allow_html=True,
    )


def insight_card(title: str, body: str, priority: str = "info") -> None:
    p = str(priority).lower()
    cls = f"priority-{p}" if p in {"critical", "high", "medium", "low", "info"} else "priority-info"
    st.markdown(
        f"<div class='insight-card {cls}'><strong>{html.escape(str(title))}</strong><div class='small-muted' style='margin-top:.25rem'>{html.escape(str(body))}</div></div>",
        unsafe_allow_html=True,
    )
