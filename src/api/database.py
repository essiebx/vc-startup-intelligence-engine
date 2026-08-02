"""Database client helper for Google BigQuery and local Data Warehouse."""

import os
import sqlite3
from typing import Optional
from google.cloud import bigquery
from src.config import settings

_bq_client: Optional[bigquery.Client] = None


def get_bigquery_client() -> Optional[bigquery.Client]:
    """Returns a Google BigQuery client instance or None if unconfigured."""
    global _bq_client
    if _bq_client is not None:
        return _bq_client

    key_path = settings.GOOGLE_APPLICATION_CREDENTIALS
    if os.path.exists(key_path):
        try:
            _bq_client = bigquery.Client.from_service_account_json(key_path)
            return _bq_client
        except Exception as e:
            print(f"Warning: Failed to initialize BigQuery client from {key_path}: {e}")
            return None

    try:
        _bq_client = bigquery.Client(project=settings.GCP_PROJECT_ID)
        return _bq_client
    except Exception:
        return None


def get_local_db_connection(db_path: str = "data/warehouse.db") -> Optional[sqlite3.Connection]:
    """Returns SQLite database connection to local warehouse if present."""
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn
    return None
