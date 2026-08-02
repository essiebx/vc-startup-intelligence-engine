-- =============================================================================
-- ANALYTICAL MART: fact_runway_risk
-- Purpose: Calculate cash runway months and classify portfolio startup risk level
-- Formula:
--   Months Since Last Raise = DATE_DIFF(CURRENT_DATE(), last_funding_date, MONTH)
--   Raw Reserve (USD)       = total_capital_raised_usd * 0.70
--   Calculated Runway (Mo)  = GREATEST(0, (Raw Reserve / monthly_burn_usd) - Months Since Last Raise)
--   Risk Category:
--     High Risk   : < 6 months
--     Medium Risk : 6 - 12 months
--     Low Risk    : > 12 months
-- =============================================================================

CREATE OR REPLACE TABLE `{{project_id}}.{{dataset_id}}.fact_runway_risk` AS
WITH metrics_prep AS (
    SELECT
        startup_id,
        company_name,
        industry,
        country,
        status,
        total_capital_raised_usd,
        estimated_monthly_burn_usd,
        last_funding_date,
        DATE_DIFF(CURRENT_DATE(), last_funding_date, MONTH) AS months_since_last_raise,
        (total_capital_raised_usd * 0.70) AS estimated_cash_reserve_usd
    FROM
        `{{project_id}}.{{dataset_id}}.stg_startups`
    WHERE
        estimated_monthly_burn_usd > 0
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
            GREATEST(
                0.0,
                (estimated_cash_reserve_usd / estimated_monthly_burn_usd) - months_since_last_raise
            ),
            1
        ) AS runway_months
    FROM
        metrics_prep
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
    CURRENT_TIMESTAMP() AS calculated_at
FROM
    runway_calc;
