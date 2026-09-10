# Advanced Prompt: Build a Global, Client-Ready Streamlit Analytics Platform

You are an expert **Python developer, Data Engineer, Data Scientist, UI/UX designer, and Streamlit architect**.

I want you to build a **complete, advanced, production-style, globally usable web application using Streamlit**. The application should look like a **real professional SaaS analytics dashboard**, not like a basic Streamlit demo.

The application should be designed so that I can **share the dashboard with clients, companies, team members, or customers through a public URL**, and users should be able to upload their own Excel/CSV/data files and immediately receive a cleaned, analyzed, and highly visual dashboard.

## 1. Main Objective

Build a platform similar to a professional:

**"AI-Powered Data Cleaning + Automated Analytics + Dashboard Generator"**

The user uploads:

* Excel files
* CSV files
* Multiple Excel sheets
* Multiple CSV files

The application should automatically:

1. Detect the uploaded file type.
2. Read the data safely.
3. Detect data quality problems.
4. Clean the data automatically.
5. Show the original vs cleaned data.
6. Explain what cleaning operations were performed.
7. Detect useful columns automatically.
8. Generate meaningful KPIs.
9. Generate charts automatically.
10. Generate an interactive dashboard.
11. Generate statistical insights.
12. Generate downloadable reports.
13. Allow the user to download the cleaned dataset.
14. Allow the user to download the dashboard/report.
15. Provide an attractive client-ready UI.

The system should support **multiple domains**, such as:

* Sales
* Finance
* HR
* Marketing
* E-commerce
* Healthcare
* Education
* Manufacturing
* Agriculture
* Customer analytics
* General business data

Do NOT hard-code the application for only one dataset.

---

# 2. Global / Shareable Website Requirement

The application must be designed as a **globally accessible Streamlit web application**.

It should be possible to deploy it using:

* Streamlit Community Cloud
* Docker
* AWS
* Azure
* Google Cloud
* Any other cloud platform

The project must include:

* `requirements.txt`
* `README.md`
* `.gitignore`
* `.env.example`
* Dockerfile
* deployment instructions
* Streamlit configuration
* environment variable support
* secure configuration
* proper project structure

Do not hard-code API keys, passwords, tokens, or credentials.

Use environment variables and Streamlit secrets where required.

---

# 3. Professional Dashboard UI

The UI should look like a **modern SaaS analytics product**.

Create a professional layout containing:

### Sidebar

* Application logo/name
* File upload
* Dashboard navigation
* Dataset information
* Cleaning options
* Visualization options
* AI insights
* Export options
* Settings
* Help/About

### Main Dashboard

Top section:

* Total Records
* Total Columns
* Missing Values
* Duplicate Rows
* Data Quality Score
* Numeric Columns
* Categorical Columns

Use attractive KPI cards.

The dashboard should have:

* responsive layout
* modern typography
* clean spacing
* professional cards
* interactive filters
* charts
* tabs
* expandable sections
* tooltips
* status indicators
* progress indicators

Make it look like a **real-world analytics platform used by clients**, not a beginner project.

---

# 4. Automatic Data Cleaning Engine

Create a reusable data-cleaning engine.

It should automatically detect and handle:

### Missing Values

Detect missing values and provide strategies such as:

* mean
* median
* mode
* forward fill
* backward fill
* constant value
* remove rows
* remove columns when appropriate

### Duplicate Data

Detect:

* fully duplicated rows
* duplicated IDs
* duplicated records

Show duplicate statistics before and after cleaning.

### Incorrect Data Types

Automatically detect and convert:

* strings → dates
* strings → numbers
* numbers stored as text
* boolean-like fields
* categorical columns

### Invalid Values

Detect:

* negative prices
* impossible ages
* invalid percentages
* impossible dates
* empty strings
* whitespace
* inconsistent capitalization
* invalid categories

### Text Cleaning

Perform:

