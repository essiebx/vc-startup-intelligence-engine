# VC Startup Intelligence Engine

An end-to-end analytical platform and early-warning runway risk detector built for Venture Capital investment and portfolio support teams.

![Architecture Overview](https://img.shields.io/badge/Architecture-Full--Stack%20Data-blue)
![Stack](https://img.shields.io/badge/Stack-BigQuery%20%7C%20FastAPI%20%7C%20Next.js%20%7C%20Power%20BI-green)

---

## Executive Summary

Venture capital firms evaluate thousands of startups yearly while monitoring portfolio cash runway. Manual tracking leads to late detection of distressed portfolio startups and missed investment opportunities.

This platform automates data ingestion, models runway risk in **Google BigQuery**, exposes REST endpoints via **FastAPI**, presents an interactive web cockpit with **Next.js & Tailwind CSS**, and delivers strategic metrics in **Power BI**.

---

## System Architecture

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
│ 4A. WEB FRONTEND (Next.js/Tailwind)│  │ 4B. EXECUTIVE BI (Power BI)        │
│ Interactive Risk & Sourcing UI     │  │ Partner-Level Reporting Dashboard  │
└────────────────────────────────────┘  └────────────────────────────────────┘
```

---

## Quickstart

### 1. Environment & Dependencies

```bash
# Create Python virtual environment
python -m venv venv

# Activate environment (Windows)
.\venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### 2. Configuration

Copy `.env.example` to `.env` and set your GCP credentials:

```ini
GCP_PROJECT_ID=your_gcp_project_id
GCP_DATASET_ID=vc_intelligence_ds
GOOGLE_APPLICATION_CREDENTIALS=keys/gcp_service_account.json
```

### 3. Run FastAPI Backend

```bash
uvicorn src.api.main:app --reload
```

### 4. Run Next.js Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## Runway Calculation Formula

$$\text{Runway (Months)} = \max\left(0, \frac{\text{Total Capital Raised} \times 0.70}{\text{Estimated Monthly Burn}} - \text{Months Since Last Raise}\right)$$

### Risk Categories
- **High Risk**: `< 6` months remaining
- **Medium Risk**: `6 - 12` months remaining
- **Low Risk**: `> 12` months remaining

---

## Repository Layout

```text
vc-startup-intelligence-engine/
├── docs/                 # Platform PRD, TRD, Data Model specs
├── data/                 # Raw and processed datasets (gitignored)
├── keys/                 # GCP service account keys (gitignored)
├── sql/                  # BigQuery DDL staging, dimensions, and facts
├── src/
│   ├── api/              # FastAPI server, schemas, and routes
│   └── ingestion/        # Pandas ETL pipeline and BigQuery loader
├── frontend/             # Next.js App Router TypeScript dashboard
├── power_bi/             # Power BI schema mapping & connection guide
└── requirements.txt      # Python dependencies
```

---

## License

MIT License.
