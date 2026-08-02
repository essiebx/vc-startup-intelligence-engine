-- =============================================================================
-- FACT TABLE: fact_funding_rounds
-- Purpose: Granular funding events per startup
-- =============================================================================

CREATE OR REPLACE TABLE `{{project_id}}.{{dataset_id}}.fact_funding_rounds` AS
SELECT
    GENERATE_UUID() AS round_id,
    s.startup_id,
    s.last_funding_date AS round_date,
    s.total_funding_rounds AS round_number,
    s.total_capital_raised_usd AS amount_raised_usd,
    s.ingested_at
FROM
    `{{project_id}}.{{dataset_id}}.stg_startups` s
WHERE
    s.total_capital_raised_usd > 0;
