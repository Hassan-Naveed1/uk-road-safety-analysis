import pandas as pd
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = (
    BASE_DIR
    / "data"
    / "raw"
    / "casualties"
    / "dft-road-casualty-statistics-casualty-last-5-years.csv"
)

# Load dataset
df = pd.read_csv(
    DATA_FILE,
    low_memory=False,
    keep_default_na=False
)

print("=" * 60)
print("CASUALTIES DATASET PROFILE")
print("=" * 60)

print(f"\nNumber of records: {len(df):,}")
print(f"Number of columns: {len(df.columns)}")

print("\nCOLUMN NAMES:")
for column in df.columns:
    print(column)

print("\nDATA TYPES:")
print(df.dtypes)

print("\nFIRST 5 RECORDS:")
print(df.head())

print("\n" + "=" * 60)
print("MISSING AND BLANK VALUES")
print("=" * 60)

missing_profile = pd.DataFrame({
    "Missing Values": df.isna().sum(),
    "Blank Values": df.eq("").sum(),
    "Unique Values": df.nunique()
})

missing_profile["Total Missing/Blank"] = (
    missing_profile["Missing Values"]
    + missing_profile["Blank Values"]
)

missing_profile["Missing Percentage"] = (
    missing_profile["Total Missing/Blank"] / len(df) * 100
)

print(missing_profile.to_string())

print("\n" + "=" * 60)
print("UNIQUE VALUES IN CATEGORICAL COLUMNS")
print("=" * 60)

categorical_columns = [
    "casualty_class",
    "sex_of_casualty",
    "age_band_of_casualty",
    "casualty_severity",
    "pedestrian_location",
    "pedestrian_movement",
    "car_passenger",
    "bus_or_coach_passenger",
    "pedestrian_road_maintenance_worker",
    "casualty_type",
    "casualty_imd_decile",
    "enhanced_casualty_severity",
    "casualty_injury_based",
    "casualty_distance_banding",
    "escooter_flag"
]

for column in categorical_columns:
    print(f"\n{column}")
    print(df[column].value_counts().sort_index().to_string())


    print("\n" + "=" * 60)
print("DUPLICATE AND IDENTIFIER CHECKS")
print("=" * 60)

# Exact duplicate rows
print("\nExact duplicate rows:")
print(df.duplicated().sum())

# Check casualty identifier combinations
print("\nDuplicate collision_index + casualty_reference:")
print(
    df.duplicated(
        subset=["collision_index", "casualty_reference"]
    ).sum()
)

# Check full casualty identifier combinations
print("\nDuplicate collision_index + vehicle_reference + casualty_reference:")
print(
    df.duplicated(
        subset=[
            "collision_index",
            "vehicle_reference",
            "casualty_reference"
        ]
    ).sum()
)

print("\n" + "=" * 60)
print("CASUALTY RELATIONSHIP CHECKS")
print("=" * 60)

# Load collisions and vehicles
collisions_file = (
    BASE_DIR / "data" / "raw" / "collisions"
    / "dft-road-casualty-statistics-collision-last-5-years.csv"
)

vehicles_file = (
    BASE_DIR / "data" / "raw" / "vehicles"
    / "dft-road-casualty-statistics-vehicle-last-5-years.csv"
)

collisions_df = pd.read_csv(
    collisions_file,
    usecols=["collision_index"],
    low_memory=False
)

vehicles_df = pd.read_csv(
    vehicles_file,
    usecols=["collision_index", "vehicle_reference"],
    low_memory=False
)

# Check casualty-to-collision relationships
collision_ids = set(collisions_df["collision_index"])

unmatched_collisions = (
    ~df["collision_index"].isin(collision_ids)
).sum()

print(f"\nUnmatched casualty-to-collision records: {unmatched_collisions:,}")

# Check casualty-to-vehicle relationships
vehicle_keys = pd.MultiIndex.from_frame(
    vehicles_df[["collision_index", "vehicle_reference"]]
)

