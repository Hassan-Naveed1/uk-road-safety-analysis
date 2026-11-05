
from pathlib import Path

import pandas as pd
import pyodbc


# ============================================================
# CONFIGURATION
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data" / "raw"

BATCH_SIZE = 10_000

CONNECTION_STRING = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=UKRoadSafetyDB;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)

DATASETS = [
    {
        "name": "Collisions",
        "file": DATA_DIR / "collisions" /
        "dft-road-casualty-statistics-collision-last-5-years.csv",
        "table": "stg.Collisions",
        "expected": 513801,
    },
    {
        "name": "Vehicles",
        "file": DATA_DIR / "vehicles" /
        "dft-road-casualty-statistics-vehicle-last-5-years.csv",
        "table": "stg.Vehicles",
        "expected": 937265,
    },
    {
        "name": "Casualties",
        "file": DATA_DIR / "casualties" /
        "dft-road-casualty-statistics-casualty-last-5-years.csv",
        "table": "stg.Casualties",
        "expected": 652821,
    },
]


# ============================================================
# IMPORT FUNCTION
# ============================================================

def import_dataset(connection, dataset):

    name = dataset["name"]
    file_path = dataset["file"]
    table = dataset["table"]
    expected = dataset["expected"]

    print("\n" + "=" * 65)
    print(f"IMPORTING {name.upper()}")
    print("=" * 65)

    if not file_path.exists():
        raise FileNotFoundError(file_path)

    imported_records = 0
    cursor = connection.cursor()

    # Read CSV in batches without automatically interpreting
    # numerical codes as missing values.
    for chunk in pd.read_csv(
        file_path,
        dtype=str,
        keep_default_na=False,
        chunksize=BATCH_SIZE
    ):

        columns = list(chunk.columns)

        column_sql = ", ".join(
            f"[{column}]" for column in columns
        )

        placeholders = ", ".join(
            "?" for _ in columns
        )

        insert_sql = (
            f"INSERT INTO {table} ({column_sql}) "
            f"VALUES ({placeholders})"
        )

        # Convert empty CSV fields to SQL NULL.
        records = [
            tuple(None if value == "" else value for value in row)
            for row in chunk.itertuples(index=False, name=None)
        ]

        cursor.fast_executemany = True
        cursor.executemany(insert_sql, records)

        connection.commit()

        imported_records += len(records)

        print(
            f"Imported {imported_records:,} / {expected:,} records",
            flush=True
        )

    cursor.close()

    print(f"\n{name} import completed.")
    print(f"Total imported: {imported_records:,}")

    if imported_records != expected:
        raise ValueError(
            f"{name}: expected {expected:,} records, "
            f"but imported {imported_records:,}."
        )

    return imported_records


# ============================================================
# MAIN IMPORT PROCESS
# ============================================================

def main():

    print("=" * 65)
    print("UK ROAD SAFETY DATA IMPORT")
    print("=" * 65)

    total_expected = sum(
        dataset["expected"] for dataset in DATASETS
    )

    print(f"Expected total records: {total_expected:,}")
    print(f"Batch size: {BATCH_SIZE:,}")

    connection = pyodbc.connect(CONNECTION_STRING)

    try:
        cursor = connection.cursor()

        # Clear staging tables before a fresh import.
        print("\nClearing existing staging tables...")

        cursor.execute("TRUNCATE TABLE stg.Casualties")
        cursor.execute("TRUNCATE TABLE stg.Vehicles")
        cursor.execute("TRUNCATE TABLE stg.Collisions")

        connection.commit()
        cursor.close()

        total_imported = 0

        for dataset in DATASETS:
            total_imported += import_dataset(
                connection,
                dataset
            )

        print("\n" + "=" * 65)
        print("IMPORT SUMMARY")
        print("=" * 65)

        print(f"Total records imported: {total_imported:,}")
        print(f"Expected records:       {total_expected:,}")

        if total_imported == total_expected:
            print("\nSUCCESS: All datasets imported successfully.")

    finally:
        connection.close()


if __name__ == "__main__":
    main()
