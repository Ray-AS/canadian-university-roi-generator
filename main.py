from typing import Optional
import pandas as pd
import zipfile
from pathlib import Path

import requests
from configs import (
    CPI_ADJUSTMENT_2018_TO_2024,
    CPI_ADJUSTMENT_2020_TO_2024,
    EARNINGS_FIELD_MAP,
    ENROLLMENTS_FIELD_MAP,
    INCOME_TO_PAYOFF,
    RATE_OF_EARNING_GROWTH,
    STAT_CAN_TABLES,
    TAX_RATE,
    TUITION_FIELD_MAP,
    YEARS_OF_TUITION,
    YEARS_TO_KEEP,
)
import matplotlib.pyplot as plt


def fetch_statcan_table(table_id: str, path: Path = Path("data/raw")) -> pd.DataFrame:
    clean_id = table_id.replace("-", "")
    path.mkdir(parents=True, exist_ok=True)

    zip_path = path / f"{clean_id[:-2]}-eng.zip"

    # Try to use cached file first
    if zip_path.exists():
        print(f"Using cached {table_id}...")
    else:
        # Download directly
        print(f"Downloading {table_id}...")
        url = f"https://www150.statcan.gc.ca/n1/tbl/csv/{clean_id[:-2]}-eng.zip"

        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

        if response.status_code != 200:
            raise Exception(f"Failed to download {table_id}: {response.status_code}")

        # Save the zip
        zip_path.write_bytes(response.content)
        print(f"Saved to {zip_path}")

    # Read the ZIP
    with zipfile.ZipFile(zip_path) as z:
        csv_files = [
            f for f in z.namelist() if f.endswith(".csv") and "MetaData" not in f
        ]
        if not csv_files:
            raise Exception(f"No data CSV found. Contents: {z.namelist()}")

        with z.open(csv_files[0]) as f:
            # df = pd.read_csv(f)
            chunks = pd.read_csv(f, chunksize=10000)
            df_filtered = pd.concat(
                [
                    chunk[
                        chunk["REF_DATE"]
                        .astype(str)
                        .str[
                            :4
                        ]  # Take only the first 4 characters (the year) (Tuition and enrollments use e.g. "2015/2016"; read instead as "2015")
                        .isin([str(y) for y in YEARS_TO_KEEP])
                    ]
                    for chunk in chunks
                    if "REF_DATE" in chunk.columns
                ],
                ignore_index=True,
            )

    return df_filtered


def fetch_all_statcan_tables(sources: dict[str, str]) -> dict[str, pd.DataFrame]:
    data = {}

    for name, table_id in sources.items():
        data[name] = fetch_statcan_table(table_id)

    return data


def filter_statcan_data(
    df: pd.DataFrame,
    years_include: list[str] | list[int],
    locations_include: list[str] = ["Canada"],
    level_of_study_include: Optional[list[str]] = None,
    field_of_study_exclude: Optional[list[str]] = None,
):
    subset = df[
        (df["REF_DATE"].isin(years_include)) & (df["GEO"].isin(locations_include))
    ]

    if field_of_study_exclude is not None:
        subset = subset[(~subset["Field of study"].isin(field_of_study_exclude))]
    if level_of_study_include is not None:
        subset = subset[(subset["Level of study"].isin(level_of_study_include))]

    return subset


def get_debt_subset(df: pd.DataFrame, subset: str):
    return df[df["Statistics"].str.contains(subset)]


def rename_debt_subset(df: pd.DataFrame, unit: str):
    return df.rename(
        columns={
            "Graduates who owed money for their education to any source (government or non-government)": f"{unit} in debt",
            "Graduates who owed money for their education to government-sponsored student loans": f"Govt loans {unit}",
            "Graduates who owed money for their education to non-government sources": f"Private loans {unit}",
        }
    )


def pivot_debt_by_source(df: pd.DataFrame):
    return df.pivot_table(
        index="REF_DATE", columns="Type of debt source", values="VALUE"
    )


def normalize_ref_date(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["REF_DATE"] = df["REF_DATE"].astype(str).str[:4].astype(int)
    return df


def normalize_field_names(
    df: pd.DataFrame, field_map: dict, field_col: str = "Field of study"
) -> pd.DataFrame:
    df = df.copy()

    df[field_col] = df[field_col].str.replace(r"\s*\[\d+\]$", "", regex=True)

    df["field"] = df[field_col].map(field_map)

    # unmapped = df[df["field"].isna()][field_col].unique()
    # if len(unmapped) > 0:
    #     print(f"Unmapped fields: {unmapped}")

    return df.dropna(subset=["field"])


def prepare_tuition_data(df: pd.DataFrame) -> pd.DataFrame:
    normalized = normalize_field_names(df, TUITION_FIELD_MAP)
    normalized = normalize_ref_date(normalized)

    # latest_year = max(normalized["REF_DATE"].unique(), key=lambda s: int(s[:4]))
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

    # latest_year = max(normalized["REF_DATE"].unique(), key=lambda s: int(s[:4]))
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


def main():
    tuition_data = filter_statcan_data(
        fetch_statcan_table(STAT_CAN_TABLES["tuition"]),
        ["2020/2021", "2021/2022", "2022/2023", "2023/2024", "2024/2025"],
        field_of_study_exclude=["Total, field of study"],
    )

    prepared_tuition_data = prepare_tuition_data(tuition_data)

    earnings_data = filter_statcan_data(
        fetch_statcan_table(STAT_CAN_TABLES["earnings"]),
        [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025],
        field_of_study_exclude=["Total, field of study"],
    )

    earnings_by_major = (
        earnings_data.groupby(["REF_DATE", "Field of study"])["VALUE"]
        .mean()
        .reset_index()
    )

    prepared_earnings_data = prepare_earnings_data(earnings_by_major)

    enrollment_data = filter_statcan_data(
        fetch_statcan_table(STAT_CAN_TABLES["enrollments"]),
        ["2020/2021", "2021/2022", "2022/2023", "2023/2024", "2024/2025"],
        field_of_study_exclude=["Total, field of study"],
    )

    enrollment_summary = (
        enrollment_data.groupby(["REF_DATE", "Field of study"])["VALUE"]
        .sum()
        .reset_index()
    )

    prepared_enrollment_data = prepare_enrollment_data(enrollment_summary)

    debt_data = filter_statcan_data(
        fetch_statcan_table(STAT_CAN_TABLES["debt"]),
        [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025],
        level_of_study_include=["Bachelor's"],
    )

    prepared_debt_data = prepare_debt_data(debt_data)
    debts_by_field = estimate_debt_by_fields(
        prepared_debt_data["debt_2024"].iloc[0], prepared_tuition_data
    )

    merged = merge_dfs(
        prepared_tuition_data,
        prepared_earnings_data,
        prepared_enrollment_data,
        debts_by_field,
    )

    merged_w_roi = calculate_roi_by_field(merged)

    print("-----------------------TUITION-----------------------")
    print(prepared_tuition_data)
    print("-----------------------EARNINGS-----------------------")
    print(prepared_earnings_data)
    print("-----------------------ENROLLMENT-----------------------")
    print(prepared_enrollment_data)
    print("-----------------------DEBT-----------------------")
    print(debts_by_field)
    print(merged_w_roi)


if __name__ == "__main__":
    main()