* trim whitespace
* lowercase/uppercase normalization
* duplicate category cleanup
* spelling/inconsistency detection where possible
* special-character handling

### Date Cleaning

Detect and standardize date formats.

Support formats such as:

* DD-MM-YYYY
* MM-DD-YYYY
* YYYY-MM-DD
* timestamps

Automatically create useful date features where appropriate:

* Year
* Quarter
* Month
* Month Name
* Week
* Day
* Day Name

### Outlier Detection

Implement multiple methods:

* IQR
* Z-score
* percentile-based detection

Allow the user to choose:

* Keep outliers
* Remove outliers
* Cap/Winsorize outliers

Clearly show what happened.

---

# 5. Data Quality Score

Create an intelligent **Data Quality Score from 0–100**.

The score should consider:

* missing values
* duplicates
* invalid values
* incorrect data types
* outliers
* inconsistent categories

Show:

**Before Cleaning Score**

and

**After Cleaning Score**

Provide a breakdown explaining how the score was calculated.

Example:

Data Quality Score: 87/100

Missing values: 94%

Duplicate quality: 100%

Data type quality: 90%

Consistency: 85%

Outlier quality: 75%

---

# 6. Automated Column Intelligence

Automatically classify columns into:

* ID
* Numeric
* Categorical
* Date
* Boolean
* Text
* Currency
* Percentage
* Geographic
* Target variable
* Potential metric
* Potential dimension

Do not require users to manually configure everything.

For example:

```text
customer_id → ID
sales → Numeric/Currency
order_date → Date
region → Categorical
profit → Numeric/Currency
country → Geographic
```

---

# 7. Automated KPI Generator

Automatically detect useful metrics based on the uploaded dataset.

Examples:

### Sales Data

* Total Sales
* Total Profit
* Average Order Value
* Total Orders
* Quantity Sold
* Profit Margin
* Best Product
* Best Region
* Best Customer

### HR Data

* Total Employees
* Average Salary
* Attrition Rate
* Average Age
* Department Count

### E-commerce

* Orders
* Revenue
* Average Basket Size
* Conversion-related metrics where possible

### Finance

* Revenue
* Expenses
* Profit
* Growth
* ROI

The application should intelligently determine which KPIs make sense for the available columns.

Do not display meaningless KPIs.

---

# 8. Automatic Visualization Engine

Automatically generate relevant charts based on detected column types.

Possible charts:

* Bar Chart
* Line Chart
* Area Chart
* Pie Chart
* Donut Chart
* Histogram
* Box Plot
* Scatter Plot
* Heatmap
* Correlation Matrix
* Treemap
* Funnel Chart
* Geographic visualization
* Time-series charts

Example logic:

```text
Date + Numeric
→ Time Series

Category + Numeric
→ Bar Chart

Category + Category
→ Count Chart

Numeric + Numeric
→ Scatter Plot

Numeric
→ Histogram

Multiple Numeric columns
→ Correlation Heatmap
```

Allow users to manually create custom visualizations as well.

---

# 9. Interactive Dashboard Filters

Add dynamic filters such as:

* Date Range
* Category
* Region
* Product
* Department
* Customer
* Country

Filters should automatically adapt to the uploaded dataset.

All charts and KPIs should update based on filters.

---

# 10. AI-Powered Insights

Add an optional AI insights module.

The system should analyze the cleaned dataset and generate human-readable insights such as:

* major trends
* unusual patterns
* top-performing categories
* declining categories
* highest revenue contributors
* low-performing segments
* correlations
* anomalies
* business recommendations

Example:

> "Sales increased by 18% in Q3 compared with Q2, mainly driven by the Electronics category."

The AI component should never invent facts that are not supported by the dataset.

If an external LLM API is used:

* use environment variables
* provide `.env.example`
* provide fallback mode when API is unavailable
* do not expose credentials

---

# 11. Statistical Analysis

Add a dedicated statistics section.

