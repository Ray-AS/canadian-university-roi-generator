from datetime import datetime
import json
from pathlib import Path
import pandas as pd


def generate_summary(df: pd.DataFrame, path: Path = Path("reports")) -> str:
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

    summary_data = {
        "report_date": datetime.now().strftime("%B %d, %Y"),
        "overall_averages": {
            "avg_annual_tuition": avg_tuition,
            "avg_total_debt": avg_debt,
            "avg_earnings_year_2": avg_earnings,
            "avg_5yr_roi": avg_roi,
            "avg_payback_period_years": avg_payback,
        },
        "best_performing": {
            "highest_roi": {
                "field": best_roi["field"],
                "roi_5yr": best_roi["roi_5yr_w_tuition"],
                "annual_tuition": best_roi["tuition"],
                "median_earnings": best_roi["earnings_2024_adjusted"],
            },
            "best_value": {
                "field": best_value["field"],
                "earnings_per_dollar": best_value["earnings_per_dollar_tuition"],
                "annual_tuition": best_value["tuition"],
                "median_earnings": best_value["earnings_2024_adjusted"],
            },
            "fastest_payback": {
                "field": fastest_payback["field"],
                "payback_years": fastest_payback["payback_years"],
                "debt_to_income": fastest_payback["debt_to_income"],
            },
        },
        "areas_of_concern": {
            "lowest_roi": {
                "field": worst_roi["field"],
                "roi_5yr": worst_roi["roi_5yr_w_tuition"],
                "annual_tuition": worst_roi["tuition"],
                "median_earnings": worst_roi["earnings_2024_adjusted"],
            },
            "lowest_value": {
                "field": worst_value["field"],
                "earnings_per_dollar": worst_value["earnings_per_dollar_tuition"],
                "annual_tuition": worst_value["tuition"],
                "median_earnings": worst_value["earnings_2024_adjusted"],
            },
            "slowest_payback": {
                "field": slowest_payback["field"],
                "payback_years": slowest_payback["payback_years"],
                "debt_to_income": slowest_payback["debt_to_income"],
            },
        },
    }

    path.mkdir(parents=True, exist_ok=True)
    json_path = path / "summary.json"
    with open(json_path, "w") as f:
        json.dump(summary_data, f, indent=4)

    summary = f"""
# Canadian University Education ROI Analysis

**Report Date:** {datetime.now().strftime("%B %d, %Y")}

## Visual Overview

This report includes the following data visualizations (see `figures/` directory):

1. **Tuition vs Earnings Chart** - Shows relationship between tuition costs and earnings (after 2 years)
2. **ROI Comparison by Field** - Side-by-side comparison of ROI of all fields
3. **Payback Period by Field** - Shows years required to repay debt at 10% of post-tax income
4. **Debt-to-Income Ratio Rankings** - Visualizes repayment burden across fields

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


def generate_field_rankings(df: pd.DataFrame, path: Path = Path("reports")) -> str:
    rankings_data = {
        "by_5yr_roi": [],
        "by_earnings_per_dollar": [],
        "by_debt_to_income": [],
        "by_payback_period": [],
    }

    rankings = """
## Field Rankings

### By 5-Year ROI (Tuition-Based)
"""
    roi_ranked = df.sort_values("roi_5yr_w_tuition", ascending=False)
    for i, (idx, row) in enumerate(roi_ranked.iterrows(), 1):
        rankings += f"{i}. **{row['field'].replace('_', ' ').title()}** - {row['roi_5yr_w_tuition']:.2f}x\n"
        rankings_data["by_5yr_roi"].append(
            {"rank": i, "field": row["field"], "value": row["roi_5yr_w_tuition"]}
        )

    rankings += """
### By Earnings per Dollar of Tuition
"""
    value_ranked = df.sort_values("earnings_per_dollar_tuition", ascending=False)
    for i, (idx, row) in enumerate(value_ranked.iterrows(), 1):
        rankings += f"{i}. **{row['field'].replace('_', ' ').title()}** - ${row['earnings_per_dollar_tuition']:.2f}\n"
        rankings_data["by_earnings_per_dollar"].append(
            {
                "rank": i,
                "field": row["field"],
                "value": row["earnings_per_dollar_tuition"],
            }
        )

    rankings += """
