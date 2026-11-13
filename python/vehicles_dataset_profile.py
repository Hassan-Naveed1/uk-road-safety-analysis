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

# SKIDDING AND OVERTURNING

skidding_summary = (
    df["skidding_and_overturning"]
    .value_counts()
    .sort_index()
)

print("\nSKIDDING AND OVERTURNING FREQUENCY")
print(skidding_summary.to_string())

# SKIDDING AND OVERTURNING

skidding_labels = {
    -1: "Data missing or out of range",
    0: "None",
    1: "Skidded",
    2: "Skidded and overturned",
    3: "Jackknifed",
    4: "Jackknifed and overturned",
    5: "Overturned",
    9: "Unknown (self reported)"
}

skidding_counts = (
    df["skidding_and_overturning"]
    .value_counts()
    .sort_values()
)

skidding_names = [
    skidding_labels.get(code, f"Unrecognised code: {code}")
    for code in skidding_counts.index
]

skidding_percentages = skidding_counts / len(df) * 100

plt.figure(figsize=(12, 6))

bars = plt.barh(skidding_names, skidding_counts.values)

plt.title("Vehicles Involved in Reported Road Collisions by Skidding and Overturning")
plt.xlabel("Number of Vehicles")
plt.ylabel("Skidding and Overturning")

for bar, count, percentage in zip(
    bars, skidding_counts.values, skidding_percentages.values
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
    VISUALISATION_DIR / "04_vehicles_by_skidding_overturning.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\nSkidding and overturning chart saved successfully.")

# VEHICLE LEAVING CARRIAGEWAY

leaving_carriageway_summary = (
    df["vehicle_leaving_carriageway"]
    .value_counts()
    .sort_index()
)

print("\nVEHICLE LEAVING CARRIAGEWAY FREQUENCY")
print(leaving_carriageway_summary.to_string())

# VEHICLE LEAVING CARRIAGEWAY

leaving_labels = {
    -1: "Data missing or out of range",
    0: "Did not leave carriageway",
    1: "Nearside",
    2: "Nearside and rebounded",
    3: "Straight ahead at junction",
    4: "Offside onto central reservation",
    5: "Offside onto central reservation and rebounded",
    6: "Offside crossed central reservation",
    7: "Offside",
    8: "Offside and rebounded",
    9: "Unknown (self reported)"
}

leaving_counts = (
    df["vehicle_leaving_carriageway"]
    .value_counts()
    .sort_values()
)

leaving_names = [
    leaving_labels.get(code, f"Unrecognised code: {code}")
    for code in leaving_counts.index
]

leaving_percentages = leaving_counts / len(df) * 100

plt.figure(figsize=(13, 8))

bars = plt.barh(leaving_names, leaving_counts.values)

plt.title("Vehicles Involved in Reported Road Collisions by Carriageway Departure")
plt.xlabel("Number of Vehicles")
plt.ylabel("Carriageway Departure")

for bar, count, percentage in zip(
    bars, leaving_counts.values, leaving_percentages.values
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
    VISUALISATION_DIR / "05_vehicles_by_carriageway_departure.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\nVehicle carriageway departure chart saved successfully.")

# OBJECTS HIT IN CARRIAGEWAY

hit_object_summary = (
    df["hit_object_in_carriageway"]
    .value_counts()
    .sort_index()
)

print("\nOBJECTS HIT IN CARRIAGEWAY FREQUENCY")
print(hit_object_summary.to_string())


# OBJECTS HIT IN CARRIAGEWAY

hit_object_labels = {
    -1: "Data missing or out of range",
    0: "None",
    1: "Previous accident",
    2: "Road works",
    4: "Parked vehicle",
    5: "Bridge (roof)",
    6: "Bridge (side)",
    7: "Bollard or refuge",
    8: "Open door of vehicle",
    9: "Central island of roundabout",
    10: "Kerb",
    11: "Other object",
    12: "Any animal (except ridden horse)",
    99: "Unknown (self reported)"
}

hit_object_counts = (
    df["hit_object_in_carriageway"]
    .value_counts()
    .sort_values()
)

hit_object_names = [
    hit_object_labels.get(code, f"Unrecognised code: {code}")
    for code in hit_object_counts.index
]

hit_object_percentages = hit_object_counts / len(df) * 100

plt.figure(figsize=(13, 8))

bars = plt.barh(hit_object_names, hit_object_counts.values)

plt.title("Vehicles Involved in Reported Road Collisions by Object Hit in Carriageway")
plt.xlabel("Number of Vehicles")
plt.ylabel("Object Hit in Carriageway")

for bar, count, percentage in zip(
    bars, hit_object_counts.values, hit_object_percentages.values
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
    VISUALISATION_DIR / "06_vehicles_by_object_hit_in_carriageway.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\nObject hit in carriageway chart saved successfully.")

# OBJECTS HIT OFF CARRIAGEWAY

hit_off_summary = (
    df["hit_object_off_carriageway"]
    .value_counts()
    .sort_index()
)

