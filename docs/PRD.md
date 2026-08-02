# Product Requirement Document (PRD)

## 1. Executive Summary & Business Context

**Organization**: Y Combinator (Investment & Portfolio Support Team)

**Problem**: VC partners and portfolio leads need to monitor startup health, detect runway risk, and spot high-growth investment candidates early.

**Solution**: A full-stack Startup Survival & Deal Sourcing Intelligence Platform consisting of:
- An ETL ingestion pipeline storing raw data in Google BigQuery.
- SQL analytics marts identifying high-risk startups and stage transition rates.
- A FastAPI REST Service delivering real-time metrics to web applications.
- A Next.js + Tailwind CSS web frontend for interactive deal sourcing.
- A Power BI executive cockpit for partner-level reporting.

---

## 2. User Personas & System Touchpoints

| Persona | Primary Goal | System Touchpoint |
| :--- | :--- | :--- |
| **Venture Analyst** | Rapidly filter and inspect individual startup profiles and cash-out estimates. | Interactive Next.js Web App |
| **Investment Partner** | Identify sector trends, valuation step-ups, and top deal candidates. | Next.js Dashboard & Power BI |
| **Portfolio Support Lead** | Receive automated risk alerts for startups with <6 months of runway. | Power BI Cockpit & API Alerts |

---

## 3. Technical Scope (Full-Stack)

- **Data Ingestion**: Local CSV extraction, schema validation, and loading via Python (pandas/polars) into BigQuery staging.
- **Data Warehouse**: BigQuery Star Schema (`dim_`, `fact_`) with window functions calculating runway estimates and round intervals.
- **API Layer**: FastAPI REST API providing structured JSON endpoints (`/api/v1/startups`, `/api/v1/metrics/runway-summary`).
- **Frontend Web App**: Next.js (App Router), TypeScript, Tailwind CSS visual components.
- **Executive BI**: Power BI dashboard connected directly to BigQuery data marts.
