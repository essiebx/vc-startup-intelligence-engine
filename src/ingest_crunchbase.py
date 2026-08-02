"""Production Crunchbase & Startup Ingestion Script.

Modularized cleaning logic tested in notebooks/01_exploratory_data_analysis.ipynb.
Automates dataset parsing, cleaning, and ingestion into BigQuery / Staging warehouse.
"""

import os
import sys
import pandas as pd
import numpy as np
from pathlib import Path

# Add project root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.config import settings


def clean_raw_startup_data(df_raw: pd.DataFrame) -> pd.DataFrame:
    """Modularized cleaning function tested in 01_exploratory_data_analysis.ipynb.

    Args:
        df_raw: Raw DataFrame loaded from CSV.

    Returns:
        Cleaned & standardized pandas DataFrame.
    """
    df = df_raw.copy()

    # Column header standardization & mapping
    col_map = {
        "startup_name": "company_name",
        "funding_amount_usd": "total_funding_usd",
        "funding_date": "last_funding_at",
        "region": "city",
        "country": "country_code",
    }
    df.rename(columns={k: v for k, v in col_map.items() if k in df.columns}, inplace=True)

    # Standardize string fields
    df["startup_id"] = df["startup_id"].astype(str).str.strip()
    df["company_name"] = df.get("company_name", df.get("name", "Unknown")).fillna("Unknown").astype(str).str.strip()
    df["industry"] = df.get("industry", df.get("category_list", "Unspecified")).fillna("Unspecified").astype(str).str.strip()
    df["country"] = df.get("country_code", "Unknown").fillna("Unknown").astype(str).str.upper().str.strip()
    df["city"] = df.get("city", "Unknown").fillna("Unknown").astype(str).str.strip()

    # Derive operating status from exit_type & exited flags
    def derive_status(row):
        exit_t = row.get("exit_type")
        if pd.notna(exit_t) and str(exit_t).strip() != "":
            return str(exit_t).strip().lower()
        if str(row.get("exited")).lower() in ["true", "1"]:
            return "acquired"
        status_v = row.get("status")
        if pd.notna(status_v) and str(status_v).strip() != "":
            return str(status_v).strip().lower()
        return "operating"

    df["status"] = df.apply(derive_status, axis=1)

    # Numeric transformations
    df["total_funding_usd"] = pd.to_numeric(df.get("total_funding_usd", 0), errors="coerce").fillna(0.0)
    df["funding_rounds"] = pd.to_numeric(df.get("funding_round", 1), errors="coerce").fillna(1).astype(int)

    # Monthly burn estimation (~$12k / employee / mo)
    if "estimated_monthly_burn_usd" in df.columns and df["estimated_monthly_burn_usd"].notna().any():
        df["estimated_monthly_burn_usd"] = pd.to_numeric(df["estimated_monthly_burn_usd"], errors="coerce").fillna(100000.0)
    else:
        emp_count = pd.to_numeric(df.get("employee_count", 15), errors="coerce").fillna(15)
        df["estimated_monthly_burn_usd"] = (emp_count * 12000.0).clip(lower=50000.0, upper=2000000.0)

    # Date parsing
    if "founded_at" in df.columns and df["founded_at"].notna().any():
        df["founded_at"] = pd.to_datetime(df["founded_at"], errors="coerce").dt.strftime("%Y-%m-%d")
    elif "founded_year" in df.columns and df["founded_year"].notna().any():
        df["founded_at"] = pd.to_datetime(df["founded_year"].astype(str) + "-01-01", errors="coerce").dt.strftime("%Y-%m-%d")
    else:
        df["founded_at"] = "2020-01-01"

    df["last_funding_at"] = pd.to_datetime(df.get("last_funding_at"), errors="coerce").dt.strftime("%Y-%m-%d")

    # Final cleaned columns selection
    cleaned_df = df[[
        "startup_id", "company_name", "industry", "country", "city",
        "status", "founded_at", "funding_rounds", "total_funding_usd",
        "last_funding_at", "estimated_monthly_burn_usd"
    ]]
    return cleaned_df


def run_crunchbase_ingestion(raw_csv_path: str, output_csv_path: str = "data/processed/clean_startups.csv"):
    """Automates reading, cleaning, and staging ingestion.

    Args:
        raw_csv_path: Local filesystem path to raw CSV file.
        output_csv_path: Local filesystem path to write processed CSV.
    """
    if not os.path.exists(raw_csv_path):
        raise FileNotFoundError(f"Raw CSV dataset not found at {raw_csv_path}")

    print(f"Reading raw Crunchbase / Startup dataset: '{raw_csv_path}'...")
    df_raw = pd.read_csv(raw_csv_path)

    print(f"Cleaning & standardizing {len(df_raw):,} records...")
    df_clean = clean_raw_startup_data(df_raw)

    # Save cleaned CSV
    Path(output_csv_path).parent.mkdir(parents=True, exist_ok=True)
    df_clean.to_csv(output_csv_path, index=False)
    print(f"Successfully processed {len(df_clean):,} rows. Exported to '{output_csv_path}'.")

    # Automate BigQuery / Local Staging Ingestion
    from src.ingestion.ingest_to_staging import ingest_to_staging
    ingest_to_staging(output_csv_path)


if __name__ == "__main__":
    raw_path = "data/raw/startup_valuation_dataset.csv"
    if not os.path.exists(raw_path):
        raw_path = "data/raw/crunchbase_startups.csv"
    
    if os.path.exists(raw_path):
        run_crunchbase_ingestion(raw_path)
    else:
        print(f"Sample script ready. Place raw CSV in 'data/raw/' to execute.")