print("\nOBJECTS HIT OFF CARRIAGEWAY FREQUENCY")
print(hit_off_summary.to_string())

# OBJECTS HIT OFF CARRIAGEWAY

hit_off_labels = {
    -1: "Data missing or out of range",
    0: "None",
    1: "Road sign or traffic signal",
    2: "Lamp post",
    3: "Telegraph/electricity pole",
    4: "Tree",
    5: "Bus stop or shelter",
    6: "Central crash barrier",
    7: "Nearside/offside crash barrier",
    8: "Submerged in water",
    9: "Entered ditch",
    10: "Other permanent object",
    11: "Wall or fence",
    99: "Unknown (self reported)"
}

hit_off_counts = (
    df["hit_object_off_carriageway"]
    .value_counts()
    .sort_values()
)

hit_off_names = [
    hit_off_labels.get(code, f"Unrecognised code: {code}")
    for code in hit_off_counts.index
]

hit_off_percentages = hit_off_counts / len(df) * 100

plt.figure(figsize=(13, 8))

bars = plt.barh(hit_off_names, hit_off_counts.values)

plt.title("Vehicles Involved in Reported Road Collisions by Object Hit Off Carriageway")
plt.xlabel("Number of Vehicles")
plt.ylabel("Object Hit Off Carriageway")

for bar, count, percentage in zip(
    bars, hit_off_counts.values, hit_off_percentages.values
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
    VISUALISATION_DIR / "07_vehicles_by_object_hit_off_carriageway.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\nObject hit off carriageway chart saved successfully.")


# FIRST POINT OF IMPACT

impact_summary = (
    df["first_point_of_impact"]
    .value_counts()
    .sort_index()
)

print("\nFIRST POINT OF IMPACT FREQUENCY")
print(impact_summary.to_string())

# FIRST POINT OF IMPACT

impact_labels = {
    -1: "Data missing or out of range",
    0: "Did not impact",
    1: "Front",
    2: "Back",
    3: "Offside",
    4: "Nearside",
    9: "Unknown (self reported)"
}

impact_counts = (
    df["first_point_of_impact"]
    .value_counts()
    .sort_values()
)

impact_names = [
    impact_labels.get(code, f"Unrecognised code: {code}")
    for code in impact_counts.index
]

impact_percentages = impact_counts / len(df) * 100

plt.figure(figsize=(12, 6))

bars = plt.barh(impact_names, impact_counts.values)

plt.title("Vehicles Involved in Reported Road Collisions by First Point of Impact")
plt.xlabel("Number of Vehicles")
plt.ylabel("First Point of Impact")

for bar, count, percentage in zip(
    bars, impact_counts.values, impact_percentages.values
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
    VISUALISATION_DIR / "08_vehicles_by_first_point_of_impact.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\nFirst point of impact chart saved successfully.")

# VEHICLE LEFT-HAND DRIVE

left_hand_drive_summary = (
    df["vehicle_left_hand_drive"]
    .value_counts()
    .sort_index()
)

print("\nVEHICLE LEFT-HAND DRIVE FREQUENCY")
print(left_hand_drive_summary.to_string())

# VEHICLE LEFT-HAND DRIVE

left_hand_drive_labels = {
    -1: "Data missing or out of range",
    1: "No",
    2: "Yes",
    9: "Unknown"
}

left_hand_drive_counts = (
    df["vehicle_left_hand_drive"]
    .value_counts()
    .sort_values()
)

left_hand_drive_names = [
    left_hand_drive_labels.get(code, f"Unrecognised code: {code}")
    for code in left_hand_drive_counts.index
]

left_hand_drive_percentages = (
    left_hand_drive_counts / len(df) * 100
)

plt.figure(figsize=(10, 5))

bars = plt.barh(
    left_hand_drive_names,
    left_hand_drive_counts.values
)

plt.title("Vehicles Involved in Reported Road Collisions by Left-Hand Drive Status")
plt.xlabel("Number of Vehicles")
plt.ylabel("Left-Hand Drive Status")

for bar, count, percentage in zip(
    bars,
    left_hand_drive_counts.values,
    left_hand_drive_percentages.values
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
    VISUALISATION_DIR / "09_vehicles_by_left_hand_drive.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\nLeft-hand drive chart saved successfully.")

# SEX OF DRIVER

sex_summary = (
    df["sex_of_driver"]
    .value_counts()
    .sort_index()
)

print("\nSEX OF DRIVER FREQUENCY")
print(sex_summary.to_string())

# SEX OF DRIVER

sex_labels = {
    -1: "Data missing or out of range",
    1: "Male",
    2: "Female",
    3: "Not known"
}

sex_counts = (
    df["sex_of_driver"]
    .value_counts()
    .sort_values()
)

sex_names = [
    sex_labels.get(code, f"Unrecognised code: {code}")
    for code in sex_counts.index
]

sex_percentages = sex_counts / len(df) * 100

plt.figure(figsize=(10, 5))

