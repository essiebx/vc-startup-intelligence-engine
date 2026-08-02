
# 🏎️ VC Startup Intelligence Engine

An end-to-end analytical platform and early-warning runway risk detector built for Venture Capital investment and portfolio support teams.

![Architecture Overview](https://img.shields.io/badge/Architecture-Full--Stack%20Data-blue)
![Stack](https://img.shields.io/badge/Stack-BigQuery%20%7C%20FastAPI%20%7C%20Next.js%20%7C%20Power%20BI-green)

---

##  Executive Summary

Venture capital firms evaluate thousands of startups yearly while simultaneously monitoring portfolio cash runway. Manual tracking leads to late detection of distressed portfolio startups and missed investment opportunities.

This platform automates data ingestion, models runway risk in **Google BigQuery**, exposes REST endpoints via **FastAPI**, presents an interactive web cockpit with **Next.js & Tremor UI**, and delivers strategic metrics in **Power BI**.

---

##  System Architecture

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. DATA INGESTION (Python)                                                 │
│ Raw Kaggle/Crunchbase CSVs ──► Pandas Clean & Parse ──► BigQuery Staging    │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 2. WAREHOUSE & ANALYTICS (Google BigQuery)                                  │
│ Staging (`stg_*`) ──► SQL Star Schema Marts ──► Fact & Dimension Tables     │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 3. API SERVICE LAYER (FastAPI Engine)                                       │
│ BigQuery Client ──► Pydantic Data Validation ──► REST Endpoints             │
└──────────────────┬──────────────────────────────────────┬───────────────────┘
                   │                                      │
                   ▼                                      ▼
┌────────────────────────────────────┐  ┌────────────────────────────────────┐
│ 4A. WEB FRONTEND (Next.js/Tremor)  │  │ 4B. EXECUTIVE BI (Power BI)        │
│ Interactive Risk & Sourcing UI     │  │ Partner-Level Reporting Dashboard  │
└────────────────────────────────────┘  └────────────────────────────────────┘
## Overview

This project ingests startup data, models runway risk in BigQuery, exposes REST endpoints via FastAPI, and provides a Next.js frontend and Power BI reporting.

Tech stack: Python (pandas, google-cloud-bigquery), BigQuery, FastAPI, Next.js (TypeScript), Power BI.
#  VC Startup Intelligence Engine

An end-to-end analytical platform and early-warning runway risk detector built for Venture Capital investment and portfolio support teams.

![Architecture Overview](https://img.shields.io/badge/Architecture-Full--Stack%20Data-blue)
![Stack](https://img.shields.io/badge/Stack-BigQuery%20%7C%20FastAPI%20%7C%20Next.js%20%7C%20Power%20BI-green)



## Quickstart

1. Clone / create locally
2. Create a Python venv, install dependencies:
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

3. Configure environment variables (example `.env`):
   GCP_PROJECT_ID=your_gcp_project_id
   GOOGLE_APPLICATION_CREDENTIALS=keys/gcp_service_account.json

4. Run FastAPI (development):
   uvicorn src.api.main:app --reload

## Runway formula

Runway (months) = (Total Capital Raised * 0.70) / Estimated Monthly Burn - Months Since Last Raise

Risk:
- High: < 6 months
- Medium: 6–12 months
- Low: > 12 months

## Repo layout

vc-startup-intelligence-engine/
├── docs/
├── data/           # local raw datasets (gitignored)
├── keys/           # GCP keys (gitignored)
├── src/
│   ├── api/
│   │   └── main.py
│   └── ingest_crunchbase.py
├── sql/
├── frontend/
└── power_bi/

License: MIT (example) — change as desired.
