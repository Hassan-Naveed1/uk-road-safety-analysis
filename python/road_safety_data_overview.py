
from pathlib import Path
import pandas as pd

# --------------------------------------------------
# PROJECT CONFIGURATION
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = PROJECT_DIR / "data" / "raw"

DATASETS = {
    "Collisions": RAW_DATA_DIR / "collisions",
    "Vehicles": RAW_DATA_DIR / "vehicles",
    "Casualties": RAW_DATA_DIR / "casualties",
}


def inspect_dataset(name, folder):

    print("\n" + "=" * 75)
    print(f"{name.upper()} DATASET")
    print("=" * 75)

    csv_files = list(folder.glob("*.csv"))

    if len(csv_files) != 1:
        raise FileNotFoundError(
            f"Expected one CSV file in {folder}, found {len(csv_files)}"
        )

    file_path = csv_files[0]

    print(f"\nFile: {file_path.name}")
    print(f"File size: {file_path.stat().st_size / (1024 ** 2):.2f} MB")

    # Load dataset
    df = pd.read_csv(file_path, low_memory=False)

    # Basic information
    print("\n--- DATASET OVERVIEW ---")
    print(f"Total records: {len(df):,}")
    print(f"Total columns: {len(df.columns):,}")
    print(f"Memory usage: {df.memory_usage(deep=True).sum() / (1024 ** 2):.2f} MB")

    # Column information
    print("\n--- COLUMN INFORMATION ---")

    column_info = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str).values,
        "Missing Values": df.isnull().sum().values,
        "Missing Percentage": (
            df.isnull().mean().values * 100
        ).round(2),
        "Unique Values": df.nunique().values
    })

    print(column_info.to_string(index=False))

    # Duplicate records
    print("\n--- DUPLICATE ANALYSIS ---")
    print(f"Duplicate rows: {df.duplicated().sum():,}")

    # Missing values
    print("\n--- MISSING VALUE SUMMARY ---")

    missing = df.isnull().sum()
    missing = missing[missing > 0].sort_values(ascending=False)

    if missing.empty:
        print("No missing values detected.")
    else:
        print(missing.to_string())

    # Potential identifier columns
    print("\n--- POTENTIAL IDENTIFIER COLUMNS ---")

    identifiers = [
        column for column in df.columns
        if any(term in column.lower()
               for term in ["index", "reference", "id"])
    ]

    if identifiers:
        for column in identifiers:
            print(
                f"{column}: "
                f"{df[column].nunique(dropna=True):,} unique values"
            )
    else:
        print("No obvious identifier columns found.")

    # Sample records
    print("\n--- FIRST FIVE RECORDS ---")
    print(df.head().to_string(index=False))

    return df


def main():

    print("=" * 75)
    print("UK ROAD SAFETY DATA OVERVIEW")
    print("=" * 75)

    datasets = {}

    for name, folder in DATASETS.items():
        datasets[name] = inspect_dataset(name, folder)

    print("\n" + "=" * 75)
    print("DATA INSPECTION COMPLETED")
    print("=" * 75)

    return datasets


if __name__ == "__main__":
    main()