### By Debt-to-Income Ratio (Lower is Better)
"""
    debt_ranked = df.sort_values("debt_to_income", ascending=True)
    for i, (idx, row) in enumerate(debt_ranked.iterrows(), 1):
        rankings += f"{i}. **{row['field'].replace('_', ' ').title()}** - {row['debt_to_income']:.2f}x\n"
        rankings_data["by_debt_to_income"].append(
            {"rank": i, "field": row["field"], "value": row["debt_to_income"]}
        )

    rankings += """
### By Payback Period (Faster is Better)
"""
    payback_ranked = df.sort_values("payback_years", ascending=True)
    for i, (idx, row) in enumerate(payback_ranked.iterrows(), 1):
        rankings += f"{i}. **{row['field'].replace('_', ' ').title()}** - {row['payback_years']:.1f} years\n"
        rankings_data["by_payback_period"].append(
            {"rank": i, "field": row["field"], "value": row["payback_years"]}
        )
    rankings += "\n---\n"

    path.mkdir(parents=True, exist_ok=True)
    json_path = path / "rankings.json"
    with open(json_path, "w") as f:
        json.dump(rankings_data, f, indent=4)

    return rankings


def generate_table(df: pd.DataFrame, path: Path = Path("reports")) -> str:
    # Sort by ROI for table presentation
    df_sorted = df.sort_values("roi_5yr_w_tuition", ascending=False).copy()
    path.mkdir(parents=True, exist_ok=True)
    csv_path = path / "roi_table.csv"
    df_sorted.to_csv(csv_path, index=False)

    table = """
## Data Table

| Field | Annual Tuition | Total Debt | Earnings (Yr 2) | ROI (Tuition) | ROI (Debt) | Debt-to-Income | Payback Years | Earnings/$ Tuition | Enrollment |
|-------|----------------|------------|-----------------|---------------|------------|----------------|---------------|-------------------|------------|
"""

    for idx, row in df_sorted.iterrows():
        field_name = row["field"].replace("_", " ").title()
        table += f"| {field_name} | ${row['tuition']:,.0f} | ${row['estimated_debt']:,.0f} | ${row['earnings_2024_adjusted']:,.0f} | {row['roi_5yr_w_tuition']:.2f}x | {row['roi_5yr_w_debt']:.2f}x | {row['debt_to_income']:.2f}x | {row['payback_years']:.1f} yrs | ${row['earnings_per_dollar_tuition']:.2f} | {row['enrollment']:,.0f} |\n"

    table += """
---
"""
    return table


def generate_visualizations(df: pd.DataFrame, path: Path = Path("reports")) -> str:
    viz_data = {
        "visualizations": [
            {
                "name": "Tuition vs Earnings Chart",
                "filename": "tuition_vs_earnings.png",
                "description": "Shows the relationship between total 4-year tuition costs and median earnings 2 years after graduation",
            },
            {
                "name": "ROI Comparison by Field",
                "filename": "roi_by_field.png",
                "description": "Side-by-side comparison showing 5-year ROI calculated based on tuition and debt",
            },
            {
                "name": "Payback Period by Field",
                "filename": "payback_years.png",
                "description": "Estimated years to repay student debt assuming 25% tax rate and 10% of post-tax income to debt repayment",
            },
            {
                "name": "Debt-to-Income Ratio Rankings",
                "filename": "debt_to_income_ratio.png",
                "description": "Horizontal bar chart showing estimated debt as a multiple of annual earnings",
            },
        ]
    }

    path.mkdir(parents=True, exist_ok=True)
    json_path = path / "visualizations.json"
    with open(json_path, "w") as f:
        json.dump(viz_data, f, indent=4)

    visualization = """
## Data Visualizations

This report is accompanied by four key visualizations located in the `figures/` directory. Each visualization highlights different aspects of the ROI analysis:

