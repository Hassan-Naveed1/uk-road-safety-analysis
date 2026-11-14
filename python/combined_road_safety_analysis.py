import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
# ============================================================
# FILE PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

COLLISIONS_FILE = (
    BASE_DIR / "data" / "raw" / "collisions" /
    "dft-road-casualty-statistics-collision-last-5-years.csv"
)

VEHICLES_FILE = (
    BASE_DIR / "data" / "raw" / "vehicles" /
    "dft-road-casualty-statistics-vehicle-last-5-years.csv"
)

CASUALTIES_FILE = (
    BASE_DIR / "data" / "raw" / "casualties" /
    "dft-road-casualty-statistics-casualty-last-5-years.csv"
)

# ============================================================
# LOAD DATASETS
# ============================================================

print("=" * 60)
print("COMBINED UK ROAD SAFETY ANALYSIS")
print("=" * 60)

collisions = pd.read_csv(COLLISIONS_FILE, low_memory=False)
vehicles = pd.read_csv(VEHICLES_FILE, low_memory=False)
casualties = pd.read_csv(CASUALTIES_FILE, low_memory=False)

# ============================================================
# RECORD COUNTS
# ============================================================

print("\nDATASET RECORD COUNTS")
print("-" * 60)

print(f"Collisions: {len(collisions):,}")
print(f"Vehicles:   {len(vehicles):,}")
print(f"Casualties: {len(casualties):,}")


# ============================================================
# IDENTIFIER VALIDATION
# ============================================================

print("\nIDENTIFIER VALIDATION")
print("-" * 60)

checks = {
    "Collision index": collisions["collision_index"].is_unique,
    "Vehicle composite key": not vehicles.duplicated(
        subset=["collision_index", "vehicle_reference"]
    ).any(),
    "Casualty composite key": not casualties.duplicated(
        subset=["collision_index", "casualty_reference"]
    ).any(),
}

for name, passed in checks.items():
    status = "PASS" if passed else "FAIL"
    print(f"{name}: {status}")

# ============================================================
# RELATIONSHIP VALIDATION
# ============================================================

print("\nRELATIONSHIP VALIDATION")
print("-" * 60)

collision_ids = set(collisions["collision_index"])
vehicle_keys = set(
    zip(vehicles["collision_index"], vehicles["vehicle_reference"])
)

# Check vehicles against collisions
unmatched_vehicles = ~vehicles["collision_index"].isin(collision_ids)

# Check casualties against collisions
unmatched_casualties = ~casualties["collision_index"].isin(collision_ids)

# Check casualties against their corresponding vehicles
casualty_vehicle_keys = list(
    zip(casualties["collision_index"], casualties["vehicle_reference"])
)

unmatched_casualty_vehicles = [
    key not in vehicle_keys for key in casualty_vehicle_keys
]

print(f"Vehicles without matching collision: {unmatched_vehicles.sum():,}")
print(f"Casualties without matching collision: {unmatched_casualties.sum():,}")
print(
    "Casualties without matching vehicle: "
    f"{sum(unmatched_casualty_vehicles):,}"
)


# ============================================================
# RECORD RELATIONSHIP SUMMARY
# ============================================================

print("\nRECORD RELATIONSHIP SUMMARY")
print("-" * 60)

vehicles_per_collision = vehicles.groupby("collision_index").size()
casualties_per_collision = casualties.groupby("collision_index").size()

casualties_per_vehicle = casualties.groupby(
    ["collision_index", "vehicle_reference"]
).size()

print(f"Collisions containing vehicles: {len(vehicles_per_collision):,}")
print(f"Collisions containing casualties: {len(casualties_per_collision):,}")
print(f"Vehicles with linked casualties: {len(casualties_per_vehicle):,}")

print("\nVEHICLES PER COLLISION")
print(f"Average: {vehicles_per_collision.mean():.2f}")
print(f"Maximum: {vehicles_per_collision.max():,}")

print("\nCASUALTIES PER COLLISION")
print(f"Average: {casualties_per_collision.mean():.2f}")
print(f"Maximum: {casualties_per_collision.max():,}")

print("\nCASUALTIES PER VEHICLE")
print(f"Average: {casualties_per_vehicle.mean():.2f}")
print(f"Maximum: {casualties_per_vehicle.max():,}")


# ============================================================
# INVESTIGATE HIGHEST CASUALTY COUNT
# ============================================================

