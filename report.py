from datetime import datetime
from pathlib import Path
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


def generate_field_rankings(df: pd.DataFrame) -> str:
    rankings = """
## Field Rankings

### By 5-Year ROI (Tuition-Based)
"""
    roi_ranked = df.sort_values("roi_5yr_w_tuition", ascending=False)
    for i, (idx, row) in enumerate(roi_ranked.iterrows(), 1):
        rankings += f"{i}. **{row['field'].replace('_', ' ').title()}** - {row['roi_5yr_w_tuition']:.2f}x\n"

    rankings += """
### By Earnings per Dollar of Tuition
"""
    value_ranked = df.sort_values("earnings_per_dollar_tuition", ascending=False)
    for i, (idx, row) in enumerate(value_ranked.iterrows(), 1):
        rankings += f"{i}. **{row['field'].replace('_', ' ').title()}** - ${row['earnings_per_dollar_tuition']:.2f}\n"

    rankings += """
### By Debt-to-Income Ratio (Lower is Better)
"""
    debt_ranked = df.sort_values("debt_to_income", ascending=True)
    for i, (idx, row) in enumerate(debt_ranked.iterrows(), 1):
        rankings += f"{i}. **{row['field'].replace('_', ' ').title()}** - {row['debt_to_income']:.2f}x\n"

    rankings += """
### By Payback Period (Faster is Better)
"""
    payback_ranked = df.sort_values("payback_years", ascending=True)
    for i, (idx, row) in enumerate(payback_ranked.iterrows(), 1):
        rankings += f"{i}. **{row['field'].replace('_', ' ').title()}** - {row['payback_years']:.1f} years\n"
    rankings += "\n---\n"

    return rankings


def generate_analysis(df: pd.DataFrame) -> str:
    analysis = """
## Field Analysis

"""
    df_sorted = df.sort_values("roi_5yr_w_tuition", ascending=False)

    for idx, row in df_sorted.iterrows():
        field_name = row["field"].replace("_", " ").title()

        # Determine if above/below average
        roi_comparison = (
            "above"
            if row["roi_5yr_w_tuition"] > df["roi_5yr_w_tuition"].mean()
            else "below"
        )
        value_comparison = (
            "above"
            if row["earnings_per_dollar_tuition"]
            > df["earnings_per_dollar_tuition"].mean()
            else "below"
        )

        analysis += f"""
### {field_name}

**Financial Metrics:**
- Annual Tuition: ${row["tuition"]:,.0f}
- Total 4-Year Tuition: ${row["total_tuition"]:,.0f}
- Estimated Debt: ${row["estimated_debt"]:,.0f}
- Median Earnings (Year 2): ${row["earnings_2024_adjusted"]:,.0f}

**Return on Investment:**
- Earnings per Dollar of Tuition: ${row["earnings_per_dollar_tuition"]:.2f} ({value_comparison} average)
- 5-Year ROI (Tuition): {row["roi_5yr_w_tuition"]:.2f}x ({roi_comparison} average)
- 5-Year ROI (Debt): {row["roi_5yr_w_debt"]:.2f}x

**Debt Burden:**
- Debt-to-Income Ratio: {row["debt_to_income"]:.2f}x
- Estimated Payback Period: {row["payback_years"]:.1f} years

**Enrollment:** {row["enrollment"]:,.0f} students

---
"""

    return analysis


def generate_policy_recommendations(df: pd.DataFrame) -> str:
    # Identify high-enrollment, low-ROI fields
    median_roi = df["roi_5yr_w_tuition"].median()
    median_enrollment = df["enrollment"].median()

    high_enroll_low_roi = df[
        (df["enrollment"] > median_enrollment) & (df["roi_5yr_w_tuition"] < median_roi)
    ].sort_values("enrollment", ascending=False)

    # Identify high debt burden fields
    high_debt_burden = df[df["debt_to_income"] > 1.0].sort_values(
        "debt_to_income", ascending=False
    )

    recommendations = """
## Policy Recommendations

### Areas Requiring Attention

#### High Enrollment, Low ROI Fields
These fields serve many students but show below-median returns:

"""
    for idx, row in high_enroll_low_roi.iterrows():
        recommendations += f"- **{row['field'].replace('_', ' ').title()}**: {row['enrollment']:,.0f} students, ROI {row['roi_5yr_w_tuition']:.2f}x\n"

    recommendations += """
**Recommendations:**
- Review tuition pricing structures for these programs
- Enhance career counseling and job placement services
- Consider industry partnerships to improve employment outcomes
- Develop financial literacy programs for students in these fields

#### High Debt Burden Fields
"""
    for idx, row in high_debt_burden.iterrows():
        recommendations += f"- **{row['field'].replace('_', ' ').title()}**: Debt-to-Income {row['debt_to_income']:.2f}x, Payback {row['payback_years']:.1f} years\n"

    recommendations += """
**Recommendations:**
- Expand scholarship and grant programs for these fields
- Review whether tuition costs are justified by earnings potential
- Consider capping debt levels for students in these programs

### Best Practices to Expand

#### High-Performing Models
Fields showing strong ROI and reasonable debt burdens can serve as models:

"""
    best_practices = df[
        (df["roi_5yr_w_tuition"] > df["roi_5yr_w_tuition"].quantile(0.75))
        & (df["debt_to_income"] < df["debt_to_income"].quantile(0.5))
    ].sort_values("roi_5yr_w_tuition", ascending=False)

    for idx, row in best_practices.iterrows():
        recommendations += f"- **{row['field'].replace('_', ' ').title()}**: ROI {row['roi_5yr_w_tuition']:.2f}x, Debt-to-Income {row['debt_to_income']:.2f}x\n"

    recommendations += """
**Recommendations:**
- Study successful curriculum and industry partnership models
- Promote these fields to students considering post-secondary education

### System-Wide Improvements

1. **Transparency:** Provide prospective students with clear ROI data before enrollment
2. **Affordability:** Review tuition increases relative to earnings outcomes
3. **Accountability:** Track and publish graduate outcomes by program
4. **Support:** Enhance financial aid for high-social-value, lower-earning fields
5. **Flexibility:** Develop more affordable pathway options (e.g., co-op, apprenticeship models)

---
"""
    return recommendations


