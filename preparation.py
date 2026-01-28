import pandas as pd

from configs import (
    CPI_ADJUSTMENT_2018_TO_2024,
    CPI_ADJUSTMENT_2020_TO_2024,
    EARNINGS_FIELD_MAP,
    ENROLLMENTS_FIELD_MAP,
    TUITION_FIELD_MAP,
)
from normalization import normalize_field_names, normalize_ref_date


def prepare_tuition_data(df: pd.DataFrame) -> pd.DataFrame:
    normalized = normalize_field_names(df, TUITION_FIELD_MAP)
    normalized = normalize_ref_date(normalized)

    latest_year = normalized["REF_DATE"].max()
    latest = normalized[normalized["REF_DATE"] == latest_year]

    return (
        latest.groupby(["REF_DATE", "field"])["VALUE"]
        .mean()
        .reset_index()
        .rename(columns={"VALUE": "tuition"})
    )


def prepare_earnings_data(df: pd.DataFrame) -> pd.DataFrame:
    normalized = normalize_field_names(df, EARNINGS_FIELD_MAP)
    normalized = normalize_ref_date(normalized)

    latest_year = normalized["REF_DATE"].max()
    latest = normalized[normalized["REF_DATE"] == latest_year]

    result = (
        latest.groupby(["REF_DATE", "field"])["VALUE"]
        .mean()
        .reset_index()
        .rename(columns={"VALUE": "earnings_2018"})
    )

    result["earnings_2024_adjusted"] = (
        result["earnings_2018"] * CPI_ADJUSTMENT_2018_TO_2024
    )

    return result[["REF_DATE", "field", "earnings_2018", "earnings_2024_adjusted"]]


def prepare_enrollment_data(df: pd.DataFrame) -> pd.DataFrame:
    normalized = normalize_field_names(df, ENROLLMENTS_FIELD_MAP)
    normalized = normalize_ref_date(normalized)

    latest_year = normalized["REF_DATE"].max()
    latest = normalized[normalized["REF_DATE"] == latest_year]

    return (
        latest.groupby(["REF_DATE", "field"])["VALUE"]
        .sum()
        .reset_index()
        .rename(columns={"VALUE": "enrollment"})
    )


def prepare_debt_data(df: pd.DataFrame) -> pd.DataFrame:
    df = normalize_ref_date(df)

    latest_year = df["REF_DATE"].max()
    latest = df[df["REF_DATE"] == latest_year]

    latest = latest[
        (
            latest["Statistics"].str.contains(
                "Average debt owed to the source at graduation"
            )
        )
    ]

    latest = latest[
        latest["Type of debt source"]
        == "Graduates who owed money for their education to any source (government or non-government)"
    ]

    latest = latest[["REF_DATE", "VALUE"]].rename(columns={"VALUE": "debt_2018"})

    latest["debt_2024"] = latest["debt_2018"] * CPI_ADJUSTMENT_2020_TO_2024

    return latest


def estimate_debt_by_fields(avg_debt: float, df_tuition: pd.DataFrame) -> pd.DataFrame:
    df = df_tuition.copy()

    avg_tuition = df["tuition"].mean()
    df["estimated_debt"] = (df["tuition"] / avg_tuition) * avg_debt

    return df


def merge_dfs(
    df_tuition: pd.DataFrame,
    df_earnings: pd.DataFrame,
    df_enrollment: pd.DataFrame,
    df_debt: pd.DataFrame,
) -> pd.DataFrame:
    return (
        df_tuition.drop(columns="REF_DATE")
        .merge(df_earnings.drop(columns="REF_DATE"), on="field", how="inner")
        .merge(df_debt.drop(columns=["REF_DATE", "tuition"]), on="field", how="left")
        .merge(df_enrollment.drop(columns="REF_DATE"), on="field", how="left")
    )
