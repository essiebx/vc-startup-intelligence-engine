# Technical Requirement Document (TRD) - Ingestion & API Layer

## 1. Data Ingestion & ETL Pipeline (`src/ingestion/`)

### Pipeline Architecture

```text
[ Raw CSV/JSON ] ──► [ Pandas Data Cleaner ] ──► [ Validation & Type Cast ] ──► [ BigQuery Staging ]
```

### Ingestion Logic Specification
1. **Extraction**:
   - Ingests raw data from Kaggle / Crunchbase dump files placed in `data/raw/`.
2. **Transformations**:
   - Standardizes header casing (`snake_case`).
   - Parses dates into standard ISO-8601 (`YYYY-MM-DD`).
   - Imputes missing currency and numeric fields with defensive default fallbacks.
   - Calculates initial month elapsed flags for runway estimation.
3. **BigQuery Batch Upload**:
   - Uses `google-cloud-bigquery` python client library.
   - Applies `WriteDisposition.WRITE_TRUNCATE` for staging table updates (`stg_startups`).

---

## 2. FastAPI REST Engine Specifications (`src/api/`)

### Base Configuration
- **Base URL**: `http://localhost:8000/api/v1`
- **Documentation**: `/docs` (Swagger UI), `/redoc` (ReDoc)

### Endpoint Signatures

#### A. Health Check
- `GET /health`
  - **Response**: `{"status": "healthy", "environment": "development", "gcp_project": "string"}`

#### B. Startups At Risk & Query Endpoint
- `GET /api/v1/startups`
  - **Query Parameters**:
    - `search` (optional `string`): Fuzzy search on `company_name` or `industry`.
    - `risk_level` (optional `string`): Filter by `"High"`, `"Medium"`, or `"Low"`.
    - `industry` (optional `string`): Filter by industry sector.
    - `page` (default `1`): Page number.
    - `page_size` (default `20`, max `100`): Items per page.
  - **Response Payload (`StartupListResponse`)**:
    ```json
    {
      "total_count": 42,
      "page": 1,
      "page_size": 20,
      "items": [
        {
          "company_id": "sup-002",
          "company_name": "QuantumPay Systems",
          "industry_sector": "Fintech",
          "country": "GBR",
          "status": "operating",
          "total_capital_raised_usd": 4200000.0,
          "estimated_monthly_burn_usd": 380000.0,
          "last_funding_date": "2023-08-10",
          "months_since_last_raise": 23,
          "estimated_cash_reserve_usd": 2940000.0,
          "estimated_runway_months": 4.7,
          "runway_risk_flag": "High"
        }
      ]
    }
    ```

#### C. Executive Metrics Summary
- `GET /api/v1/metrics/runway-summary`
  - **Response Payload (`RiskSummaryKPI`)**:
    ```json
    {
      "total_portfolio_startups": 150,
      "high_risk_count": 18,
      "medium_risk_count": 34,
      "low_risk_count": 98,
      "avg_runway_months": 14.2,
      "total_capital_deployed_usd": 420000000.0
    }
    ```

#### D. Dropdown Filter Options
- `GET /api/v1/metrics/filters`
  - **Response Payload**:
    ```json
    {
      "industries": ["Artificial Intelligence", "Fintech", "Healthcare", "CleanTech", "Cybersecurity"],
      "countries": ["USA", "GBR", "DEU", "ISR", "CAN"],
      "risk_levels": ["High", "Medium", "Low"]
    }
    ```
