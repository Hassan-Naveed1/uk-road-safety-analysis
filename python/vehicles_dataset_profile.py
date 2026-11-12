import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = (
    PROJECT_DIR
    / "data"
    / "raw"
    / "vehicles"
    / "dft-road-casualty-statistics-vehicle-last-5-years.csv"
)

df = pd.read_csv(
    DATA_FILE,
    low_memory=False,
    keep_default_na=False
)

print("=" * 60)
print("VEHICLES DATASET PROFILE")
print("=" * 60)

print(f"\nNumber of records: {len(df):,}")
print(f"Number of columns: {len(df.columns)}")

profile = pd.DataFrame({
    "column_name": df.columns,
    "data_type": df.dtypes.astype(str).values,
    "missing_values": (
        (df.isna() | df.eq("")).sum().values
    ),
    "unique_values": df.nunique().values
})

print("\nCOLUMN OVERVIEW")
print(profile.to_string(index=False))

OUTPUT_DIR = PROJECT_DIR / "data" / "processed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

VISUALISATION_DIR = PROJECT_DIR / "visualisations"
VISUALISATION_DIR.mkdir(parents=True, exist_ok=True)

profile.to_csv(
    OUTPUT_DIR / "vehicles_column_profile.csv",
    index=False
)

print("\nVehicle column profile saved successfully.")


vehicle_type_summary = (
    df["vehicle_type"]
    .value_counts()
    .sort_index()
    .reset_index()
)

vehicle_type_summary.columns = [
    "vehicle_type_code",
    "vehicle_count"
]

vehicle_type_summary["percentage"] = (
    vehicle_type_summary["vehicle_count"] / len(df) * 100
).round(2)

print("\nVEHICLE FREQUENCY BY TYPE")
print(vehicle_type_summary.to_string(index=False))

# VEHICLE TYPES

vehicle_type_labels = {
    -1: "Data missing or out of range",
    1: "Pedal cycle",
    2: "Motorcycle 50cc and under",
    3: "Motorcycle 125cc and under",
    4: "Motorcycle over 125cc up to 500cc",
    5: "Motorcycle over 500cc",
    8: "Taxi / Private hire car",
    9: "Car",
    10: "Minibus",
    11: "Bus or coach",
    16: "Ridden horse",
    17: "Agricultural vehicle",
    18: "Tram",
    19: "Van / goods vehicle up to 3.5 tonnes",
    20: "Goods vehicle over 3.5t and under 7.5t",
    21: "Goods vehicle 7.5 tonnes and over",
    22: "Mobility scooter",
    23: "Electric motorcycle",
    33: "Personal powered transporter",
    90: "Other vehicle",
    97: "Motorcycle - unknown cc",
    98: "Goods vehicle - unknown weight",
    99: "Unknown vehicle type"
}

vehicle_counts = df["vehicle_type"].value_counts().sort_values()

vehicle_labels = [
    vehicle_type_labels.get(code, f"Unrecognised code: {code}")
    for code in vehicle_counts.index
]

vehicle_percentages = (vehicle_counts / len(df)) * 100

plt.figure(figsize=(12, 10))

bars = plt.barh(vehicle_labels, vehicle_counts.values)

plt.title("Vehicles Involved in Reported Road Collisions by Vehicle Type")
plt.xlabel("Number of Vehicles")
plt.ylabel("Vehicle Type")

for bar, count, percentage in zip(
    bars, vehicle_counts.values, vehicle_percentages.values
):
    plt.text(
        bar.get_width(),
        bar.get_y() + bar.get_height() / 2,
        f" {count:,} ({percentage:.2f}%)",
        va="center",
        fontsize=8
    )

plt.tight_layout()

plt.savefig(
    VISUALISATION_DIR / "01_vehicles_by_type.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\nVehicle type chart saved successfully.")

# VEHICLE MANOEUVRES

manoeuvre_summary = (
    df["vehicle_manoeuvre"]
    .value_counts()
    .sort_index()
)

print("\nVEHICLE MANOEUVRE FREQUENCY")
print(manoeuvre_summary.to_string())

# VEHICLE MANOEUVRES

manoeuvre_labels = {
    -1: "Data missing or out of range",
    1: "Reversing",
    2: "Parked",
    3: "Waiting to go ahead",
    4: "Slowing or stopping",
    5: "Moving off",
    6: "U-turn",
    7: "Turning left",
    8: "Waiting to turn left",
    9: "Turning right",
    10: "Waiting to turn right",
    11: "Changing lane to left",
    12: "Changing lane to right",
    13: "Overtaking moving vehicle on offside",
    14: "Overtaking stationary vehicle on offside",
    15: "Overtaking on nearside",
    19: "Going ahead",
    20: "Parking",
    99: "Unknown (self reported)"
}

manoeuvre_counts = df["vehicle_manoeuvre"].value_counts().sort_values()

manoeuvre_names = [
    manoeuvre_labels.get(code, f"Unrecognised code: {code}")
    for code in manoeuvre_counts.index
]

manoeuvre_percentages = manoeuvre_counts / len(df) * 100

plt.figure(figsize=(12, 9))

bars = plt.barh(manoeuvre_names, manoeuvre_counts.values)

plt.title("Vehicles Involved in Reported Road Collisions by Manoeuvre")
plt.xlabel("Number of Vehicles")
plt.ylabel("Vehicle Manoeuvre")

for bar, count, percentage in zip(
    bars, manoeuvre_counts.values, manoeuvre_percentages.values
):
    plt.text(
        bar.get_width(),
        bar.get_y() + bar.get_height() / 2,
        f" {count:,} ({percentage:.2f}%)",
        va="center",
        fontsize=8
    )

plt.tight_layout()

plt.savefig(
    VISUALISATION_DIR / "02_vehicles_by_manoeuvre.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\nVehicle manoeuvre chart saved successfully.")

# JUNCTION LOCATION

junction_location_summary = (
    df["junction_location"]
    .value_counts()
    .sort_index()
)

print("\nJUNCTION LOCATION FREQUENCY")
print(junction_location_summary.to_string())


# JUNCTION LOCATION

junction_location_labels = {
    -1: "Data missing or out of range",
    0: "Not at or within 20 metres of junction",
    1: "Approaching junction / junction approach",
    2: "Cleared junction / junction exit",
    3: "Leaving roundabout",
    4: "Entering roundabout",
    5: "Leaving main road",
    6: "Entering main road",
    7: "Entering from slip road",
    8: "Mid junction / on roundabout",
    9: "Unknown (self reported)"
}

junction_counts = (
    df["junction_location"]
    .value_counts()
    .sort_values()
)

junction_labels = [
    junction_location_labels.get(code, f"Unrecognised code: {code}")
    for code in junction_counts.index
]

junction_percentages = junction_counts / len(df) * 100

plt.figure(figsize=(12, 7))

bars = plt.barh(junction_labels, junction_counts.values)

plt.title("Vehicles Involved in Reported Road Collisions by Junction Location")
plt.xlabel("Number of Vehicles")
plt.ylabel("Junction Location")

for bar, count, percentage in zip(
    bars, junction_counts.values, junction_percentages.values
):
    plt.text(
        bar.get_width(),
        bar.get_y() + bar.get_height() / 2,
        f" {count:,} ({percentage:.2f}%)",
        va="center",
        fontsize=8
    )

plt.tight_layout()

plt.savefig(
    VISUALISATION_DIR / "03_vehicles_by_junction_location.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\nJunction location chart saved successfully.")

