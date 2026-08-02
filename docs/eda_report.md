# Exploratory Data Analysis (EDA) Report

## Executive Dataset Overview
- **Dataset File**: `data/raw/startup_valuation_dataset.csv`
- **Total Record Count**: `50,000` rows
- **Total Column Count**: `17` columns

## Column Inventory & Data Types
| Column Name | Data Type | Null Count | Null (%) |
| :--- | :--- | :--- | :--- |
| `startup_id` | `str` | `0` | `0.0%` |
| `startup_name` | `str` | `0` | `0.0%` |
| `founded_year` | `int64` | `0` | `0.0%` |
| `country` | `str` | `0` | `0.0%` |
| `region` | `str` | `0` | `0.0%` |
| `industry` | `str` | `0` | `0.0%` |
| `funding_round` | `str` | `0` | `0.0%` |
| `funding_amount_usd` | `int64` | `0` | `0.0%` |
| `funding_date` | `str` | `0` | `0.0%` |
| `lead_investor` | `str` | `0` | `0.0%` |
| `co_investors` | `str` | `0` | `0.0%` |
| `employee_count` | `int64` | `0` | `0.0%` |
| `estimated_revenue_usd` | `float64` | `0` | `0.0%` |
| `estimated_valuation_usd` | `float64` | `0` | `0.0%` |
| `exited` | `bool` | `0` | `0.0%` |
| `exit_type` | `str` | `45,100` | `90.2%` |
| `tags` | `str` | `0` | `0.0%` |

## Numeric Column Statistics
| Column | Count | Mean | Std | Min | 50% (Median) | Max |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `founded_year` | `50,000` | `2,013.98` | `5.49` | `2,005.00` | `2,014.00` | `2,023.00` |
| `funding_amount_usd` | `50,000` | `811,933,933.64` | `1,273,724,346.20` | `3,925,000.00` | `439,832,000.00` | `61,037,115,000.00` |
| `employee_count` | `50,000` | `502.43` | `289.13` | `2.00` | `503.00` | `1,000.00` |
| `estimated_revenue_usd` | `50,000` | `223,188,413.77` | `401,447,328.45` | `622,017.24` | `106,859,740.48` | `23,041,887,506.12` |
| `estimated_valuation_usd` | `50,000` | `4,887,720,266.19` | `8,277,872,908.98` | `12,794,685.51` | `2,442,208,693.32` | `322,060,497,842.35` |

## Categorical Column Distributions
| Column | Unique Values | Top Frequent Value | Frequency |
| :--- | :--- | :--- | :--- |
| `startup_id` | `50,000` | `456bf4d2-b982-41e7-83fe-04bac2053405` | `1` |
| `startup_name` | `36,866` | `Smith and Sons` | `73` |
| `country` | `243` | `Congo` | `429` |
| `region` | `6` | `Oceania` | `8,436` |
| `industry` | `7` | `Fintech` | `7,259` |
| `funding_round` | `7` | `Series B` | `11,877` |
| `funding_date` | `3,653` | `2024-10-20` | `29` |
| `lead_investor` | `7` | `SoftBank` | `7,287` |
| `co_investors` | `259` | `Tiger Global` | `2,402` |
| `exited` | `2` | `False` | `42,667` |
| `exit_type` | `2` | `IPO` | `2,529` |
| `tags` | `18,644` | `EdTech, Mobile` | `138` |

## Key EDA Insights & Data Cleaning Recommendations
1. **Primary Identifiers**: `startup_id` provides a unique UUID per record.
2. **Naming Alignment**: `startup_name` maps to target `company_name`, `funding_amount_usd` to `total_funding_usd`, `funding_date` to `last_funding_at`.
3. **Operating Status Deduction**: `exited` (boolean) and `exit_type` ('IPO', 'Acquisition') derive status ('operating', 'ipo', 'acquisition').
4. **Burn Rate Estimation**: Raw dataset lacks explicit `estimated_monthly_burn_usd`, derived cleanly from `employee_count` multiplier (~$12,000 / headcount / month).
5. **Date Normalization**: `founded_year` converted to ISO-8601 `YYYY-01-01` date standard.