print("\nHIGHEST CASUALTY COUNT INVESTIGATION")
print("-" * 60)

casualties_per_collision = casualties.groupby("collision_index").size()

highest_collision_id = casualties_per_collision.idxmax()
highest_casualty_count = casualties_per_collision.max()

collision_details = collisions.loc[
    collisions["collision_index"] == highest_collision_id,
    [
        "collision_index",
        "collision_year",
        "date",
        "time",
        "collision_severity",
        "number_of_vehicles",
        "number_of_casualties"
    ]
]

print(f"Collision index: {highest_collision_id}")
print(f"Casualty records: {highest_casualty_count}")

print("\nCOLLISION DETAILS")
print(collision_details.to_string(index=False))

# ============================================================
# INSPECT UNUSUAL COLLISION CASUALTIES
# ============================================================

print("\nCASUALTY RECORD DETAILS")
print("-" * 60)

collision_casualties = casualties[
    casualties["collision_index"] == highest_collision_id
]

print("\nCASUALTY CLASS")
print(collision_casualties["casualty_class"].value_counts(dropna=False))

print("\nCASUALTY TYPE")
print(collision_casualties["casualty_type"].value_counts(dropna=False))

print("\nCASUALTY SEVERITY")
print(collision_casualties["casualty_severity"].value_counts(dropna=False))

print("\nVEHICLE REFERENCES")
print(collision_casualties["vehicle_reference"].value_counts(dropna=False))

# ============================================================
# INVESTIGATE VEHICLE INVOLVED
# ============================================================

print("\nVEHICLE INVOLVED IN UNUSUAL COLLISION")
print("-" * 60)

vehicle_details = vehicles[
    (vehicles["collision_index"] == highest_collision_id) &
    (vehicles["vehicle_reference"] == 1)
]

columns_to_show = [
    "collision_index",
    "vehicle_reference",
    "vehicle_type",
    "generic_make_model",
    "age_of_vehicle",
    "journey_purpose_of_driver"
]

print(vehicle_details[columns_to_show].to_string(index=False))

# ============================================================
# COLLISION LOCATION AND ROAD CONDITIONS
# ============================================================

print("\nCOLLISION LOCATION AND ROAD CONDITIONS")
print("-" * 60)

location_columns = [
    "local_authority_district",
    "local_authority_highway",
    "road_type",
    "speed_limit",
    "urban_or_rural_area",
    "light_conditions",
    "weather_conditions",
    "road_surface_conditions"
]

print(
    collision_details.merge(
        collisions[["collision_index"] + location_columns],
        on="collision_index",
        how="left"
    )[location_columns].to_string(index=False)
)

# ============================================================
# TOP 10 COLLISIONS BY CASUALTY COUNT
# ============================================================

print("\nTOP 10 COLLISIONS BY CASUALTY COUNT")
print("-" * 70)

# Count actual casualty records for each collision
actual_casualty_counts = (
    casualties.groupby("collision_index")
    .size()
    .rename("actual_casualties")
)

# Combine actual counts with collision records
top_collisions = collisions[
    ["collision_index", "date", "collision_year",
     "number_of_vehicles", "number_of_casualties"]
].merge(
    actual_casualty_counts,
    on="collision_index",
    how="left",
    validate="one_to_one"
)

# Sort and select the 10 highest
top_10 = top_collisions.nlargest(
    10, "actual_casualties"
)

# Compare reported and actual casualty counts
top_10["count_difference"] = (
    top_10["number_of_casualties"] -
    top_10["actual_casualties"]
)

print(
    top_10.to_string(index=False)
)

# Check whether reported and actual counts agree
print("\nCOUNT VALIDATION")
print("-" * 70)

print(
    "All 10 reported counts match actual counts:",
    (top_10["count_difference"] == 0).all()
)

# ============================================================
# INVESTIGATE SECOND-HIGHEST CASUALTY COLLISION
# ============================================================

second_collision_id = "2025041681268"

print("\nSECOND-HIGHEST CASUALTY COLLISION")
print("-" * 60)

print("\nCOLLISION DETAILS")
print(
    collisions[
        collisions["collision_index"] == second_collision_id
    ].to_string(index=False)
)

print("\nCASUALTY CLASS")
print(
    casualties[
        casualties["collision_index"] == second_collision_id
    ]["casualty_class"].value_counts()
)

