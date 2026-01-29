import pandas as pd

from services.configs import (
    INCOME_TO_PAYOFF,
    RATE_OF_EARNING_GROWTH,
    TAX_RATE,
    YEARS_OF_TUITION,
)


def calculate_roi_by_field(df: pd.DataFrame) -> pd.DataFrame:
    df["total_tuition"] = df["tuition"] * YEARS_OF_TUITION
    df["debt_to_income"] = df["estimated_debt"] / df["earnings_2024_adjusted"]
    pass

    # Payback years (assuming 10% of post-tax income, 25% tax rate)
    post_tax = df["earnings_2024_adjusted"] * (1 - TAX_RATE)
    annual_payment = post_tax * INCOME_TO_PAYOFF
    df["payback_years"] = df["estimated_debt"] / annual_payment

    # 5-year ROI (assume 3% annual salary growth)
    df["earnings_5yr"] = df["earnings_2024_adjusted"] * (
        RATE_OF_EARNING_GROWTH**3
    )  # 3 more years of growth
    avg_earnings = (df["earnings_2024_adjusted"] + df["earnings_5yr"]) / 2
    cumulative_5yr = avg_earnings * 5
    df["roi_5yr_w_debt"] = (cumulative_5yr - df["estimated_debt"]) / df[
        "estimated_debt"
    ]
    df["roi_5yr_w_tuition"] = (cumulative_5yr - df["total_tuition"]) / df[
        "total_tuition"
    ]

    df["earnings_per_dollar_tuition"] = (
        df["earnings_2024_adjusted"] / df["total_tuition"]
    )

    return df


def calculate_roi_all_students(df: pd.DataFrame) -> float:
    return (df["roi_5yr_w_tuition"] * df["enrollment"]).sum() / df["enrollment"].sum()
