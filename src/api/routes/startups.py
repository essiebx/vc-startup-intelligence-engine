"""Startup routes endpoint handler."""

from typing import Optional
from fastapi import APIRouter, Query
from src.api.schemas import StartupListResponse, RunwayRiskItem
from src.api.database import get_bigquery_client, get_local_db_connection
from src.config import settings

router = APIRouter(prefix="/startups", tags=["Startups"])

MOCK_STARTUPS = [
    {
        "startup_id": "sup-001",
        "company_name": "ApexAI Solutions",
        "industry": "Artificial Intelligence",
        "country": "USA",
        "status": "operating",
        "total_capital_raised_usd": 12500000.0,
        "estimated_monthly_burn_usd": 450000.0,
        "last_funding_date": "2024-11-15",
        "months_since_last_raise": 8,
        "estimated_cash_reserve_usd": 8750000.0,
        "runway_months": 11.4,
        "risk_level": "Medium"
    },
    {
        "startup_id": "sup-002",
        "company_name": "QuantumPay Systems",
        "industry": "Fintech",
        "country": "GBR",
        "status": "operating",
        "total_capital_raised_usd": 4200000.0,
        "estimated_monthly_burn_usd": 380000.0,
        "last_funding_date": "2023-08-10",
        "months_since_last_raise": 23,
        "estimated_cash_reserve_usd": 2940000.0,
        "runway_months": 4.7,
        "risk_level": "High"
    }
]


@router.get("", response_model=StartupListResponse)
def list_startups(
    search: Optional[str] = Query(None, description="Search by company name or industry"),
    risk_level: Optional[str] = Query(None, description="Filter by risk category: High, Medium, Low"),
    industry: Optional[str] = Query(None, description="Filter by industry"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100)
):
    """Retrieves paginated list of startups with calculated runway risk parameters."""
    bq_client = get_bigquery_client()
    
    if bq_client:
        try:
            table_id = f"{settings.GCP_PROJECT_ID}.{settings.GCP_DATASET_ID}.fact_runway_risk"
            where_clauses = []
            if risk_level:
                where_clauses.append(f"LOWER(risk_level) = '{risk_level.lower()}'")
            if industry:
                where_clauses.append(f"LOWER(industry) = '{industry.lower()}'")
            if search:
                where_clauses.append(
                    f"(LOWER(company_name) LIKE '%{search.lower()}%' OR LOWER(industry) LIKE '%{search.lower()}%')"
                )
            
            where_str = f"WHERE {' AND '.join(where_clauses)}" if where_clauses else ""
            query = f"""
                SELECT * FROM `{table_id}`
                {where_str}
                ORDER BY runway_months ASC
                LIMIT {page_size} OFFSET {(page - 1) * page_size}
            """
            query_job = bq_client.query(query)
            results = [dict(row) for row in query_job]
            
            return StartupListResponse(
                total_count=len(results),
                page=page,
                page_size=page_size,
                items=[RunwayRiskItem(**item) for item in results]
            )
        except Exception:
            pass

    # Query Local Warehouse Database if available
    conn = get_local_db_connection()
    if conn:
        try:
            where_clauses = []
            params = []
            if risk_level and risk_level != "All":
                where_clauses.append("LOWER(risk_level) = ?")
                params.append(risk_level.lower())
            if industry:
                where_clauses.append("LOWER(industry) = ?")
                params.append(industry.lower())
            if search:
                where_clauses.append("(LOWER(company_name) LIKE ? OR LOWER(industry) LIKE ?)")
                params.extend([f"%{search.lower()}%", f"%{search.lower()}%"])

            where_str = f"WHERE {' AND '.join(where_clauses)}" if where_clauses else ""
            
            count_sql = f"SELECT COUNT(*) FROM fact_runway_risk {where_str}"
            total_count = conn.execute(count_sql, params).fetchone()[0]

            sql = f"""
                SELECT * FROM fact_runway_risk
                {where_str}
                ORDER BY runway_months ASC
                LIMIT ? OFFSET ?
            """
            query_params = params + [page_size, (page - 1) * page_size]
            rows = conn.execute(sql, query_params).fetchall()
            results = [dict(row) for row in rows]
            conn.close()

            return StartupListResponse(
                total_count=total_count,
                page=page,
                page_size=page_size,
                items=[RunwayRiskItem(**item) for item in results]
            )
        except Exception as e:
            print(f"Local warehouse query error: {e}")
            if conn:
                conn.close()

    # Fallback to mock data
    items = MOCK_STARTUPS
    return StartupListResponse(
        total_count=len(items),
        page=page,
        page_size=page_size,
        items=[RunwayRiskItem(**item) for item in items[:page_size]]
    )
