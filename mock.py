import pandas as pd


def make_mock_merged_df() -> pd.DataFrame:
    data = {
        "field": [
            "agriculture",
            "business",
            "comp_sci",
            "education",
            "health",
            "humanities",
            "other",
            "personal_services",
            "physical_sciences",
            "social_sciences",
            "visual_arts",
        ],
        "tuition": [6200, 7200, 8000, 6500, 7800, 6000, 6100, 6700, 7600, 6900, 5800],
        "earnings_2018": [
            42000,
            52000,
            60000,
            48000,
            58000,
            36000,
            37000,
            45000,
            50000,
            49000,
            33000,
        ],
        "earnings_2024_adjusted": [
            50000,
            62000,
            72000,
            58000,
            70000,
            43000,
            44000,
            53000,
            60000,
            59000,
            40000,
        ],
        "estimated_debt": [
            18000,
            23000,
            26000,
            20000,
            25000,
            17000,
            17500,
            21000,
            24000,
            22000,
            16000,
        ],
        "enrollment": [
            18000,
            95000,
            70000,
            45000,
            85000,
            30000,
            20000,
            25000,
            35000,
            60000,
            15000,
        ],
    }

    df = pd.DataFrame(data)

    # Derived fields (same logic as your pipeline)
    YEARS_OF_TUITION = 4
    TAX_RATE = 0.25
    INCOME_TO_PAYOFF = 0.10
    RATE_OF_EARNING_GROWTH = 1.03

    df["total_tuition"] = df["tuition"] * YEARS_OF_TUITION
    df["debt_to_income"] = df["estimated_debt"] / df["earnings_2024_adjusted"]

    post_tax = df["earnings_2024_adjusted"] * (1 - TAX_RATE)
    annual_payment = post_tax * INCOME_TO_PAYOFF
    df["payback_years"] = df["estimated_debt"] / annual_payment

    df["earnings_5yr"] = df["earnings_2024_adjusted"] * (RATE_OF_EARNING_GROWTH**3)
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