Include where applicable:

* Mean
* Median
* Mode
* Standard Deviation
* Variance
* Minimum
* Maximum
* Percentiles
* Skewness
* Kurtosis
* Correlation
* Distribution analysis

Automatically select useful statistics.

---

# 12. Data Profiling

Create an automatic data profiling page showing:

* Dataset size
* Column names
* Data types
* Missing values
* Unique values
* Duplicate values
* Memory usage
* Cardinality
* Numeric summary
* Categorical summary

Create a visual data-quality report.

---

# 13. Before vs After Cleaning

Create a dedicated comparison page.

Show:

```text
                  BEFORE       AFTER
Rows               10,000      9,870
Columns               15         15
Missing Values        420          0
Duplicates            130          0
Invalid Dates          21          0
Data Quality          61%        96%
```

Also show visual comparisons.

---

# 14. Smart Recommendations

Based on data quality and analytics, provide recommendations.

Example:

```text
Recommendation 1
The "customer_email" column contains 8% invalid email values.

Recommendation 2
The "revenue" column contains extreme outliers that should be reviewed.

Recommendation 3
The "region" column contains inconsistent category names.
```

Use priority levels:

* Critical
* High
* Medium
* Low
* Informational

---

# 15. File Management

The application should allow:

* Upload Excel
* Upload CSV
* Multiple file upload
* Excel sheet selection
* Preview data
* Download cleaned Excel
* Download cleaned CSV
* Download dashboard report
* Download summary report

Support large files as safely as possible and provide clear error messages.

---

# 16. Multiple Dataset Support

Add the ability to upload multiple datasets.

Example:

```text
customers.xlsx
orders.csv
products.xlsx
```

Allow users to:

* inspect each dataset
* clean each dataset
* identify possible join keys
* optionally merge datasets

Example:

```text
customers.customer_id
orders.customer_id
```

Suggest possible relationships.

---

# 17. Data Joining / Merging

Create a visual interface for merging datasets.

Support:

* Inner Join
* Left Join
* Right Join
* Outer Join

Allow users to select:

* left dataset
* right dataset
* join column
* join type

Show a preview before applying.

---

# 18. Export / Reporting

Create professional export functionality.

Generate:

### Excel Report

Include:

* cleaned dataset
* data quality report
* statistics
* summary
* KPI values

### PDF Report

Include:

* project title
* dataset summary
* data quality score
* cleaning operations
* KPIs
* charts
* insights
* recommendations

### CSV

Export cleaned data.

---

# 19. Client Sharing

The application must be designed so that a client can open the shared URL and use the dashboard without needing to understand Python.

Create:

* welcome page
* onboarding instructions
* clean UI
* help section
* sample dataset
* demo mode
* download templates

Create a **Demo Dashboard** that works without uploading a file.

---

# 20. Demo Mode

Provide a built-in demo dataset such as:

```text
Sales Dashboard Demo
```

Include realistic sample data with:

* Date
* Product
* Category
* Region
* Customer
* Quantity
* Sales
* Cost
* Profit

The demo dashboard should immediately show a complete professional dashboard.

---

# 21. Advanced Features

Add these features where practical:

### Smart Auto Dashboard

One click:

**"Generate Dashboard"**

Automatically:

1. Analyze dataset
2. Clean dataset
3. Detect data types
4. Detect KPIs
5. Detect dimensions
6. Generate charts
7. Generate insights
8. Generate recommendations

### Dashboard Customization

Allow users to customize:

* dashboard title
* logo
* filters
* visible KPIs
* chart selection
* chart order

### Theme

Support:

* Light Mode
* Dark Mode

### Session Management

Maintain uploaded dataset and analysis within the user's session.

### Error Handling

Never allow the application to crash because of bad user input.

Use friendly messages such as:

> "The uploaded file could not be processed. Please verify that the file contains a valid table."

---

# 22. Security

