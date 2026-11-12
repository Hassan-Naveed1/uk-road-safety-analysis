import pandas as pd
from pathlib import Path

# Project directory
PROJECT_DIR = Path(__file__).resolve().parent.parent

# Collisions dataset location
DATA_FILE = PROJECT_DIR / "data" / "raw" / "collisions" / "dft-road-casualty-statistics-collision-last-5-years.csv"

# Load dataset
df = pd.read_csv(DATA_FILE, low_memory=False, keep_default_na=False)

print("=" * 60)
print("COLLISIONS DATASET PROFILE")
print("=" * 60)

print(f"\nNumber of records: {len(df):,}")
print(f"Number of columns: {len(df.columns)}")


# Column-level overview
column_profile = pd.DataFrame({
    "column_name": df.columns,
    "data_type": df.dtypes.astype(str).values,
    "missing_values": (df.isna() | df.eq("")).sum().values,
    "unique_values": df.nunique(dropna=False).values
})

print("\n" + "=" * 60)
print("COLUMN OVERVIEW")
print("=" * 60)

print(column_profile.to_string(index=False))


# Save column profile
OUTPUT_DIR = PROJECT_DIR / "data" / "processed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "collisions_column_profile.csv"

column_profile.to_csv(OUTPUT_FILE, index=False)

print(f"\nColumn profile saved to: {OUTPUT_FILE}")

# Collision severity distribution
severity_summary = (
    df["collision_severity"]
    .value_counts()
    .sort_index()
    .reset_index()
)

severity_summary.columns = ["severity_code", "collision_count"]

severity_summary["percentage"] = (
    severity_summary["collision_count"] / len(df) * 100
).round(2)

print("\n" + "=" * 60)
print("COLLISION SEVERITY DISTRIBUTION")
print("=" * 60)

print(severity_summary.to_string(index=False))

import matplotlib.pyplot as plt

# Collision severity chart
severity_labels = {
    1: "Fatal",
    2: "Serious",
    3: "Slight"
}

severity_summary["severity"] = severity_summary["severity_code"].map(severity_labels)

plt.figure(figsize=(9, 5))

bars = plt.bar(
    severity_summary["severity"],
    severity_summary["collision_count"]
)

plt.title("UK Road Collisions by Severity (2021–2025)")
plt.xlabel("Collision Severity")
plt.ylabel("Number of Collisions")

plt.bar_label(bars, fmt="%.0f", padding=3)

plt.tight_layout()

plt.savefig(
    PROJECT_DIR / "visualisations" / "02_collision_severity.png",
    dpi=300
)

plt.show()
plt.close()