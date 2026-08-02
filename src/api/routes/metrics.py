"""Metrics and Portfolio Risk Analytics Route Handler."""

from fastapi import APIRouter
from src.api.schemas import RiskSummaryKPI, FilterOptions
from src.api.database import get_bigquery_client, get_local_db_connection
from src.api.routes.startups import MOCK_STARTUPS
from src.config import settings

router = APIRouter(prefix="/metrics", tags=["Metrics & Analytics"])


@router.get("/runway-summary", response_model=RiskSummaryKPI)
def get_runway_summary():
    """Generates portfolio-wide runway metrics KPI summary."""
    bq_client = get_bigquery_client()
    
    if bq_client:
        try:
            table_id = f"{settings.GCP_PROJECT_ID}.{settings.GCP_DATASET_ID}.fact_runway_risk"
            query = f"""
                SELECT
                    COUNT(1) as total_startups,
                    COUNTIF(risk_level = 'High') as high_risk,
                    COUNTIF(risk_level = 'Medium') as med_risk,
                    COUNTIF(risk_level = 'Low') as low_risk,
                    AVG(runway_months) as avg_runway,
                    SUM(total_capital_raised_usd) as total_capital
                FROM `{table_id}`
            """
            job = bq_client.query(query)
            row = list(job)[0]
            return RiskSummaryKPI(
                total_portfolio_startups=row["total_startups"] or 0,
                high_risk_count=row["high_risk"] or 0,
                medium_risk_count=row["med_risk"] or 0,
                low_risk_count=row["low_risk"] or 0,
                avg_runway_months=round(row["avg_runway"] or 0.0, 1),
                total_capital_deployed_usd=float(row["total_capital"] or 0.0)
            )
        except Exception:
            pass

    # Query Local Warehouse Database if present
    conn = get_local_db_connection()
    if conn:
        try:
            sql = """
                SELECT
                    COUNT(*) as total_startups,
                    SUM(CASE WHEN risk_level = 'High' THEN 1 ELSE 0 END) as high_risk,
                    SUM(CASE WHEN risk_level = 'Medium' THEN 1 ELSE 0 END) as med_risk,
                    SUM(CASE WHEN risk_level = 'Low' THEN 1 ELSE 0 END) as low_risk,
                    AVG(runway_months) as avg_runway,
                    SUM(total_capital_raised_usd) as total_capital
                FROM fact_runway_risk
            """
            row = conn.execute(sql).fetchone()
            conn.close()
            return RiskSummaryKPI(
                total_portfolio_startups=row["total_startups"] or 0,
                high_risk_count=row["high_risk"] or 0,
                medium_risk_count=row["med_risk"] or 0,
                low_risk_count=row["low_risk"] or 0,
                avg_runway_months=round(row["avg_runway"] or 0.0, 1),
                total_capital_deployed_usd=float(row["total_capital"] or 0.0)
            )
        except Exception as e:
            print(f"Local warehouse metrics error: {e}")
            if conn:
                conn.close()

    total = len(MOCK_STARTUPS)
    high = len([s for s in MOCK_STARTUPS if s["risk_level"] == "High"])
    med = len([s for s in MOCK_STARTUPS if s["risk_level"] == "Medium"])
    low = len([s for s in MOCK_STARTUPS if s["risk_level"] == "Low"])
    avg_runway = sum(s["runway_months"] for s in MOCK_STARTUPS) / total if total > 0 else 0.0
    total_capital = sum(s["total_capital_raised_usd"] for s in MOCK_STARTUPS)

    return RiskSummaryKPI(
        total_portfolio_startups=total,
        high_risk_count=high,
        medium_risk_count=med,
        low_risk_count=low,
        avg_runway_months=round(avg_runway, 1),
        total_capital_deployed_usd=total_capital
    )


@router.get("/filters", response_model=FilterOptions)
def get_filter_options():
    """Returns available unique industries, countries, and risk levels for UI dropdowns."""
    conn = get_local_db_connection()
    if conn:
        try:
            ind_rows = conn.execute("SELECT DISTINCT industry FROM fact_runway_risk WHERE industry IS NOT NULL ORDER BY industry LIMIT 20").fetchall()
            cnt_rows = conn.execute("SELECT DISTINCT country FROM fact_runway_risk WHERE country IS NOT NULL ORDER BY country LIMIT 20").fetchall()
            conn.close()
            return FilterOptions(
                industries=[r["industry"] for r in ind_rows],
                countries=[r["country"] for r in cnt_rows],
                risk_levels=["High", "Medium", "Low"]
            )
        except Exception:
            if conn:
                conn.close()

    return FilterOptions(
        industries=["Artificial Intelligence", "Fintech", "Healthcare", "CleanTech", "Cybersecurity", "SaaS", "Blockchain", "Logistics"],
        countries=["USA", "GBR", "DEU", "ISR", "CAN", "FRA", "JPN", "IND"],
        risk_levels=["High", "Medium", "Low"]
    )