### 1. Tuition vs Earnings Chart
**File:** `figures/tuition_vs_earnings.png`

Shows the relationship between total 4-year tuition costs and median earnings 2 years after graduation:
- Whether higher tuition translates to higher earnings
- Outliers in either direction (high cost/low earnings or low cost/high earnings)

![tuition_vs_earnings](../figures/tuition_vs_earnings.png)

**Key Insight:** Some of the lowest-tuition fields produce competitive earnings, suggesting strong value for students.

---

### 2. ROI Comparison by Field
**File:** `figures/roi_by_field.png`

Side-by-side comparison showing 5-year ROI calculated two ways:
- Based on total tuition paid
- Based on estimated debt incurred

Includes average ROI lines for both calculations. The gap between the two bars shows how debt burden affects returns.

![roi_by_field](../figures/roi_by_field.png)

**Key Insight:** Fields where debt-based ROI is significantly lower than tuition-based ROI indicate students are over-borrowing relative to costs.

---

### 3. Payback Period by Field
**File:** `figures/payback_years.png`

Shows estimated years to repay student debt assuming 25% tax rate on income and 10% of post-tax income goes to debt repayment. Converts abstract debt figures into time, which is more intuitive for students and families.

![payback_years](../figures/payback_years.png)

**Key Insight:** Fields requiring 15+ years for debt repayment may discourage students despite long-term career potential.

---

### 4. Debt-to-Income Ratio Rankings
**File:** `figures/debt_to_income_ratio.png`

Horizontal bar chart showing estimated debt as a multiple of annual earnings. A ratio above 1.0 means debt exceeds annual income. Lower is better.

![debt_to_income](../figures/debt_to_income_ratio.png)

**Key Insight:** Fields with ratios above 1.2x may face significant repayment stress and warrant financial aid attention.

---
"""
    return visualization


def generate_analysis(df: pd.DataFrame, path: Path = Path("reports")) -> str:
    df_sorted = df.sort_values("roi_5yr_w_tuition", ascending=False)
    analysis_data = {"fields": []}

    analysis = """
## Field Analysis

"""

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

        analysis_data["fields"].append(
            {
                "field": row["field"],
                "field_display_name": field_name,
                "financial_metrics": {
                    "annual_tuition": row["tuition"],
                    "total_4yr_tuition": row["total_tuition"],
                    "estimated_debt": row["estimated_debt"],
                    "median_earnings_year_2": row["earnings_2024_adjusted"],
                },
                "roi_metrics": {
                    "earnings_per_dollar_tuition": row["earnings_per_dollar_tuition"],
                    "earnings_per_dollar_comparison": value_comparison,
                    "roi_5yr_tuition": row["roi_5yr_w_tuition"],
                    "roi_tuition_comparison": roi_comparison,
                    "roi_5yr_debt": row["roi_5yr_w_debt"],
                },
                "debt_burden": {
                    "debt_to_income_ratio": row["debt_to_income"],
                    "payback_period_years": row["payback_years"],
                },
                "enrollment": int(row["enrollment"]),
            }
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

    path.mkdir(parents=True, exist_ok=True)
    json_path = path / "analysis.json"
    with open(json_path, "w") as f:
        json.dump(analysis_data, f, indent=4)

    return analysis


def generate_policy_recommendations(
    df: pd.DataFrame, path: Path = Path("reports")
) -> str:
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

    policy_data = {
        "areas_requiring_attention": {
            "high_enrollment_low_roi": [],
            "high_debt_burden": [],
        },
        "best_practices": [],
        "recommendations": {
            "high_enrollment_low_roi_fields": [
                "Review tuition pricing structures for these programs",
                "Enhance career counseling and job placement services",
                "Consider industry partnerships to improve employment outcomes",
                "Develop financial literacy programs for students in these fields",
            ],
            "high_debt_burden_fields": [
                "Expand scholarship and grant programs for these fields",
                "Review whether tuition costs are justified by earnings potential",
                "Consider capping debt levels for students in these programs",
            ],
            "system_wide": [
                "Transparency: Provide prospective students with clear ROI data before enrollment",
                "Affordability: Review tuition increases relative to earnings outcomes",
                "Accountability: Track and publish graduate outcomes by program",
                "Support: Enhance financial aid for high-social-value, lower-earning fields",
                "Flexibility: Develop more affordable pathway options (e.g., co-op, apprenticeship models)",
            ],
        },
    }

    recommendations = """
