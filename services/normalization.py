from typing import Optional
import pandas as pd


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
