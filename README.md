# DataPilot Global

**AI-assisted data cleaning + business intelligence workspace built with Streamlit.**

DataPilot Global turns messy CSV/Excel files into a clean, client-ready analytics workspace. It is designed to feel like a small SaaS analytics product rather than a basic Streamlit demo.

## Highlights

- ⚡ Fast session-first workflow with no database required
- 📥 CSV, XLSX, XLSM and XLS uploads
- 📚 Multiple files and multiple Excel sheets
- 🧹 Explainable automatic cleaning
- 🧪 Data-quality scoring before/after cleaning
- 📊 Automatic KPI and dashboard generation
- 🎛️ Interactive dashboard filters
- 📈 Automatic and custom visualizations
- 🔎 Data profiling and statistical analysis
- 💡 Deterministic business insights and recommendations
- 🤖 Optional OpenAI narrative layer with deterministic fallback
- 💬 Safe Ask Your Data — no arbitrary user code execution
- 🚨 IQR, Z-score and Isolation Forest anomaly detection
- 🔮 Lightweight linear forecasting when time-series data is suitable
- 🔗 Visual dataset merge/join workspace
- 📄 CSV, Excel and PDF exports
- 🌙 Dark/light presentation modes
- 🏷️ Client branding and dashboard title controls
- 🔐 Optional access-code gate
- 🧰 Built-in demo datasets
- 🧪 Automated tests
- 🐳 Docker-ready

## Main workflow

```text
Upload → Validate → Clean → Profile → Dashboard → Insights → Monitor → Export
```

## Project structure

```text
global-data-analytics-platform/
├── app.py
├── requirements.txt
├── README.md
├── Dockerfile
├── .env.example
├── .gitignore
├── .streamlit/
│   ├── config.toml
│   └── secrets.toml.example
├── config/
├── components/
├── core/
├── pages/
├── utils/
├── assets/
│   ├── reference/
│   └── sample_data/
├── reference_frontend/
└── tests/
```

## Windows / VS Code setup

PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

Then open the local URL printed by Streamlit, normally:

```text
http://localhost:8501
```

## Linux / macOS

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

## Demo mode

Open **Home** and select **Start with Demo Dashboard**. The project includes a realistic sales dataset so the complete dashboard can be explored without uploading a file.

Sample datasets are also available in `assets/sample_data/`:

- `sales_demo.csv`
- `hr_dirty.csv`
- `marketing_dirty.csv`
- `multi_sheet_demo.xlsx`

## Cleaning engine

The Cleaning Studio supports:

- whitespace cleanup
- duplicate-header protection
- numeric-string conversion
- currency and percentage normalization
- date parsing
- missing-value strategies
- fully empty column removal
- duplicate row removal
- negative-number handling
- IQR outlier removal
- IQR winsorization/capping
- before/after quality scoring
- cleaning audit log
- restore-to-raw workflow

The cleaning engine is deliberately conservative: it does not silently execute arbitrary transformations on user data.

## Dashboard

The dashboard automatically detects:

- numeric metrics
- currency metrics
- percentages
- dates
- categorical dimensions
- geographic dimensions
- boolean fields
- IDs
- text fields

It then generates useful KPIs and charts when the dataset supports them.

The **Visualization Studio** also lets a user build a custom bar, line, area, pie, donut, histogram, scatter or box chart.

## Ask Your Data

The deterministic query layer supports safe questions such as:

```text
What is the total sales?
Which product has the highest sales?
What is the average price?
What is the strongest correlation?
Show monthly sales trend.
How many rows are there?
```

No arbitrary Python, SQL or user-supplied code is executed.

## Optional AI insights

AI is optional. Set an OpenAI key only if you want the narrative enhancement:

```text
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4.1-mini
```

If the key is absent or the API fails, the deterministic analytics continue to work.

Never commit `.env` or real secrets to Git.

## Environment variables

Copy `.env.example` to `.env` for local development:

```text
APP_NAME=DataPilot Global
BRAND_NAME=DataPilot Analytics
APP_ACCESS_CODE=
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4.1-mini
MAX_UPLOAD_MB=200
DEFAULT_MISSING_NUMERIC=median
```

For Streamlit Cloud, use **App Settings → Secrets** rather than committing secrets.

## Tests

Run:

```powershell
pytest -q
```

The included suite covers:

- cleaning behavior
- duplicate/header edge cases
- data loading
- quality scoring
- KPI generation
- Excel sheet loading
- anomaly detection
- forecasting

## Docker

Build:

```bash
docker build -t datapilot-global .
```

Run:

```bash
docker run --rm -p 8501:8501 datapilot-global
```

Open:

```text
http://localhost:8501
```

## Streamlit Community Cloud

1. Push this project to GitHub.
2. Create a new Streamlit app.
3. Select the repository and `app.py` as the main file.
4. Add secrets under the app settings if needed.
5. Deploy.

The application is built around `st.navigation`/`st.Page`, so the entrypoint remains `app.py` while navigation is managed centrally.

## Performance notes

- Large charts are sampled/capped for visualization rather than rendering every row.
- Uploads are kept session-scoped.
- Duplicate upload processing is avoided within a browser session.
- Heavy analytics are only executed when their page is opened.
- AI calls are explicit and user-triggered.

## Security notes

This project does not intentionally persist uploaded datasets in a database. Uploads are processed in the Streamlit session. For production client deployments, combine the optional access code with platform-level authentication, HTTPS, proper secret management and an appropriate data-retention policy.

## Troubleshooting

### `ModuleNotFoundError`

Make sure the virtual environment is active:

```powershell
.venv\Scripts\activate
pip install -r requirements.txt
```

### Excel upload fails

Confirm that the workbook contains at least one non-empty sheet and that the file is not corrupted.

### AI insights do not appear

AI is optional. Check that `OPENAI_API_KEY` is configured. The main analytics features do not require it.

### Dashboard has no charts

The uploaded dataset may not contain enough compatible numeric/date/category columns. Open **Data Profile** to inspect detected types.

### Upload is too large

Increase `MAX_UPLOAD_MB` only when the deployment environment can safely handle the larger file size. Streamlit's server upload limit should also be configured consistently.

## Product roadmap ideas

Potential next-stage production features include SSO/OAuth, persistent workspaces, database-backed projects, scheduled refreshes, team permissions, row-level security, reusable dashboard templates and background jobs for very large datasets.

## License

See `LICENSE`.
