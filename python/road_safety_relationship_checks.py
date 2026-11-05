
from pathlib import Path

import pandas as pd


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data" / "raw"

COLLISIONS_FILE = DATA_DIR / "collisions" / (
    "dft-road-casualty-statistics-collision-last-5-years.csv"
)

VEHICLES_FILE = DATA_DIR / "vehicles" / (
    "dft-road-casualty-statistics-vehicle-last-5-years.csv"
)

CASUALTIES_FILE = DATA_DIR / "casualties" / (
    "dft-road-casualty-statistics-casualty-last-5-years.csv"
)


# ============================================================
# LOAD DATASETS
# ============================================================

print("=" * 65)
print("UK ROAD SAFETY - DATA RELATIONSHIP CHECKS")
print("=" * 65)

collisions = pd.read_csv(COLLISIONS_FILE, low_memory=False)
vehicles = pd.read_csv(VEHICLES_FILE, low_memory=False)
casualties = pd.read_csv(CASUALTIES_FILE, low_memory=False)

print("\nAll datasets loaded successfully.")

print(f"Collisions: {len(collisions):,} records")
print(f"Vehicles:   {len(vehicles):,} records")
print(f"Casualties: {len(casualties):,} records")


# ============================================================
# 1. PRIMARY KEY CHECKS
# ============================================================

print("\n" + "=" * 65)
print("1. KEY UNIQUENESS CHECKS")
print("=" * 65)


def check_key(data, columns, dataset_name):
    duplicate_count = data.duplicated(subset=columns).sum()

    print(f"\n{dataset_name}")
    print(f"Key columns: {', '.join(columns)}")
    print(f"Duplicate key records: {duplicate_count:,}")

    if duplicate_count == 0:
        print("Result: PASS - key is unique.")
    else:
        print("Result: REVIEW - duplicate keys found.")

        duplicates = data[
            data.duplicated(subset=columns, keep=False)
        ]

        print("Sample duplicate records:")
        print(duplicates[columns].head(10).to_string(index=False))


check_key(
    collisions,
    ["collision_index"],
    "COLLISIONS"
)

check_key(
    vehicles,
    ["collision_index", "vehicle_reference"],
    "VEHICLES"
)

check_key(
    casualties,
    ["collision_index", "casualty_reference"],
    "CASUALTIES"
)


# ============================================================
# 2. FOREIGN KEY CHECKS
# ============================================================

print("\n" + "=" * 65)
print("2. COLLISION REFERENCE CHECKS")
print("=" * 65)

collision_ids = set(collisions["collision_index"])

vehicle_collision_ids = set(vehicles["collision_index"])
casualty_collision_ids = set(casualties["collision_index"])

orphan_vehicles = vehicles[
    ~vehicles["collision_index"].isin(collision_ids)
]

orphan_casualties = casualties[
    ~casualties["collision_index"].isin(collision_ids)
]

print("\nVehicle records without a matching collision:")
print(f"{len(orphan_vehicles):,}")

print("\nCasualty records without a matching collision:")
print(f"{len(orphan_casualties):,}")

print("\nCollision coverage:")
print(
    "Collisions represented in vehicles:",
    f"{len(vehicle_collision_ids & collision_ids):,}"
)

print(
    "Collisions represented in casualties:",
    f"{len(casualty_collision_ids & collision_ids):,}"
)


# ============================================================
# 3. CASUALTY-TO-VEHICLE REFERENCE CHECK
# ============================================================

print("\n" + "=" * 65)
print("3. CASUALTY-TO-VEHICLE REFERENCE CHECK")
print("=" * 65)

vehicle_keys = vehicles[
    ["collision_index", "vehicle_reference"]
].drop_duplicates()

casualty_vehicle_keys = casualties[
    ["collision_index", "vehicle_reference"]
].drop_duplicates()

casualty_vehicle_check = casualty_vehicle_keys.merge(
    vehicle_keys,
    on=["collision_index", "vehicle_reference"],
    how="left",
    indicator=True
)

