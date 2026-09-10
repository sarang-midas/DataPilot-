# DataPilot — Advanced Data Cleaning & Analytics Workbench

DataPilot is a browser-based project that lets a user upload CSV, Excel or JSON data, inspect data quality, apply cleaning rules, generate automatic insights and build interactive visualizations.

## Features

- CSV, XLSX, XLS and JSON import
- Automatic column-type detection: numeric, date, categorical and text
- Data-quality score using completeness, validity and uniqueness
- Missing values, duplicates, invalid values and data profiling
- Cleaning: trim whitespace, normalize numbers, fill/drop missing values, remove duplicates, IQR outlier filtering and optional negative-value correction
- Audit trail for cleaning operations
- Visualizations: bar, line, area, pie, donut, scatter and histogram
- Automatic chart recommendations
- Numeric summary statistics and correlation insight
- Cleaned CSV/JSON export
- JSON quality/report export
- Searchable data preview
- No backend required for the MVP; processing stays in the browser session

## Run in VS Code

### 1. Requirements

Install Node.js (LTS recommended).

### 2. Open the project

Unzip the project and open the `data-pilot` folder in VS Code.

### 3. Install dependencies

```bash
npm install
```

### 4. Start the development server

```bash
npm run dev
```

Vite will print a local URL. Open it in your browser.

### 5. Production build

```bash
npm run build
```

### 6. Preview the production build

```bash
npm run preview
```

## Suggested next upgrades for a final-year / portfolio version

1. Add FastAPI backend for large files and server-side processing.
2. Add PySpark for very large datasets.
3. Add PostgreSQL for dataset history and user accounts.
4. Add an LLM-powered data analyst that converts natural-language questions into safe dataframe operations.
5. Add PDF report generation.
6. Add Docker and deploy to Azure.
7. Add authentication and dataset version history.

## Project structure

```text
DataPilot/
├── index.html
├── package.json
├── README.md
└── src/
    ├── main.jsx
    └── styles.css
```