Implement reasonable security practices.

Never:

* hard-code API keys
* expose secrets
* store private uploaded data unnecessarily
* execute arbitrary user code
* trust file names or file extensions blindly

Validate uploads and handle malicious/invalid files safely.

---

# 23. Performance

Optimize the application using:

* Streamlit caching
* efficient Pandas operations
* lazy calculations where possible
* modular functions
* efficient file processing

Avoid recalculating expensive operations unnecessarily.

---

# 24. Project Architecture

Create a professional project structure similar to:

```text
global-data-analytics-platform/
│
├── app.py
├── requirements.txt
├── README.md
├── Dockerfile
├── .gitignore
├── .env.example
│
├── config/
│   └── settings.py
│
├── components/
│   ├── sidebar.py
│   ├── navbar.py
│   ├── kpi_cards.py
│   ├── charts.py
│   ├── filters.py
│   └── ui.py
│
├── core/
│   ├── data_loader.py
│   ├── data_cleaner.py
│   ├── data_profiler.py
│   ├── data_quality.py
│   ├── column_detector.py
│   ├── kpi_engine.py
│   ├── visualization_engine.py
│   ├── insight_engine.py
│   ├── recommendation_engine.py
│   └── merge_engine.py
│
├── pages/
│   ├── dashboard.py
│   ├── data_cleaning.py
│   ├── profiling.py
│   ├── statistics.py
│   ├── insights.py
│   ├── reports.py
│   └── settings.py
│
├── utils/
│   ├── helpers.py
│   ├── validators.py
│   ├── exporters.py
│   └── logger.py
│
├── assets/
│   ├── logo.png
│   └── sample_data/
│
└── tests/
    ├── test_cleaning.py
    ├── test_quality.py
    ├── test_kpis.py
    └── test_loader.py
```

You may improve this architecture when appropriate.

---

# 25. Code Quality

Write clean, modular, reusable Python.

Use:

* functions
* classes where useful
* type hints
* docstrings
* exception handling
* logging
* validation

Avoid putting the entire application into one huge Python file.

Every major feature should be separated into modules.

---

# 26. Recommended Technologies

Use Python technologies such as:

* Streamlit
* Pandas
* NumPy
* Plotly
* OpenPyXL
* PyArrow
* SciPy
* Scikit-learn
* ReportLab
* python-dotenv

Use additional libraries when they provide a clear benefit.

Prefer **Plotly** for interactive charts.

---

# 27. Professional UI Requirement

Use custom Streamlit CSS carefully to achieve a modern SaaS appearance.

The dashboard should visually resemble products such as:

* modern BI platforms
* SaaS analytics platforms
* enterprise dashboards

Do NOT make it look like:

```text
basic Streamlit widgets stacked vertically
```

Instead use:

* cards
* sections
* columns
* tabs
* containers
* modern navigation
* visual hierarchy
* responsive layouts

---

# 28. User Workflow

The ideal workflow should be:

```text
Home
 ↓
Upload Dataset
 ↓
Data Validation
 ↓
Data Quality Scan
 ↓
Automatic Cleaning
 ↓
Data Profiling
 ↓
Generate Dashboard
 ↓
KPI Dashboard
 ↓
Visual Analytics
 ↓
AI Insights
 ↓
Recommendations
 ↓
Export Report
```

Make the workflow extremely easy for a non-technical user.

---

# 29. Sample Data Cleaning Scenarios

Include sample datasets containing intentionally bad data so the application can demonstrate its capabilities.

Examples:

* missing values
* duplicates
* invalid dates
* inconsistent categories
* incorrect data types
* whitespace
* outliers
* invalid numbers

The application should correctly clean these datasets.

---

# 30. Dashboard Screenshot Requirement

I will provide you with **reference screenshots of the type of dashboard design I want**.

When I upload the screenshots:

