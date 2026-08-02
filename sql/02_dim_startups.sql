-- =============================================================================
-- DIMENSION TABLE: dim_startups
-- Purpose: Canonical dimension table for portfolio & market startup profiles
-- =============================================================================

CREATE OR REPLACE TABLE `{{project_id}}.{{dataset_id}}.dim_startups` AS
SELECT
    startup_id,
    company_name,
    COALESCE(industry, 'Unspecified') AS industry,
    COALESCE(country, 'Unknown') AS country,
    city,
    status,
    founded_date,
    EXTRACT(YEAR FROM founded_date) AS founded_year,
    ingested_at AS created_at,
    CURRENT_TIMESTAMP() AS updated_at
FROM
    `{{project_id}}.{{dataset_id}}.stg_startups`;
