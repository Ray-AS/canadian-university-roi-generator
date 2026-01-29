from datetime import datetime
import pandas as pd


def generate_summary(df: pd.DataFrame) -> str:
    avg_tuition = df["tuition"].mean()
    avg_debt = df["estimated_debt"].mean()
    avg_earnings = df["earnings_2024_adjusted"].mean()
    avg_roi = df["roi_5yr_w_tuition"].mean()
    avg_payback = df["payback_years"].mean()

    best_roi = df.loc[df["roi_5yr_w_tuition"].idxmax()]
    worst_roi = df.loc[df["roi_5yr_w_tuition"].idxmin()]

    best_value = df.loc[df["earnings_per_dollar_tuition"].idxmax()]
    worst_value = df.loc[df["earnings_per_dollar_tuition"].idxmin()]

    fastest_payback = df.loc[df["payback_years"].idxmin()]
    slowest_payback = df.loc[df["payback_years"].idxmax()]

    summary = f"""
# Summary: Canadian University Education ROI Analysis

**Report Date:** {datetime.now().strftime("%B %d, %Y")}

## Key Findings

### Overall
- **Average Annual Tuition:** ${avg_tuition:,.0f}
- **Average Total Debt:** ${avg_debt:,.0f}
- **Average Earnings (Year 2):** ${avg_earnings:,.0f}
- **Average 5-Year ROI:** {avg_roi:.2f}x
- **Average Payback Period:** {avg_payback:.1f} years

### Best Performing Fields

**Highest ROI:** {best_roi["field"].replace("_", " ").title()}
- 5-Year ROI: {best_roi["roi_5yr_w_tuition"]:.2f}x
- Annual Tuition: ${best_roi["tuition"]:,.0f}
- Median Earnings: ${best_roi["earnings_2024_adjusted"]:,.0f}

**Best Value for Money:** {best_value["field"].replace("_", " ").title()}
- Earnings per Dollar: ${best_value["earnings_per_dollar_tuition"]:.2f}
- Annual Tuition: ${best_value["tuition"]:,.0f}
- Median Earnings: ${best_value["earnings_2024_adjusted"]:,.0f}

**Fastest Debt Payback:** {fastest_payback["field"].replace("_", " ").title()}
- Payback Period: {fastest_payback["payback_years"]:.1f} years
- Debt-to-Income: {fastest_payback["debt_to_income"]:.2f}x

### Areas of Concern

**Lowest ROI:** {worst_roi["field"].replace("_", " ").title()}
- 5-Year ROI: {worst_roi["roi_5yr_w_tuition"]:.2f}x
- Annual Tuition: ${worst_roi["tuition"]:,.0f}
- Median Earnings: ${worst_roi["earnings_2024_adjusted"]:,.0f}

**Lowest Value for Money:** {worst_value["field"].replace("_", " ").title()}
- Earnings per Dollar: ${worst_value["earnings_per_dollar_tuition"]:.2f}
- Annual Tuition: ${worst_value["tuition"]:,.0f}
- Median Earnings: ${worst_value["earnings_2024_adjusted"]:,.0f}

**Slowest Debt Payback:** {slowest_payback["field"].replace("_", " ").title()}
- Payback Period: {slowest_payback["payback_years"]:.1f} years
- Debt-to-Income: {slowest_payback["debt_to_income"]:.2f}x

---
"""
    return summary
