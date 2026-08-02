# Frontend Web Cockpit & Power BI Specification

## 1. Next.js Component Hierarchy & UI Specs

### App Router Layout Tree (`frontend/src/`)

```text
src/
├── app/
│   ├── layout.tsx         # Global Providers, HTML shell, Dark mode
│   ├── page.tsx           # Interactive VC Radar Dashboard Page
│   └── globals.css        # Tailwind directives & design system reset
├── components/
│   ├── Header.tsx         # Brand header with status indicators
│   ├── KpiCard.tsx        # High, Med, Low risk KPI metrics cards
│   ├── RiskBadge.tsx      # Color-coded visual status badge (High, Med, Low)
│   └── StartupTable.tsx   # Interactive filterable, sortable runway table
└── lib/
    └── api.ts             # API client functions with error handling & fallback
```

### Dashboard UI Component Layout
1. **Header Component (`Header.tsx`)**:
   - Platform title ("VC Startup Intelligence Cockpit").
   - Live indicators for BigQuery connection and FastAPI engine status.
2. **Executive KPI Strip (`KpiCard.tsx`)**:
   - 4-card responsive grid:
     - **High Risk Count** (Red alert accent, `<6` mo remaining).
     - **Medium Risk Watch** (Amber warning accent, `6–12` mo).
     - **Low Risk Buffer** (Green success accent, `>12` mo).
     - **Portfolio Average Runway** (Cyan metrics accent).
3. **Filter Control Bar**:
   - Search input box (company name / sector).
   - Quick risk category toggle buttons (`All`, `High`, `Medium`, `Low`).
   - Refresh button with loading spinner state.
4. **Startup Risk Table (`StartupTable.tsx`)**:
   - Tabular view listing: Company Name, Industry Sector, Total Raised, Monthly Burn Rate, Runway (Months), and Risk Level Badge.

---

## 2. Power BI Executive Cockpit Specification

### Direct Query / Import Model
- **Data Source**: BigQuery analytical mart `fact_runway_risk`.
- **Refresh Frequency**: Scheduled daily refresh / direct query mode.

### DAX Measures Specification

#### 1. High Risk Startup Count
```dax
HighRiskStartupsCount = 
CALCULATE(
    COUNTROWS(fact_runway_risk),
    fact_runway_risk[risk_level] = "High"
)
```

#### 2. Weighted Average Runway (Months)
```dax
WeightedAvgRunwayMonths = 
AVERAGEX(
    fact_runway_risk,
    fact_runway_risk[runway_months]
)
```

#### 3. Total Capital at Imminent Risk (USD)
```dax
CapitalAtImminentRiskUSD = 
CALCULATE(
    SUM(fact_runway_risk[total_capital_raised_usd]),
    fact_runway_risk[risk_level] = "High"
)
```

### Visual Layout Grid
- **Header**: YC Partner Dashboard Title + Global Date Slicer.
- **Top Row Cards**: `HighRiskStartupsCount`, `WeightedAvgRunwayMonths`, `CapitalAtImminentRiskUSD`.
- **Main Area**:
  - Left: Scatter plot of Monthly Burn Rate (Y-axis) vs Capital Raised (X-axis) colored by Risk Level.
  - Right: Table listing of High Risk companies with runway months and last funding date.
