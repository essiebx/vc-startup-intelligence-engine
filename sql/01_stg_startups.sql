-- =============================================================================
-- STAGING MODEL: stg_startups
-- Purpose: Ingest and clean raw startup data from Kaggle / Crunchbase source
-- =============================================================================

CREATE OR REPLACE TABLE `{{project_id}}.{{dataset_id}}.stg_startups` AS
SELECT
    TRIM(LOWER(startup_id)) AS startup_id,
    TRIM(name) AS company_name,
    TRIM(category_list) AS industry,
    TRIM(country_code) AS country,
    TRIM(city) AS city,
    TRIM(status) AS status, -- operating, acquired, closed, ipo
    PARSE_DATE('%Y-%m-%d', founded_at) AS founded_date,
    CAST(funding_rounds AS INT64) AS total_funding_rounds,
    CAST(total_funding_usd AS NUMERIC) AS total_capital_raised_usd,
    PARSE_DATE('%Y-%m-%d', last_funding_at) AS last_funding_date,
    CAST(estimated_monthly_burn_usd AS NUMERIC) AS estimated_monthly_burn_usd,
    CURRENT_TIMESTAMP() AS ingested_at
FROM
    `{{project_id}}.{{dataset_id}}.raw_startups`
WHERE
    startup_id IS NOT NULL;
