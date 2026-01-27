from typing import Optional
import pandas as pd
import zipfile
from pathlib import Path

import requests
from configs import (
    EARNINGS_FIELD_MAP,
    ENROLLMENTS_FIELD_MAP,
    STAT_CAN_TABLES,
    TUITION_FIELD_MAP,
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


def normalize_field_names(
    df: pd.DataFrame, field_map: dict, field_col: str = "Field of study"
) -> pd.DataFrame:
    df = df.copy()

    df[field_col] = df[field_col].str.replace(r"\s*\[\d+\]$", "", regex=True)

    df["field"] = df[field_col].map(field_map)

    unmapped = df[df["field"].isna()][field_col].unique()
    if len(unmapped) > 0:
        print(f"Unmapped fields: {unmapped}")

    return df.dropna(subset=["field"])


def main():
    # data = fetch_all_statcan_tables(STAT_CAN_TABLES)

    # for table_id, table_data in data.items():
    #     print(f"ID: {table_id}")
    #     print("=" * 50)
    #     print(table_data.head(5))
    #     print(table_data.columns)
    #     print(table_data.dtypes)

    #     subset = table_data[table_data["GEO"] == "Canada"]
    #     subset.groupby("REF_DATE")["VALUE"].mean().plot()
    #     plt.savefig(f"figures/{table_id}.png", dpi=300)
    #     plt.close()

    # ISOLATE RELEVANT DATA FOR TUITION
    tuition_data = filter_statcan_data(
        fetch_statcan_table(STAT_CAN_TABLES["tuition"]),
        ["2022/2023", "2023/2024", "2024/2025"],
        field_of_study_exclude=["Total, field of study"],
    )

    # print(tuition_data[["REF_DATE", "Field of study", "VALUE"]])

    # ISOLATE RELEVANT DATA FOR EARNINGS
    earnings_data = filter_statcan_data(
        fetch_statcan_table(STAT_CAN_TABLES["earnings"]),
        [2015, 2016, 2017],
        field_of_study_exclude=["Total, field of study"],
    )

    earnings_by_major = (
        earnings_data.groupby(["REF_DATE", "Field of study"])["VALUE"]
        .mean()
        .reset_index()
    )

    # print(earnings_by_major)

    # ISOLATE RELEVANT DATA FOR DEBT
    debt_data = filter_statcan_data(
        fetch_statcan_table(STAT_CAN_TABLES["debt"]),
        [2015, 2020],
        level_of_study_include=["Bachelor's"],
    )

    percent_debt = get_debt_subset(
        debt_data, "Percentage of graduates who owed debt to the source at graduation"
    )

    dollar_debt = get_debt_subset(
        debt_data, "Average debt owed to the source at graduation"
    )

    percent_summary = pivot_debt_by_source(percent_debt)
    dollar_summary = pivot_debt_by_source(dollar_debt)

    percent_summary = rename_debt_subset(percent_summary, "%")
    dollar_summary = rename_debt_subset(dollar_summary, "$")

    combined = pd.concat([percent_summary, dollar_summary], axis=1)

    # print(combined)

    # ISOLATE RELEVANT DATA FOR ENROLLMENTS
    enrollment_data = filter_statcan_data(
        fetch_statcan_table(STAT_CAN_TABLES["enrollments"]),
        ["2022/2023", "2023/2024", "2024/2025"],
        field_of_study_exclude=["Total, field of study"],
    )

    enrollment_summary = (
        enrollment_data.groupby(["REF_DATE", "Field of study"])["VALUE"]
        .sum()
        .reset_index()
    )

    # print(enrollment_summary)

    tuition = normalize_field_names(
        tuition_data[["REF_DATE", "Field of study", "VALUE"]], TUITION_FIELD_MAP
    )

    earnings = normalize_field_names(earnings_by_major, EARNINGS_FIELD_MAP)

    enrollment = normalize_field_names(enrollment_summary, ENROLLMENTS_FIELD_MAP)

    print(tuition)
    print(earnings)
    print(enrollment)
    print(combined)


if __name__ == "__main__":
    main()
