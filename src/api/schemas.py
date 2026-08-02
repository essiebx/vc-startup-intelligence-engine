"""Pydantic Request & Response Data Models."""

from typing import List, Optional
from pydantic import BaseModel, Field


class StartupBase(BaseModel):
    startup_id: str
    company_name: str
    industry: str
    country: str
    status: str
    total_capital_raised_usd: float
    estimated_monthly_burn_usd: float
    last_funding_date: Optional[str] = None


class RunwayRiskItem(StartupBase):
    months_since_last_raise: int
    estimated_cash_reserve_usd: float
    runway_months: float
    risk_level: str = Field(..., description="High (<6m), Medium (6-12m), Low (>12m)")


class StartupListResponse(BaseModel):
    total_count: int
    page: int
    page_size: int
    items: List[RunwayRiskItem]


class RiskSummaryKPI(BaseModel):
    total_portfolio_startups: int
    high_risk_count: int
    medium_risk_count: int
    low_risk_count: int
    avg_runway_months: float
    total_capital_deployed_usd: float


class FilterOptions(BaseModel):
    industries: List[str]
    countries: List[str]
    risk_levels: List[str]