casualty_keys = pd.MultiIndex.from_frame(
    df[["collision_index", "vehicle_reference"]]
)

unmatched_vehicles = (~casualty_keys.isin(vehicle_keys)).sum()

print(f"Unmatched casualty-to-vehicle records: {unmatched_vehicles:,}")


import matplotlib.pyplot as plt

# Casualty severity labels
severity_labels = {
    1: "Fatal",
    2: "Serious",
    3: "Slight"
}

# Count casualties by severity
severity_counts = df["casualty_severity"].value_counts().sort_index()

# Replace numeric codes with labels
severity_counts.index = [
    severity_labels[code] for code in severity_counts.index
]

# Calculate percentages
severity_percentages = (
    severity_counts / severity_counts.sum() * 100
)

# Create chart
plt.figure(figsize=(10, 6))

bars = plt.bar(
    severity_counts.index,
    severity_counts.values
)

plt.title("Casualties by Severity (2021–2025)")
plt.xlabel("Casualty Severity")
plt.ylabel("Number of Casualties")
plt.grid(axis="y", alpha=0.3)

# Add count and percentage labels
for bar, count, percentage in zip(
    bars,
    severity_counts.values,
    severity_percentages.values
):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f"{count:,}\n({percentage:.2f}%)",
        ha="center",
        va="bottom"
    )

plt.tight_layout()

# Save chart
output_dir = BASE_DIR / "visualisations"
output_dir.mkdir(parents=True, exist_ok=True)

plt.savefig(
    output_dir / "01_casualties_by_severity.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# Casualties by year
yearly_casualties = df["collision_year"].value_counts().sort_index()

plt.figure(figsize=(10, 6))

bars = plt.bar(
    yearly_casualties.index.astype(str),
    yearly_casualties.values
)

plt.title("Total Casualties by Year (2021–2025)")
plt.xlabel("Year")
plt.ylabel("Number of Casualties")
plt.grid(axis="y", alpha=0.3)

for bar, count in zip(bars, yearly_casualties.values):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f"{count:,}",
        ha="center",
        va="bottom"
    )

plt.tight_layout()

plt.savefig(
    output_dir / "02_casualties_by_year.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("\nCASUALTIES BY YEAR:")
print(yearly_casualties.to_string())

# Casualties by class
class_labels = {
    1: "Driver / Rider",
    2: "Passenger",
    3: "Pedestrian"
}

class_counts = df["casualty_class"].value_counts().sort_index()
class_counts.index = [
    class_labels[code] for code in class_counts.index
]

class_percentages = class_counts / class_counts.sum() * 100

plt.figure(figsize=(10, 6))

bars = plt.bar(class_counts.index, class_counts.values)

plt.title("Casualties by Class (2021–2025)")
plt.xlabel("Casualty Class")
plt.ylabel("Number of Casualties")
plt.grid(axis="y", alpha=0.3)

for bar, count, percentage in zip(
    bars, class_counts.values, class_percentages.values
):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f"{count:,}\n({percentage:.2f}%)",
        ha="center",
        va="bottom"
    )

plt.tight_layout()

plt.savefig(
    output_dir / "03_casualties_by_class.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("\nCASUALTIES BY CLASS:")
print(class_counts.to_string())

# Casualties by sex
sex_labels = {
    -1: "Missing / Out of Range",
    1: "Male",
    2: "Female",
    9: "Unknown"
}

sex_counts = df["sex_of_casualty"].value_counts().sort_index()
sex_counts.index = [sex_labels[code] for code in sex_counts.index]

sex_percentages = sex_counts / sex_counts.sum() * 100

plt.figure(figsize=(10, 6))
plt.ylim(0, 450000)

bars = plt.bar(sex_counts.index, sex_counts.values)

plt.title("Casualties by Sex (2021–2025)")
plt.xlabel("Sex")
plt.ylabel("Number of Casualties")
plt.grid(axis="y", alpha=0.3)

for bar, count, percentage in zip(
    bars, sex_counts.values, sex_percentages.values
):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f"{count:,}\n({percentage:.2f}%)",
        ha="center",
        va="bottom"
    )

