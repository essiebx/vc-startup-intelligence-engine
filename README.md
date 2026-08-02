# VC Startup Intelligence Engine

An end-to-end analytical platform and early-warning runway risk detector built for Venture Capital investment and portfolio support teams.

## Overview

This project ingests startup data, models runway risk in BigQuery, exposes REST endpoints via FastAPI, and provides a Next.js frontend and Power BI reporting.

Tech stack: Python (pandas, google-cloud-bigquery), BigQuery, FastAPI, Next.js (TypeScript), Power BI.

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
