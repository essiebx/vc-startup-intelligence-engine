"""Stage 4: Data Warehouse Modeling & SQL Transformations Orchestrator."""

import os
import sys
import sqlite3
import pandas as pd
from pathlib import Path

# Add project root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from src.config import settings


def run_warehouse_transformations(db_path: str = "data/warehouse.db"):
    """Executes SQL transformations building dimension tables, fact tables, and analytical marts.

    Args:
        db_path: Path to SQLite staging & warehouse database.
    """
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Staging database not found at {db_path}. Run Stage 3 ingestion first.")

    print(f"Connecting to data warehouse at '{db_path}'...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 1. Build Dimension Table: dim_startups
    print("Building Dimension Table: 'dim_startups'...")
    cursor.execute("DROP TABLE IF EXISTS dim_startups;")
    dim_query = """
    CREATE TABLE dim_startups AS
    SELECT
        startup_id,
        company_name,
        COALESCE(industry, 'Unspecified') AS industry,
        COALESCE(country, 'Unknown') AS country,
        city,
        status,
        founded_at AS founded_date,
        STRFTIME('%Y', founded_at) AS founded_year,
        DATETIME('now') AS created_at
    FROM stg_startups;
    """
    cursor.execute(dim_query)

    # 2. Build Fact Table: fact_funding_rounds
    print("Building Fact Table: 'fact_funding_rounds'...")
    cursor.execute("DROP TABLE IF EXISTS fact_funding_rounds;")
    fact_funding_query = """
    CREATE TABLE fact_funding_rounds AS
    SELECT
        startup_id || '_r' || CAST(funding_rounds AS TEXT) AS round_id,
        startup_id,
        last_funding_at AS round_date,
        funding_rounds AS round_number,
        total_funding_usd AS amount_raised_usd
    FROM stg_startups
    WHERE total_funding_usd > 0;
    """
    cursor.execute(fact_funding_query)

    # 3. Build Analytical Mart: fact_runway_risk
    print("Building Analytical Mart: 'fact_runway_risk'...")
    cursor.execute("DROP TABLE IF EXISTS fact_runway_risk;")
    runway_mart_query = """
    CREATE TABLE fact_runway_risk AS
    WITH metrics_prep AS (
        SELECT
            startup_id,
            company_name,
            industry,
            country,
            status,
            total_funding_usd AS total_capital_raised_usd,
            estimated_monthly_burn_usd,
            last_funding_at AS last_funding_date,
            CAST(
                MAX(0, (julianday('now') - julianday(COALESCE(last_funding_at, '2024-01-01'))) / 30.4375)
                AS INTEGER
            ) AS months_since_last_raise,
            (total_funding_usd * 0.70) AS estimated_cash_reserve_usd
        FROM stg_startups
    ),
    runway_calc AS (
        SELECT
            startup_id,
            company_name,
            industry,
            country,
            status,
            total_capital_raised_usd,
            estimated_monthly_burn_usd,
            last_funding_date,
            months_since_last_raise,
            estimated_cash_reserve_usd,
            ROUND(
                MAX(
                    0.0,
                    (estimated_cash_reserve_usd / CASE WHEN estimated_monthly_burn_usd > 0 THEN estimated_monthly_burn_usd ELSE 100000.0 END) - months_since_last_raise
                ),
                1
            ) AS runway_months
        FROM metrics_prep
    )
    SELECT
        startup_id,
        company_name,
        industry,
        country,
        status,
        total_capital_raised_usd,
        estimated_monthly_burn_usd,
        last_funding_date,
        months_since_last_raise,
        estimated_cash_reserve_usd,
        runway_months,
        CASE
            WHEN runway_months < 6.0 THEN 'High'
            WHEN runway_months BETWEEN 6.0 AND 12.0 THEN 'Medium'
            ELSE 'Low'
        END AS risk_level,
        DATETIME('now') AS calculated_at
    FROM runway_calc;
    """
    cursor.execute(runway_mart_query)
    conn.commit()

    # Verify Mart Row Count and Risk Distribution
    df_risk = pd.read_sql_query(
        "SELECT risk_level, COUNT(*) as count, ROUND(AVG(runway_months), 1) as avg_runway FROM fact_runway_risk GROUP BY risk_level",
        conn
    )
    conn.close()

    print("\nWarehouse Transformations Completed Successfully!")
    print("Analytical Mart 'fact_runway_risk' Summary:")
    print(df_risk.to_string(index=False))


if __name__ == "__main__":
    db_file = "data/warehouse.db"
    run_warehouse_transformations(db_file)
