"""Stage 3: Ingestion Pipeline - Staging Loader (Local DB & BigQuery)."""

import os
import sys
import sqlite3
import pandas as pd
from pathlib import Path

# Add project root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from src.config import settings


def ingest_to_staging(processed_csv_path: str, db_path: str = "data/warehouse.db"):
    """Ingests processed clean CSV data into staging database table (stg_startups).

    Args:
        processed_csv_path: Path to cleaned CSV.
        db_path: Local SQLite database file path.
    """
    if not os.path.exists(processed_csv_path):
        raise FileNotFoundError(f"Processed CSV dataset not found at {processed_csv_path}")

    print(f"Reading processed dataset from {processed_csv_path}...")
    df = pd.read_csv(processed_csv_path)

    # Ingest into local SQLite staging database for zero-config offline execution
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    
    print(f"Ingesting {len(df):,} records into local staging database '{db_path}' -> table 'stg_startups'...")
    df.to_sql("stg_startups", conn, if_exists="replace", index=False)
    conn.commit()
    conn.close()
    print("Local staging ingestion complete.")

    # Ingest into BigQuery staging if GCP credentials configured
    key_path = settings.GOOGLE_APPLICATION_CREDENTIALS
    if os.path.exists(key_path):
        try:
            from google.cloud import bigquery
            client = bigquery.Client.from_service_account_json(key_path)
            table_id = f"{settings.GCP_PROJECT_ID}.{settings.GCP_DATASET_ID}.stg_startups"
            
            job_config = bigquery.LoadJobConfig(
                source_format=bigquery.SourceFormat.CSV,
                skip_leading_rows=1,
                autodetect=True,
                write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
            )
            with open(processed_csv_path, "rb") as f:
                load_job = client.load_table_from_file(f, table_id, job_config=job_config)
            load_job.result()
            print(f"BigQuery staging ingestion complete: Loaded into '{table_id}'.")
        except Exception as e:
            print(f"Notice: BigQuery load skipped ({e}). Local staging is active.")


if __name__ == "__main__":
    proc_csv = "data/processed/clean_startups.csv"
    ingest_to_staging(proc_csv)
