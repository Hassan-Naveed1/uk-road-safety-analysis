
from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data" / "raw"

datasets = {
    "Collisions": DATA_DIR / "collisions" / "dft-road-casualty-statistics-collision-last-5-years.csv",
    "Vehicles": DATA_DIR / "vehicles" / "dft-road-casualty-statistics-vehicle-last-5-years.csv",
    "Casualties": DATA_DIR / "casualties" / "dft-road-casualty-statistics-casualty-last-5-years.csv"
}

for name, file_path in datasets.items():

    print("\n" + "=" * 75)
    print(f"{name.upper()} - COLUMN DATA TYPES")
    print("=" * 75)

    df = pd.read_csv(file_path, low_memory=False)

    for column, dtype in df.dtypes.items():
        print(f"{column:<65} {dtype}")

    del df

print("\nSchema inspection completed.")