print("\nCASUALTY TYPE")
print(
    casualties[
        casualties["collision_index"] == second_collision_id
    ]["casualty_type"].value_counts()
)

print("\nCASUALTY SEVERITY")
print(
    casualties[
        casualties["collision_index"] == second_collision_id
    ]["casualty_severity"].value_counts()
)

# ============================================================
# VEHICLES INVOLVED IN SECOND-HIGHEST CASUALTY COLLISION
# ============================================================

print("\nVEHICLES INVOLVED IN SECOND-HIGHEST CASUALTY COLLISION")
print("-" * 70)

collision_vehicles = vehicles[
    vehicles["collision_index"] == second_collision_id
]

print(
    collision_vehicles[
        [
            "collision_index",
            "vehicle_reference",
            "vehicle_type",
            "generic_make_model",
            "age_of_vehicle",
            "journey_purpose_of_driver"
        ]
    ].to_string(index=False)
)

print("\nCASUALTIES BY VEHICLE REFERENCE AND TYPE")
print("-" * 70)

collision_casualties = casualties[
    casualties["collision_index"] == second_collision_id
]

print(
    collision_casualties.groupby(
        ["vehicle_reference", "casualty_type", "casualty_class"]
    ).size().reset_index(name="casualty_count").to_string(index=False)
)

# ============================================================
# TOP 10 COLLISIONS - CASUALTY AND VEHICLE BREAKDOWN
# ============================================================

print("\nTOP 10 COLLISIONS - DETAILED BREAKDOWN")
print("=" * 60)

for collision_id in top_10["collision_index"]:

    print(f"\nCollision: {collision_id}")
    print("-" * 60)

    # Casualties in this collision
    collision_casualties = casualties[
        casualties["collision_index"] == collision_id
    ]

    print("Casualty classes:")
    print(collision_casualties["casualty_class"].value_counts().to_dict())

    print("Casualty types:")
    print(collision_casualties["casualty_type"].value_counts().to_dict())

    # Vehicles in this collision
    collision_vehicles = vehicles[
        vehicles["collision_index"] == collision_id
    ]

    print("Vehicle types:")
    print(collision_vehicles["vehicle_type"].value_counts().to_dict())

# ============================================================
# TOP 10 COLLISIONS - SUMMARY TABLE
# ============================================================

print("\nTOP 10 COLLISIONS SUMMARY")
print("=" * 60)

print(
    top_10[
        [
            "collision_index",
            "date",
            "collision_year",
            "number_of_vehicles",
            "number_of_casualties"
        ]
    ].to_string(index=False)
)

print("\nTOTAL CASUALTIES ACROSS TOP 10:")
print(top_10["number_of_casualties"].sum())

print("\nAVERAGE CASUALTIES PER COLLISION:")
print(round(top_10["number_of_casualties"].mean(), 2))

# ============================================================
# VEHICLES AND CASUALTIES RELATIONSHIP
# ============================================================

print("\nVEHICLES AND CASUALTIES RELATIONSHIP")
print("=" * 60)

vehicle_casualty_summary = (
    collisions.groupby("number_of_vehicles")["number_of_casualties"]
    .agg(["count", "mean", "median", "max"])
    .round(2)
)

print(vehicle_casualty_summary.to_string())


# ============================================================
# GROUPED VEHICLE AND CASUALTY ANALYSIS
# ============================================================

print("\nGROUPED VEHICLE AND CASUALTY ANALYSIS")
print("=" * 60)

grouped_summary = (
    collisions.assign(
        vehicle_group=collisions["number_of_vehicles"].clip(upper=5)
    )
    .groupby("vehicle_group")["number_of_casualties"]
    .agg(["count", "mean", "median"])
    .round(2)
)

grouped_summary.index = [
    "1 vehicle",
    "2 vehicles",
    "3 vehicles",
    "4 vehicles",
    "5+ vehicles"
]

print(grouped_summary.to_string())

# ============================================================
# VEHICLES AND CASUALTIES CHART
# ============================================================

plt.figure(figsize=(9, 5))

plt.bar(
    grouped_summary.index,
    grouped_summary["mean"]
)

plt.title("Average Casualties by Number of Vehicles")
plt.xlabel("Number of Vehicles")
plt.ylabel("Average Casualties")
plt.tight_layout()

plt.savefig(
    BASE_DIR / "visualisations" / "combined_vehicle_casualty_analysis.png",
    dpi=300
)

plt.show()
plt.close()