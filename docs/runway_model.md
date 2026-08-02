# Runway Risk Calculation Model

## Overview

The runway risk detection algorithm computes how many months of operational runway a startup has remaining based on its total capital raised, estimated monthly burn rate, and elapsed time since its last funding round.

## Mathematical Model

$$ \text{Estimated Reserve (USD)} = \text{Total Capital Raised} \times 0.70 $$

$$ \text{Months Elapsed} = \text{DATE\_DIFF}(\text{Current Date}, \text{Last Funding Date}, \text{Months}) $$

$$ \text{Runway (Months)} = \max\left(0, \frac{\text{Estimated Reserve}}{\text{Estimated Monthly Burn}} - \text{Months Elapsed}\right) $$

## Risk Threshold Classification

| Risk Level | Runway Threshold | Description | Action Required |
| :--- | :--- | :--- | :--- |
| **High** | $< 6$ months | Imminent capital exhaustion risk | Immediate bridge round or emergency cost reduction |
| **Medium** | $6 - 12$ months | Approaching fundraising window | Prepare deck, initiate partner contacts |
| **Low** | $> 12$ months | Healthy capital buffer | Focus on growth & execution |

## Assumptions & Constants

1. **Reserve Multiplier ($0.70$)**: Assumes $30\%$ of total raised capital is consumed by initial capex, setup, tax, or fees prior to steady-state burn.
2. **Linear Monthly Burn**: Assumes constant burn rate unless updated by revised financial reporting.
