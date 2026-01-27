import pandas as pd
import zipfile
from pathlib import Path

import requests
from configs import STAT_CAN_TABLES, YEARS_TO_KEEP
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


def map_to_fields(table_data: pd.DataFrame, field_maps: list[str]):
    pass


def main():
    data = fetch_all_statcan_tables(STAT_CAN_TABLES)
    # for table, table_id in STAT_CAN_TABLES.items():
    #     print(f"\nTABLE: {table} | ID: {table_id}")
    #     print("=" * 50)
    #     df = fetch_statcan_table(table_id)
    #     print(f"Shape: {df.shape}")

    #     # Show all columns without truncation
    #     pd.set_option("display.max_columns", None)
    #     pd.set_option("display.width", None)
    #     print(df.head().to_string())

    # for table_id, table_data in data.items():
    #     print(f"ID: {table_id}")
    #     print("=" * 50)

    #     print(f"Shape: {table_data.shape}")
    #     pd.set_option("display.max_columns", None)
    #     pd.set_option("display.width", None)
    #     print(table_data.head().to_string())
    for table_id, table_data in data.items():
        print(f"ID: {table_id}")
        print("=" * 50)
        print(table_data.head(5))
        print(table_data.columns)
        print(table_data.dtypes)

        subset = table_data[table_data["GEO"] == "Canada"]
        subset.groupby("REF_DATE")["VALUE"].mean().plot()
        plt.savefig(f"figures/{table_id}.png", dpi=300)
        plt.close()


if __name__ == "__main__":
    main()