plt.tight_layout()

plt.savefig(
    output_dir / "04_casualties_by_sex.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# Casualties by age band
age_band_labels = {
    -1: "Missing / Out of Range",
    1: "0–5",
    2: "6–10",
    3: "11–15",
    4: "16–20",
    5: "21–25",
    6: "26–35",
    7: "36–45",
    8: "46–55",
    9: "56–65",
    10: "66–75",
    11: "Over 75"
}

age_band_counts = (
    df["age_band_of_casualty"]
    .value_counts()
    .sort_index()
)

age_band_counts.index = [
    age_band_labels[code] for code in age_band_counts.index
]

age_band_percentages = (
    age_band_counts / age_band_counts.sum() * 100
)

plt.figure(figsize=(12, 6))

bars = plt.bar(
    age_band_counts.index,
    age_band_counts.values
)

plt.title("Casualties by Age Band (2021–2025)")
plt.xlabel("Age Band")
plt.ylabel("Number of Casualties")
plt.xticks(rotation=30, ha="right")
plt.grid(axis="y", alpha=0.3)

for bar, count, percentage in zip(
    bars,
    age_band_counts.values,
    age_band_percentages.values
):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f"{count:,}\n({percentage:.1f}%)",
        ha="center",
        va="bottom",
        fontsize=8
    )

plt.ylim(0, age_band_counts.max() * 1.15)
plt.tight_layout()