## Policy Recommendations

### Areas Requiring Attention

#### High Enrollment, Low ROI Fields
These fields serve many students but show below-median returns:

"""
    for idx, row in high_enroll_low_roi.iterrows():
        recommendations += f"- **{row['field'].replace('_', ' ').title()}**: {row['enrollment']:,.0f} students, ROI {row['roi_5yr_w_tuition']:.2f}x\n"
        policy_data["areas_requiring_attention"]["high_enrollment_low_roi"].append(
            {
                "field": row["field"],
                "enrollment": int(row["enrollment"]),
                "roi_5yr": row["roi_5yr_w_tuition"],
            }
        )

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
        policy_data["areas_requiring_attention"]["high_debt_burden"].append(
            {
                "field": row["field"],
                "debt_to_income": row["debt_to_income"],
                "payback_years": row["payback_years"],
            }
        )

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
        policy_data["best_practices"].append(
            {
                "field": row["field"],
                "roi_5yr": row["roi_5yr_w_tuition"],
                "debt_to_income": row["debt_to_income"],
            }
        )

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

    path.mkdir(parents=True, exist_ok=True)
    json_path = path / "policy_recommendations.json"
    with open(json_path, "w") as f:
        json.dump(policy_data, f, indent=2)

    return recommendations


def generate_methodology(df: pd.DataFrame, path: Path = Path("reports")) -> str:
    methodology_data = {
        "data_sources": [
            "Table 37-10-0003-01: Canadian undergraduate tuition fees by field of study",
            "Table 37-10-0280-01: Characteristics and median employment income of longitudinal cohorts",
            "Table 37-10-0011-01: Postsecondary enrolments by field of study",
            "Table 37-10-0036-01: Student debt from all sources",
        ],
        "assumptions": {
            "inflation_adjustment": {
                "cpi_2018_to_2024": 1.21,
                "cpi_2020_to_2024": 1.14,
            },
            "debt_estimation": {
                "method": "Proportional to tuition costs",
                "formula": "(tuition_for_field / avg_tuition) * avg_national_debt",
                "program_length": "4 years",
            },
            "roi_calculation": {
                "earnings_growth": 0.03,
                "base_period": "2 years post-graduation",
                "tuition_roi_formula": "(5yr_cumulative_earnings - total_tuition) / total_tuition",
                "debt_roi_formula": "(5yr_cumulative_earnings - estimated_debt) / estimated_debt",
            },
            "payback_calculation": {
                "income_to_debt_repayment": 0.10,
                "tax_rate": 0.25,
                "interest_rate": 0.0,
                "formula": "debt / (post_tax_income * repayment_percentage)",
            },
            "earnings_per_dollar": {
                "formula": "median_annual_earnings_year2 / total_4yr_tuition"
            },
        },
        "limitations": [
            "Earnings data represents median, not mean",
            "Does not account for regional variation",
            "Does not distinguish graduate vs undergraduate in some fields",
            "Does not account for scholarships, grants, or other financial aid",
            "Does not account for career progression beyond Year 2",
            "Does not account for job market saturation or demand",
            "Does not account for individual career choices and performance",
        ],
        "data_years": {
            "tuition": "2023/2024",
            "earnings": "2018 (inflation-adjusted to 2024)",
            "enrollment": "2023/2024",
            "debt": "2020 (inflation-adjusted to 2024)",
        },
    }

    path.mkdir(parents=True, exist_ok=True)
    json_path = path / "methodology.json"
    with open(json_path, "w") as f:
        json.dump(methodology_data, f, indent=2)

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
    report += generate_table(df)
    report += generate_visualizations(df)
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