def generate_methodology(df: pd.DataFrame) -> str:
    methodology = """
## Methodology & Assumptions

### Data Sources
All data sourced from Statistics Canada tables:
- **Table 37-10-0003-01:** Canadian undergraduate tuition fees by field of study (current dollars)
- **Table 37-10-0280-01:** Characteristics and median employment income of longitudinal cohorts of postsecondary graduates two and five years after graduation, by educational qualification and field of study (alternative primary groupings)
- **Table 37-10-0011-01:** Postsecondary enrolments, by field of study, registration status, program type, credential type and gender
- **Table 37-10-0036-01:** Student debt from all sources, by province of study and level of study

### Key Assumptions

#### Inflation Adjustment
- CPI adjustment (2018 to 2024): 1.21
- CPI adjustment (2020 to 2024): 1.14

#### Debt Estimation
- Average national debt used as baseline
- Debt estimated for each field proportional to tuition costs
    - **Debt for Field:** (tuition cost for field / average tuition cost) * average national debt
- Assumes standard 4-year undergraduate program

#### ROI Calculation
- Amount earned over 5 years (minus tuition costs) compared to amount paid for tuition
- Assumes 3% annual earnings growth
- Based on median earnings 2 years post-graduation
- **5-Year ROI (Tuition):** (5-year cumulative earnings - total tuition) / total tuition
- **5-Year ROI (Debt):** (5-year cumulative earnings - estimated debt) / estimated debt

#### Payback Period Calculation
- Assumes 10% of post-tax income dedicated to debt repayment
- Tax rate assumed at 25%
- No interest on debt (simplified)
- **Post-tax Income:** median earnings * (1 - tax-rate) [tax rate assumed to be 25%]
- **Payback Years:** debt for field / (post-tax income * % of income to debt repayment) [% to debt repayment assumed to be 10%]

#### Earnings per Dollar
- Shows immediate earning potential relative to investment
- **Earnings per Dollar:** median annual earnings (year 2) / total 4-year tuition

### Limitations
- Earnings data represents median, not mean (outliers not reflected)
- Does not account for:
  - Regional variation in tuition or earnings
  - Graduate vs undergraduate distinctions in some fields
  - Scholarships, grants, or other financial aid
  - Career progression beyond Year 2
  - Job market saturation or demand
  - Individual career choices and performance

### Data Years
- Tuition: 2023/2024 academic year
- Earnings: 2018 (inflation-adjusted to 2024)
- Enrollment: 2023/2024 academic year
- Debt: 2020 (inflation-adjusted to 2024)

---
"""
    return methodology


def generate_report(df: pd.DataFrame, path: Path = Path("reports")) -> None:
    path.mkdir(parents=True, exist_ok=True)

    print("Generating report...")

    report = ""
    report += generate_summary(df)
    report += generate_field_rankings(df)
    report += generate_analysis(df)
    report += generate_methodology(df)
    report += generate_policy_recommendations(df)

    # Add footer
    report += f"""
---

**Report Generated:** {datetime.now().strftime("%B %d, %Y at %I:%M %p")}

**Data Sources:** Statistics Canada Tables 37-10-0003-01, 37-10-0280-01, 37-10-0011-01, 37-10-0036-01

For questions or additional analysis, please refer to the accompanying visualizations and raw data files.
"""

    report_path = path / "REPORT.md"
    with open(report_path, "w") as f:
        f.write(report)

    print(f"Report saved: {report_path}")