plt.savefig(
    output_dir / "05_casualties_by_age_band.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("\nCASUALTIES BY AGE BAND:")
print(age_band_counts.to_string())

# Casualties by exact age
valid_ages = df.loc[
    df["age_of_casualty"] >= 0,
    "age_of_casualty"
]

plt.figure(figsize=(12, 6))

plt.hist(
    valid_ages,
    bins=range(0, 111, 5),
    edgecolor="black"
)

plt.title("Casualties by Exact Age (2021–2025)")
plt.xlabel("Age")
plt.ylabel("Number of Casualties")
plt.xticks(range(0, 111, 5))
plt.grid(axis="y", alpha=0.3)

plt.tight_layout()

plt.savefig(
    output_dir / "06_casualties_by_exact_age.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("\nEXACT AGE STATISTICS:")
print(f"Valid age records: {len(valid_ages):,}")
print(f"Mean age: {valid_ages.mean():.2f}")
print(f"Median age: {valid_ages.median():.0f}")
print(f"Minimum age: {valid_ages.min()}")
print(f"Maximum age: {valid_ages.max()}")
print(f"Missing/out-of-range: {(df['age_of_casualty'] == -1).sum():,}")

# Casualties by type
casualty_type_labels = {
    -1: "Missing / Out of Range",
    0: "Pedestrian",
    1: "Cyclist",
    2: "Motorcycle <=50cc",
    3: "Motorcycle <=125cc",
    4: "Motorcycle 125-500cc",
    5: "Motorcycle >500cc",
    8: "Taxi / Private Hire",
    9: "Car Occupant",
    10: "Minibus Occupant",
    11: "Bus / Coach Occupant",
    16: "Horse Rider",
    17: "Agricultural Vehicle",
    18: "Tram Occupant",
    19: "Van / Goods <=3.5t",
    20: "Goods Vehicle 3.5-7.5t",
    21: "Goods Vehicle >=7.5t",
    22: "Mobility Scooter",
    23: "Electric Motorcycle",
    33: "Personal Powered Transporter",
    90: "Other Vehicle",
    97: "Motorcycle Unknown CC",
    98: "Goods Vehicle Unknown Weight",
    99: "Unknown"
}

casualty_type_counts = (
    df["casualty_type"].value_counts().sort_index()
)

casualty_type_counts.index = [
    casualty_type_labels[code]
    for code in casualty_type_counts.index
]

plt.figure(figsize=(13, 8))

bars = plt.barh(
    casualty_type_counts.index,
    casualty_type_counts.values
)

plt.title("Casualties by Type (2021–2025)")
plt.xlabel("Number of Casualties")
plt.ylabel("Casualty Type")
plt.grid(axis="x", alpha=0.3)

for bar, count in zip(bars, casualty_type_counts.values):
    plt.text(
        bar.get_width(),
        bar.get_y() + bar.get_height() / 2,
        f" {count:,}",
        va="center",
        fontsize=8
    )

plt.tight_layout()

plt.savefig(
    output_dir / "07_casualties_by_type.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("\nCASUALTIES BY TYPE:")
print(casualty_type_counts.to_string())

# Casualty severity by sex - percentage distribution

severity_sex = pd.crosstab(
    df["sex_of_casualty"],
    df["casualty_severity"],
    normalize="index"
) * 100

severity_sex = severity_sex.rename(
    index={
        -1: "Missing / Out of Range",
        1: "Male",
        2: "Female",
        9: "Unknown"
    },
    columns={
        1: "Fatal",
        2: "Serious",
        3: "Slight"
    }
)

severity_sex = severity_sex.reindex(
    columns=["Fatal", "Serious", "Slight"]
)

ax = severity_sex.plot(
    kind="bar",
    stacked=True,
    figsize=(11, 6)
)

plt.title("Casualty Severity Distribution by Sex (2021–2025)")
plt.xlabel("Sex")
plt.ylabel("Percentage of Casualties")
plt.xticks(rotation=0)
plt.ylim(0, 100)
plt.legend(title="Severity")
plt.grid(axis="y", alpha=0.3)

plt.tight_layout()

plt.savefig(
    output_dir / "08_casualty_severity_by_sex.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("\nCASUALTY SEVERITY BY SEX (%):")
print(severity_sex.round(2).to_string())

# Casualty severity by year

severity_year = pd.crosstab(
    df["collision_year"],
    df["casualty_severity"]
)

severity_year = severity_year.rename(
    columns={
        1: "Fatal",
        2: "Serious",
        3: "Slight"
    }
)

severity_year = severity_year[["Fatal", "Serious", "Slight"]]

ax = severity_year.plot(
    kind="bar",
    figsize=(11, 6)
)

plt.title("Casualty Severity by Year (2021–2025)")
plt.xlabel("Year")
plt.ylabel("Number of Casualties")
plt.xticks(rotation=0)
plt.legend(title="Severity")
plt.grid(axis="y", alpha=0.3)

plt.tight_layout()

plt.savefig(
    output_dir / "09_casualty_severity_by_year.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("\nCASUALTY SEVERITY BY YEAR:")
print(severity_year.to_string())

# Load collision day information
collisions_file = (
    BASE_DIR / "data" / "raw" / "collisions"
    / "dft-road-casualty-statistics-collision-last-5-years.csv"
)

collision_days = pd.read_csv(
    collisions_file,
    usecols=["collision_index", "day_of_week", "time"],
    low_memory=False
)
# Join collision day to casualty records
casualties_with_day = df.merge(
    collision_days,
    on="collision_index",
    how="left",
    validate="many_to_one"
)

print("\nCASUALTY RECORDS WITHOUT A MATCHED DAY:")
print(casualties_with_day["day_of_week"].isna().sum())

# Casualties by day of the week

day_labels = {
    1: "Sunday",
    2: "Monday",
    3: "Tuesday",
    4: "Wednesday",
    5: "Thursday",
    6: "Friday",
    7: "Saturday"
}

day_counts = (
    casualties_with_day["day_of_week"]
    .value_counts()
    .sort_index()
)

day_counts.index = [
    day_labels[day] for day in day_counts.index
]

plt.figure(figsize=(11, 6))

bars = plt.bar(day_counts.index, day_counts.values)

plt.title("Casualties by Day of the Week (2021–2025)")
plt.xlabel("Day of the Week")
plt.ylabel("Number of Casualties")
plt.grid(axis="y", alpha=0.3)

for bar, count in zip(bars, day_counts.values):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f"{count:,}",
        ha="center",
        va="bottom"
    )

plt.ylim(0, day_counts.max() * 1.12)
plt.tight_layout()

plt.savefig(
    output_dir / "10_casualties_by_day.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("\nCASUALTIES BY DAY:")
print(day_counts.to_string())


# Casualties by hour

casualties_with_day["hour"] = pd.to_datetime(
    casualties_with_day["time"],
    format="%H:%M",
    errors="coerce"
).dt.hour

hour_counts = (
    casualties_with_day["hour"]
    .value_counts()
    .sort_index()
)

plt.figure(figsize=(12, 6))

bars = plt.bar(hour_counts.index, hour_counts.values)

plt.title("Casualties by Hour of the Day (2021–2025)")
plt.xlabel("Hour of the Day")
plt.ylabel("Number of Casualties")
plt.xticks(range(24))
plt.grid(axis="y", alpha=0.3)

for bar, count in zip(bars, hour_counts.values):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f"{count:,}",
        ha="center",
        va="bottom",
        fontsize=8
    )

plt.tight_layout()

plt.savefig(
    output_dir / "11_casualties_by_hour.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("\nCASUALTIES BY HOUR:")
print(hour_counts.to_string())


# Casualty severity distribution by casualty class

severity_class = pd.crosstab(
    df["casualty_class"],
    df["casualty_severity"],
    normalize="index"
) * 100

severity_class = severity_class.rename(
    index={
        1: "Driver / Rider",
        2: "Passenger",
        3: "Pedestrian"
    },
    columns={
        1: "Fatal",
        2: "Serious",
        3: "Slight"
    }
)

severity_class = severity_class[
    ["Fatal", "Serious", "Slight"]
]

ax = severity_class.plot(
    kind="bar",
    stacked=True,
    figsize=(11, 6)
)

plt.title("Casualty Severity Distribution by Class (2021–2025)")
plt.xlabel("Casualty Class")
plt.ylabel("Percentage of Casualties")
plt.xticks(rotation=0)
plt.ylim(0, 100)
plt.legend(title="Severity", loc="upper right")
plt.grid(axis="y", alpha=0.3)

plt.tight_layout()

plt.savefig(
    output_dir / "12_casualty_severity_by_class.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("\nCASUALTY SEVERITY BY CLASS (%):")
print(severity_class.round(2).to_string())

# E-scooter casualties by year

escooter_year = (
    df.groupby(["collision_year", "escooter_flag"])
    .size()
    .unstack(fill_value=0)
)

escooter_year = escooter_year.rename(
    columns={
        0: "Other Casualties",
        1: "E-scooter Casualties"
    }
)

escooter_year = escooter_year[
    ["E-scooter Casualties", "Other Casualties"]
]

print("\nE-SCOOTER CASUALTIES BY YEAR:")
print(escooter_year[["E-scooter Casualties"]].to_string())

ax = escooter_year["E-scooter Casualties"].plot(
    kind="bar",
    figsize=(11, 6)
)

plt.title("E-scooter Casualties by Year (2021–2025)")
plt.xlabel("Year")
plt.ylabel("Number of Casualties")
plt.xticks(rotation=0)
plt.grid(axis="y", alpha=0.3)

for container in ax.containers:
    labels = [
        f"{int(value):,}"
        for value in container.datavalues
    ]

    ax.bar_label(
        container,
        labels=labels,
        padding=3
    )
    
plt.tight_layout()

plt.savefig(
    output_dir / "13_escooter_casualties_by_year.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()