1. Analyze the visual structure.
2. Identify the layout.
3. Identify cards and sections.
4. Identify colors.
5. Identify navigation style.
6. Identify chart placement.
7. Recreate the overall professional design in Streamlit.
8. Do not blindly copy branding or copyrighted assets.
9. Improve the design where appropriate.

The final application should visually feel similar to the reference while remaining an original implementation.

---

# 31. Global Product-Level Improvements

Do not simply implement the features mentioned above.

Think like a **senior product engineer** and add useful improvements that would make this application more valuable as a global product.

Potential additions include:

* automatic dataset recommendations
* natural-language questions over data
* "Ask your Data" feature
* anomaly detection
* trend detection
* forecast module
* correlation discovery
* data dictionary generation
* automatic chart explanation
* smart column recommendations
* report templates
* dashboard templates
* branding customization
* sample datasets
* data validation rules
* downloadable audit logs
* cleaning history
* undo/redo cleaning operations
* configurable cleaning settings

Only add features that are technically practical and keep the application stable.

---

# 32. Ask Your Data Feature

Add an optional natural-language analytics interface.

Example:

```text
User:
"What was the highest-selling product?"

System:
"Laptop generated the highest sales with ₹12.4 lakh."

User:
"Show monthly sales for 2026."

System:
"Generating monthly sales trend..."
```

The system must calculate answers from the uploaded dataset rather than hallucinating.

---

# 33. Forecasting Module

When the uploaded dataset contains a usable date/time column and numerical metric, optionally provide:

* trend analysis
* moving average
* forecasting
* seasonality analysis

Do not force forecasting when the dataset is unsuitable.

---

# 34. Anomaly Detection

Add automatic anomaly detection for relevant numeric data.

Show:

* anomaly count
* anomaly percentage
* affected rows
* affected metrics
* visualization

Use appropriate algorithms such as:

* IQR
* Z-score
* Isolation Forest where useful

Explain anomalies clearly.

---

# 35. README

Create a detailed README containing:

* project overview
* features
* screenshots section
* installation
* local setup
* environment variables
* running the application
* deployment to Streamlit Cloud
* Docker deployment
* project structure
* usage guide
* troubleshooting
* future improvements

---

# 36. Deployment

The final project must include exact commands.

For local development:

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
streamlit run app.py
```

Also provide Docker instructions.

---

# 37. Final Deliverable

I want the final result to be a **complete runnable project**, not a partial example.

Generate:

```text
1. Full source code
2. Complete folder structure
3. requirements.txt
4. README.md
5. Dockerfile
6. .env.example
7. Sample datasets
8. Tests
9. Professional UI
10. Automatic cleaning engine
11. Dashboard generator
12. KPI engine
13. Visualization engine
14. AI insights
15. Export functionality
16. Client sharing support
17. Demo mode
18. Deployment documentation
```

The project must run with:

```bash
streamlit run app.py
```

without requiring unnecessary manual code changes.

---

# 38. Important Development Rule

Before writing the final implementation, think through:

* architecture
* dependencies
* data flow
* user flow
* error handling
* performance
* security
* deployment
* scalability

Then implement the complete solution.

Do not give me only pseudo-code.

Do not give me incomplete files.

Do not replace important functionality with comments such as:

```python
# implement this later
```

Every major feature should have working code.

When a feature requires an external API, provide both:

1. API-enabled implementation
2. fallback implementation without the API

so the application remains usable.

---

# 39. Final Goal

The final product should feel like:

> **A global AI-powered data cleaning and business intelligence platform where any user can upload messy Excel/CSV data and instantly receive a clean dataset, professional dashboard, KPIs, visualizations, insights, anomaly detection, recommendations, and downloadable reports.**

Build it with **Streamlit**, but make the result look and behave like a **professional commercial SaaS analytics product** rather than a simple Streamlit project.

After implementation, provide the complete project in a **ZIP file** with all source code, assets, sample data, configuration, tests, and documentation included.