unmatched_casualty_vehicle_refs = casualty_vehicle_check[
    casualty_vehicle_check["_merge"] == "left_only"
]

print(
    "Distinct casualty vehicle references:",
    f"{len(casualty_vehicle_keys):,}"
)

print(
    "References without a matching vehicle:",
    f"{len(unmatched_casualty_vehicle_refs):,}"
)

if not unmatched_casualty_vehicle_refs.empty:
    print("\nSample unmatched references:")
    print(
        unmatched_casualty_vehicle_refs[
            ["collision_index", "vehicle_reference"]
        ].head(10).to_string(index=False)
    )


# ============================================================
# 4. VEHICLE COUNT VALIDATION
# ============================================================

print("\n" + "=" * 65)
print("4. RECORDED VS ACTUAL VEHICLE COUNTS")
print("=" * 65)

actual_vehicle_counts = (
    vehicles.groupby("collision_index")
    .size()
    .rename("actual_vehicle_count")
)

vehicle_comparison = collisions[
    ["collision_index", "number_of_vehicles"]
].merge(
    actual_vehicle_counts,
    on="collision_index",
    how="left"
)

vehicle_comparison["actual_vehicle_count"] = (
    vehicle_comparison["actual_vehicle_count"].fillna(0)
)

vehicle_comparison["vehicle_count_matches"] = (
    vehicle_comparison["number_of_vehicles"]
    == vehicle_comparison["actual_vehicle_count"]
)

vehicle_mismatches = vehicle_comparison[
    ~vehicle_comparison["vehicle_count_matches"]
]

print(
    "Collisions with matching vehicle counts:",
    f"{vehicle_comparison['vehicle_count_matches'].sum():,}"
)

print(
    "Collisions with mismatched vehicle counts:",
    f"{len(vehicle_mismatches):,}"
)

if not vehicle_mismatches.empty:
    print("\nSample vehicle count mismatches:")
    print(
        vehicle_mismatches.head(10).to_string(index=False)
    )


# ============================================================
# 5. CASUALTY COUNT VALIDATION
# ============================================================

print("\n" + "=" * 65)
print("5. RECORDED VS ACTUAL CASUALTY COUNTS")
print("=" * 65)

actual_casualty_counts = (
    casualties.groupby("collision_index")
    .size()
    .rename("actual_casualty_count")
)

casualty_comparison = collisions[
    ["collision_index", "number_of_casualties"]
].merge(
    actual_casualty_counts,
    on="collision_index",
    how="left"
)

casualty_comparison["actual_casualty_count"] = (
    casualty_comparison["actual_casualty_count"].fillna(0)
)

casualty_comparison["casualty_count_matches"] = (
    casualty_comparison["number_of_casualties"]
    == casualty_comparison["actual_casualty_count"]
)

casualty_mismatches = casualty_comparison[
    ~casualty_comparison["casualty_count_matches"]
]

print(
    "Collisions with matching casualty counts:",
    f"{casualty_comparison['casualty_count_matches'].sum():,}"
)

print(
    "Collisions with mismatched casualty counts:",
    f"{len(casualty_mismatches):,}"
)

if not casualty_mismatches.empty:
    print("\nSample casualty count mismatches:")
    print(
        casualty_mismatches.head(10).to_string(index=False)
    )


# ============================================================
# 6. SUMMARY
# ============================================================

print("\n" + "=" * 65)
print("RELATIONSHIP CHECK SUMMARY")
print("=" * 65)

print(f"""
Collisions: {len(collisions):,}
Vehicles:   {len(vehicles):,}
Casualties: {len(casualties):,}

Vehicle orphan records: {len(orphan_vehicles):,}
Casualty orphan records: {len(orphan_casualties):,}

Unmatched casualty-to-vehicle references:
{len(unmatched_casualty_vehicle_refs):,}

Vehicle count mismatches: {len(vehicle_mismatches):,}
Casualty count mismatches: {len(casualty_mismatches):,}
""")

print("Relationship checks completed.")
print("=" * 65)
