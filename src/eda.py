"""Stage 1: Exploratory Data Analysis (EDA) for Startup Valuation Dataset."""

import os
import pandas as pd
import numpy as np
from pathlib import Path


def run_eda(raw_csv_path: str, report_output_path: str):
    """Performs exploratory data analysis on the raw CSV dataset and outputs a markdown report.

    Args:
        raw_csv_path: Path to raw dataset CSV.
        report_output_path: Path to markdown output report.
    """
    if not os.path.exists(raw_csv_path):
        raise FileNotFoundError(f"Raw dataset not found at {raw_csv_path}")

    print(f"Reading raw dataset for EDA: {raw_csv_path}...")
    df = pd.read_csv(raw_csv_path)

    total_rows, total_cols = df.shape
    columns = list(df.columns)
    
    # Missing values analysis
    missing_counts = df.isnull().sum()
    missing_pct = (missing_counts / total_rows * 100).round(2)
    missing_df = pd.DataFrame({
        "Column": missing_counts.index,
        "Missing Count": missing_counts.values,
        "Missing (%)": missing_pct.values
    })

    # Data types
    dtypes_series = df.dtypes.astype(str)

    # Numeric summaries
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    numeric_summary = df[numeric_cols].describe().T.reset_index().rename(columns={"index": "Column"})
    for num_col in ["mean", "std", "min", "50%", "max"]:
        if num_col in numeric_summary.columns:
            numeric_summary[num_col] = numeric_summary[num_col].round(2)

    # Categorical top values
    cat_cols = df.select_dtypes(include=["object", "string", "bool"]).columns
    cat_summaries = []
    for c in cat_cols:
        top_val = df[c].value_counts().head(1)
        val_name = top_val.index[0] if len(top_val) > 0 else "N/A"
        val_count = top_val.values[0] if len(top_val) > 0 else 0
        cat_summaries.append({
            "Column": c,
            "Unique Count": df[c].nunique(dropna=True),
            "Top Value": str(val_name),
            "Top Value Frequency": val_count
        })
    cat_df = pd.DataFrame(cat_summaries)

    # Generate Markdown Report Content
    report_lines = [
        "# Exploratory Data Analysis (EDA) Report",
        "",
        "## Executive Dataset Overview",
        f"- **Dataset File**: `{raw_csv_path}`",
        f"- **Total Record Count**: `{total_rows:,}` rows",
        f"- **Total Column Count**: `{total_cols}` columns",
        "",
        "## Column Inventory & Data Types",
        "| Column Name | Data Type | Null Count | Null (%) |",
        "| :--- | :--- | :--- | :--- |"
    ]

    for col in columns:
        null_c = missing_counts[col]
        null_p = missing_pct[col]
        dt = dtypes_series[col]
        report_lines.append(f"| `{col}` | `{dt}` | `{null_c:,}` | `{null_p}%` |")

    report_lines.extend([
        "",
        "## Numeric Column Statistics",
        "| Column | Count | Mean | Std | Min | 50% (Median) | Max |",
        "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |"
    ])

    for _, row in numeric_summary.iterrows():
        c_name = row["Column"]
        cnt = int(row["count"])
        mean_v = f"{row['mean']:,.2f}"
        std_v = f"{row['std']:,.2f}"
        min_v = f"{row['min']:,.2f}"
        med_v = f"{row['50%']:,.2f}"
        max_v = f"{row['max']:,.2f}"
        report_lines.append(f"| `{c_name}` | `{cnt:,}` | `{mean_v}` | `{std_v}` | `{min_v}` | `{med_v}` | `{max_v}` |")

    report_lines.extend([
        "",
        "## Categorical Column Distributions",
        "| Column | Unique Values | Top Frequent Value | Frequency |",
        "| :--- | :--- | :--- | :--- |"
    ])

    for _, row in cat_df.iterrows():
        c_name = row["Column"]
        u_cnt = row["Unique Count"]
        top_v = str(row["Top Value"])[:40]
        top_freq = row["Top Value Frequency"]
        report_lines.append(f"| `{c_name}` | `{u_cnt:,}` | `{top_v}` | `{top_freq:,}` |")

    report_lines.extend([
        "",
        "## Key EDA Insights & Data Cleaning Recommendations",
        "1. **Primary Identifiers**: `startup_id` provides a unique UUID per record.",
        "2. **Naming Alignment**: `startup_name` maps to target `company_name`, `funding_amount_usd` to `total_funding_usd`, `funding_date` to `last_funding_at`.",
        "3. **Operating Status Deduction**: `exited` (boolean) and `exit_type` ('IPO', 'Acquisition') derive status ('operating', 'ipo', 'acquisition').",
        "4. **Burn Rate Estimation**: Raw dataset lacks explicit `estimated_monthly_burn_usd`, derived cleanly from `employee_count` multiplier (~$12,000 / headcount / month).",
        "5. **Date Normalization**: `founded_year` converted to ISO-8601 `YYYY-01-01` date standard."
    ])

    Path(report_output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(report_output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))

    print(f"EDA report successfully generated at {report_output_path}")


if __name__ == "__main__":
    raw_csv = "data/raw/startup_valuation_dataset.csv"
    if not os.path.exists(raw_csv):
        raw_csv = "data/raw/crunchbase_startups.csv"
    report_out = "docs/eda_report.md"
    run_eda(raw_csv, report_out)
