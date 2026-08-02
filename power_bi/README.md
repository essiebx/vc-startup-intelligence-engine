# Power BI Integration Guide

This directory contains configuration templates for connecting **Power BI Desktop** to the **VC Startup Intelligence Engine**.

## Data Source Setup

### Method A: Direct BigQuery Connector (Recommended)

1. Open **Power BI Desktop**.
2. Click **Get Data** -> **More...** -> **Database** -> **Google BigQuery**.
3. Select **Sign in** with your GCP Organizational Account or Service Account.
4. Input your `GCP_PROJECT_ID` and dataset name `vc_intelligence_ds`.
5. Select the table `fact_runway_risk` and click **Load** or **Transform Data**.

### Method B: REST API Connector (Web Source)

1. Click **Get Data** -> **Web**.
2. URL: `http://localhost:8000/api/v1/metrics/runway-summary` (or production endpoint).
3. Use JSON parser to expand record tables.

## Recommended Visualizations

1. **High Risk Alert KPI Card**: Filter `risk_level = 'High'`.
2. **Runway Months Distribution**: Clustered column chart (`runway_months` grouped into buckets vs `company_name`).
3. **Burn vs Capital Raised Matrix**: Scatter plot with `total_capital_raised_usd` (X-axis) vs `estimated_monthly_burn_usd` (Y-axis), colored by `risk_level`.
