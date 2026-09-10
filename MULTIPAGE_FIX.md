# Multipage routing fix

The previous version used a sidebar radio as navigation. This version uses Streamlit's
native `st.navigation()` / `st.Page()` routing, so every workspace page has a real URL.

Routes:
- /
- /dashboard
- /cleaning
- /profiling
- /statistics
- /insights
- /ask_data
- /anomalies
- /reports
- /merge
- /settings_page

Run only:
`streamlit run app.py`

Do not run files under `pages/` directly.
