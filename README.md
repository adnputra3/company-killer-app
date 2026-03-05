Company Killer App Suite

A multipage Streamlit app for quick business operations and data workflows.

## Apps Included

1. **KPI Dashboard**
Monitor key business metrics in one place.

2. **Invoice Maker**
Create simple invoices and download them as text files.

3. **Data Analyst**
Upload CSV files, preview data, view summary statistics, and chart numeric columns.

4. **CSV Cleaner**
Upload CSV and standardize columns into this schema:
`date, category, revenue, orders, customers`

---

## Run Locally

### 1) Go to project folder
```bash
cd ~/projects/company-killer/A-kpi-dashboard
2) Create virtual environment
python3 -m venv .venv
3) Activate virtual environment
source .venv/bin/activate
4) Install dependencies
pip install streamlit pandas
5) Run app
python -m streamlit run app.py

Open in browser: http://localhost:8501
