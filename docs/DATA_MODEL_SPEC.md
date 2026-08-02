# Data Model & Schema Specification

```text
                  ┌────────────────────────┐
                  │      dim_dates         │
                  └───────────┬────────────┘
                              │
                              ▼
┌──────────────────┐    ┌─────────────────────────┐    ┌──────────────────┐
│  dim_companies   │───►│  fact_funding_rounds    │◄───│  dim_investors   │
└──────────────────┘    └─────────────────────────┘    └──────────────────┘
                              ▲
                              │
                  ┌────────────────────────┐
                  │ fact_runway_estimates  │
                  └────────────────────────┘
```

## 1. Core Warehouse Entities (BigQuery Marts)

### Dimensions

- **`dim_companies`**: `company_id` (PK), `company_name`, `industry_sector`, `company_status`, `country_code`, `founded_date`.
- **`dim_investors`**: `investor_id` (PK), `investor_name`, `investor_type`.
- **`dim_dates`**: `date_id` (PK), `year`, `quarter`, `month_name`.

### Fact Tables

- **`fact_funding_rounds`**: `fact_round_id` (PK), `company_id` (FK), `investor_id` (FK), `funded_date` (FK), `round_stage`, `raised_amount_usd`, `months_since_last_round`.
- **`fact_runway_estimates`**: `company_id` (FK), `last_funding_date`, `total_capital_raised_usd`, `estimated_monthly_burn_usd`, `estimated_runway_months`, `runway_risk_flag` (High Risk: <6 mo, Medium Risk: 6–12 mo, Low Risk: >12 mo).

---

## 2. API Data Transfer Objects (Pydantic Schemas)

These schemas map BigQuery mart outputs into clean JSON payloads for the Next.js frontend:

```python
from datetime import date
from typing import Literal
from pydantic import BaseModel

class StartupRiskSummary(BaseModel):
    company_id: str
    company_name: str
    industry_sector: str
    last_funding_date: date
    total_capital_raised_usd: float
    estimated_runway_months: float
    runway_risk_flag: Literal["High Risk", "Medium Risk", "Low Risk"]
```
