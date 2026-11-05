
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


# Project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = (
    PROJECT_DIR
    / "data"
    / "raw"
    / "collisions"
    / "dft-road-casualty-statistics-collision-last-5-years.csv"
)

OUTPUT_FILE = (
    PROJECT_DIR
    / "visualisations"
    / "01_collision_coordinate_completeness.png"
)


# Load collision data
collisions = pd.read_csv(DATA_FILE, low_memory=False)

# Check whether both geographical coordinates are available
missing_coordinates = (
    collisions["latitude"].isna()
    | collisions["longitude"].isna()
)

missing_count = missing_coordinates.sum()
available_count = len(collisions) - missing_count

# Calculate percentages
available_percentage = available_count / len(collisions) * 100
missing_percentage = missing_count / len(collisions) * 100

# Print results
print("=" * 55)
print("COLLISION COORDINATE COMPLETENESS")
print("=" * 55)

print(f"Total collision records: {len(collisions):,}")
print(f"Coordinates available: {available_count:,}")
print(f"Coordinates missing: {missing_count:,}")
print(f"Available percentage: {available_percentage:.4f}%")
print(f"Missing percentage: {missing_percentage:.4f}%")


# Create chart
labels = ["Coordinates available", "Coordinates missing"]
values = [available_count, missing_count]

fig, ax = plt.subplots(figsize=(9, 5))

bars = ax.bar(
    labels,
    values,
    color=["#2E8B57", "#DC6B6B"],
    width=0.5
)

ax.set_title(
    "UK Road Collision Data: Coordinate Completeness",
    fontsize=14,
    fontweight="bold",
    pad=15
)

ax.set_ylabel("Number of collision records")
ax.set_ylim(0, len(collisions) * 1.12)

# Add record counts and percentages
for bar, count, percentage in zip(
    bars,
    values,
    [available_percentage, missing_percentage]
):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f"{count:,}\n({percentage:.4f}%)",
        ha="center",
        va="bottom",
        fontsize=10
    )

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()

# Save chart
plt.savefig(OUTPUT_FILE, dpi=300, bbox_inches="tight")
plt.show()

print(f"\nChart saved to: {OUTPUT_FILE}")
