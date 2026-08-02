export interface Startup {
  startup_id: string;
  company_name: string;
  industry: string;
  country: string;
  status: string;
  total_capital_raised_usd: number;
  estimated_monthly_burn_usd: number;
  last_funding_date?: string;
  months_since_last_raise: number;
  estimated_cash_reserve_usd: number;
  runway_months: number;
  risk_level: 'High' | 'Medium' | 'Low';
}

export interface RiskSummaryKPI {
  total_portfolio_startups: number;
  high_risk_count: number;
  medium_risk_count: number;
  low_risk_count: number;
  avg_runway_months: number;
  total_capital_deployed_usd: number;
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api/v1';

export async function fetchRunwaySummary(): Promise<RiskSummaryKPI> {
  try {
    const res = await fetch(`${API_BASE_URL}/metrics/runway-summary`, { cache: 'no-store' });
    if (!res.ok) throw new Error('Failed to fetch metrics summary');
    return await res.json();
  } catch (error) {
    console.warn('API error, returning fallback metrics:', error);
    return {
      total_portfolio_startups: 5,
      high_risk_count: 2,
      medium_risk_count: 1,
      low_risk_count: 2,
      avg_runway_months: 13.2,
      total_capital_deployed_usd: 69600000.0,
    };
  }
}

export async function fetchStartups(search?: string, riskLevel?: string): Promise<Startup[]> {
  try {
    const params = new URLSearchParams();
    if (search) params.append('search', search);
    if (riskLevel && riskLevel !== 'All') params.append('risk_level', riskLevel);

    const res = await fetch(`${API_BASE_URL}/startups?${params.toString()}`, { cache: 'no-store' });
    if (!res.ok) throw new Error('Failed to fetch startups list');
    const data = await res.json();
    return data.items;
  } catch (error) {
    console.warn('API error, returning fallback startup list:', error);
    return [
      {
        startup_id: 'sup-001',
        company_name: 'ApexAI Solutions',
        industry: 'Artificial Intelligence',
        country: 'USA',
        status: 'operating',
        total_capital_raised_usd: 12500000.0,
        estimated_monthly_burn_usd: 450000.0,
        last_funding_date: '2024-11-15',
        months_since_last_raise: 8,
        estimated_cash_reserve_usd: 8750000.0,
        runway_months: 11.4,
        risk_level: 'Medium',
      },
      {
        startup_id: 'sup-002',
        company_name: 'QuantumPay Systems',
        industry: 'Fintech',
        country: 'GBR',
        status: 'operating',
        total_capital_raised_usd: 4200000.0,
        estimated_monthly_burn_usd: 380000.0,
        last_funding_date: '2023-08-10',
        months_since_last_raise: 23,
        estimated_cash_reserve_usd: 2940000.0,
        runway_months: 4.7,
        risk_level: 'High',
      },
      {
        startup_id: 'sup-003',
        company_name: 'BioHealth Robotics',
        industry: 'Healthcare',
        country: 'DEU',
        status: 'operating',
        total_capital_raised_usd: 28000000.0,
        estimated_monthly_burn_usd: 620000.0,
        last_funding_date: '2025-02-01',
        months_since_last_raise: 3,
        estimated_cash_reserve_usd: 19600000.0,
        runway_months: 28.6,
        risk_level: 'Low',
      },
    ];
  }
}