bars = plt.barh(sex_names, sex_counts.values)

plt.title("Vehicles Involved in Reported Road Collisions by Driver Sex")
plt.xlabel("Number of Vehicles")
plt.ylabel("Driver Sex")

for bar, count, percentage in zip(
    bars, sex_counts.values, sex_percentages.values
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
    VISUALISATION_DIR / "10_vehicles_by_driver_sex.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\nDriver sex chart saved successfully.")

# DRIVER AGE BAND

age_band_summary = (
    df["age_band_of_driver"]
    .value_counts()
    .sort_index()
)

print("\nDRIVER AGE BAND FREQUENCY")
print(age_band_summary.to_string())

# DRIVER AGE BAND

age_band_labels = {
    -1: "Data missing or out of range",
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
    df["age_band_of_driver"]
    .value_counts()
    .sort_index()
)

age_band_names = [
    age_band_labels.get(code, f"Unrecognised code: {code}")
    for code in age_band_counts.index
]

age_band_percentages = age_band_counts / len(df) * 100

plt.figure(figsize=(11, 7))

bars = plt.barh(age_band_names, age_band_counts.values)

plt.title("Vehicles Involved in Reported Road Collisions by Driver Age Band")
plt.xlabel("Number of Vehicles")
plt.ylabel("Driver Age Band")

for bar, count, percentage in zip(
    bars, age_band_counts.values, age_band_percentages.values
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
    VISUALISATION_DIR / "11_vehicles_by_driver_age_band.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\nDriver age band chart saved successfully.")

# DRIVER AGE

driver_age_summary = (
    df["age_of_driver"]
    .value_counts()
    .sort_index()
)

print("\nDRIVER AGE FREQUENCY")
print(driver_age_summary.to_string())

# DRIVER AGE STATISTICS

valid_driver_ages = df.loc[
    df["age_of_driver"] != -1,
    "age_of_driver"
]

print("\nDRIVER AGE STATISTICS")
print(f"Valid age records: {len(valid_driver_ages):,}")
print(f"Minimum age: {valid_driver_ages.min()}")
print(f"Maximum age: {valid_driver_ages.max()}")
print(f"Mean age: {valid_driver_ages.mean():.2f}")
print(f"Median age: {valid_driver_ages.median():.2f}")

print("\nUNUSUAL DRIVER AGE CHECKS")

print(
    "Drivers under 17:",
    (valid_driver_ages < 17).sum()
)

print(
    "Drivers aged over 90:",
    (valid_driver_ages > 90).sum()
)

print(
    "Drivers aged over 100:",
    (valid_driver_ages > 100).sum()
)
# DRIVER AGE DISTRIBUTION

plt.figure(figsize=(12, 6))

plt.hist(
    valid_driver_ages,
    bins=range(0, 111, 5),
    edgecolor="black"
)

plt.title("Distribution of Driver Ages in Reported Road Collisions")
plt.xlabel("Driver Age")
plt.ylabel("Number of Vehicles")

plt.xticks(range(0, 111, 5))
plt.tight_layout()

plt.savefig(
    VISUALISATION_DIR / "12_vehicles_by_driver_age_distribution.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\nDriver age distribution chart saved successfully.")

# VEHICLE AGE FREQUENCY

vehicle_age_summary = (
    df["age_of_vehicle"]
    .value_counts()
    .sort_index()
)

print("\nVEHICLE AGE FREQUENCY")
print(vehicle_age_summary.to_string())

# VEHICLE AGE STATISTICS

valid_vehicle_ages = df.loc[
    df["age_of_vehicle"] != -1,
    "age_of_vehicle"
]

print("\nVEHICLE AGE STATISTICS")
print(f"Valid records: {len(valid_vehicle_ages):,}")
print(f"Minimum age: {valid_vehicle_ages.min()}")
print(f"Maximum age: {valid_vehicle_ages.max()}")
print(f"Mean age: {valid_vehicle_ages.mean():.2f}")
print(f"Median age: {valid_vehicle_ages.median():.2f}")

print("\nUNUSUAL VEHICLE AGE CHECKS")
print(f"Vehicles over 30 years: {(valid_vehicle_ages > 30).sum():,}")
print(f"Vehicles over 50 years: {(valid_vehicle_ages > 50).sum():,}")
print(f"Vehicles over 100 years: {(valid_vehicle_ages > 100).sum():,}")

# VEHICLE AGE DISTRIBUTION

plt.figure(figsize=(12, 6))

plt.hist(
    valid_vehicle_ages[valid_vehicle_ages <= 50],
    bins=range(0, 56, 5),
    edgecolor="black"
)

plt.title("Distribution of Vehicle Ages in Reported Road Collisions")
plt.xlabel("Vehicle Age (Years)")
plt.ylabel("Number of Vehicles")

plt.xticks(range(0, 56, 5))
plt.tight_layout()

plt.savefig(
    VISUALISATION_DIR / "13_vehicles_by_age.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\nVehicle age distribution chart saved successfully.")
