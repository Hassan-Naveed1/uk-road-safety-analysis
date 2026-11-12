
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# ============================================================
# 1. PROJECT CONFIGURATION
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = (
    PROJECT_DIR
    / "data"
    / "raw"
    / "collisions"
    / "dft-road-casualty-statistics-collision-last-5-years.csv"
)

OUTPUT_DIR = PROJECT_DIR / "data" / "processed"
VISUALISATION_DIR = PROJECT_DIR / "visualisations"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
VISUALISATION_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# 2. LOAD DATASET
# ============================================================

df = pd.read_csv(
    DATA_FILE,
    low_memory=False,
    keep_default_na=False
)

print("=" * 60)
print("COLLISIONS DATASET PROFILE")
print("=" * 60)

print(f"\nNumber of records: {len(df):,}")
print(f"Number of columns: {len(df.columns)}")


# ============================================================
# 3. COLUMN OVERVIEW
# ============================================================

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
column_profile.to_csv(
    OUTPUT_DIR / "collisions_column_profile.csv",
    index=False
)

print("\nColumn profile saved successfully.")


# ============================================================
# 4. COLLISION SEVERITY ANALYSIS
# ============================================================

severity_summary = (
    df["collision_severity"]
    .value_counts()
    .sort_index()
    .reset_index()
)

severity_summary.columns = [
    "severity_code",
    "collision_count"
]

severity_summary["percentage"] = (
    severity_summary["collision_count"] / len(df) * 100
).round(2)

severity_labels = {
    1: "Fatal",
    2: "Serious",
    3: "Slight"
}

severity_summary["severity"] = (
    severity_summary["severity_code"].map(severity_labels)
)

print("\n" + "=" * 60)
print("COLLISION SEVERITY DISTRIBUTION")
print("=" * 60)

print(severity_summary.to_string(index=False))


# Severity chart
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
    VISUALISATION_DIR / "02_collision_severity.png",
    dpi=300
)

plt.show()
plt.close()


# ============================================================
# 5. COLLISION FREQUENCY BY YEAR
# ============================================================

yearly_summary = (
    df["collision_year"]
    .value_counts()
    .sort_index()
    .reset_index()
)

yearly_summary.columns = [
    "year",
    "collision_count"
]

yearly_summary["percentage"] = (
    yearly_summary["collision_count"] / len(df) * 100
).round(2)

print("\n" + "=" * 60)
print("COLLISION FREQUENCY BY YEAR")
print("=" * 60)

print(yearly_summary.to_string(index=False))


# Yearly trend chart
plt.figure(figsize=(9, 5))

plt.plot(
    yearly_summary["year"],
    yearly_summary["collision_count"],
    marker="o"
)

plt.title("UK Road Collision Trends (2021–2025)")
plt.xlabel("Year")
plt.ylabel("Number of Collisions")
plt.xticks(yearly_summary["year"])

plt.grid(axis="y", alpha=0.3)
plt.tight_layout()

plt.savefig(
    VISUALISATION_DIR / "03_collision_yearly_trend.png",
    dpi=300
)

plt.show()
plt.close()


# ============================================================
# 6. COLLISION FREQUENCY BY DAY OF THE WEEK
# ============================================================

day_summary = (
    df["day_of_week"]
    .value_counts()
    .sort_index()
    .reset_index()
)

day_summary.columns = [
    "day_code",
    "collision_count"
]

day_summary["percentage"] = (
    day_summary["collision_count"] / len(df) * 100
).round(2)

day_names = {
    1: "Sunday",
    2: "Monday",
    3: "Tuesday",
    4: "Wednesday",
    5: "Thursday",
    6: "Friday",
    7: "Saturday"
}

day_summary["day"] = day_summary["day_code"].map(day_names)

print("\n" + "=" * 60)
print("COLLISION FREQUENCY BY DAY OF THE WEEK")
print("=" * 60)

print(day_summary.to_string(index=False))


# Day-of-week chart
plt.figure(figsize=(10, 5))

bars = plt.bar(
    day_summary["day"],
    day_summary["collision_count"]
)

plt.title("UK Road Collisions by Day of the Week (2021–2025)")
plt.xlabel("Day of the Week")
plt.ylabel("Number of Collisions")

plt.bar_label(bars, fmt="%.0f", padding=3)

plt.tight_layout()

plt.savefig(
    VISUALISATION_DIR / "04_collisions_by_day.png",
    dpi=300
)

plt.show()
plt.close()


# ============================================================
# 7. COLLISION FREQUENCY BY HOUR
# ============================================================

time_values = pd.to_datetime(
    df["time"],
    format="%H:%M",
    errors="coerce"
)

invalid_times = time_values.isna().sum()

hourly_summary = (
    time_values.dt.hour
    .value_counts()
    .sort_index()
    .reset_index()
)

hourly_summary.columns = [
    "hour",
    "collision_count"
]

hourly_summary["percentage"] = (
    hourly_summary["collision_count"] / len(df) * 100
).round(2)

print("\n" + "=" * 60)
print("COLLISION FREQUENCY BY HOUR")
print("=" * 60)

print(f"Invalid or missing times: {invalid_times:,}")
print(hourly_summary.to_string(index=False))


# Hourly collision chart
plt.figure(figsize=(12, 5))

bars = plt.bar(
    hourly_summary["hour"],
    hourly_summary["collision_count"]
)

plt.title("UK Road Collisions by Hour (2021–2025)")
plt.xlabel("Hour of the Day")
plt.ylabel("Number of Collisions")

plt.xticks(range(24))
plt.bar_label(bars, fmt="%.0f", padding=2, fontsize=7)

plt.grid(axis="y", alpha=0.3)
plt.tight_layout()

plt.savefig(
    VISUALISATION_DIR / "05_collisions_by_hour.png",
    dpi=300
)

plt.show()
plt.close()


# ============================================================
# 8. COLLISION SEVERITY BY YEAR
# ============================================================

severity_year_summary = pd.crosstab(
    df["collision_year"],
    df["collision_severity"]
)

severity_year_summary.columns = [
    "Fatal",
    "Serious",
    "Slight"
]

severity_year_summary["Total"] = severity_year_summary.sum(axis=1)

print("\n" + "=" * 60)
print("COLLISION SEVERITY BY YEAR")
print("=" * 60)

print(severity_year_summary.to_string())

# Calculate severity percentages within each year
severity_percentage = (
    severity_year_summary[["Fatal", "Serious", "Slight"]]
    .div(severity_year_summary["Total"], axis=0)
    * 100
)

print("\n" + "=" * 60)
print("COLLISION SEVERITY PERCENTAGES BY YEAR")
print("=" * 60)

print(severity_percentage.round(2).to_string())


# ============================================================
# 9. COLLISION SEVERITY TRENDS BY YEAR
# ============================================================

years = severity_percentage.index.astype(str)

fig, axes = plt.subplots(
    nrows=3,
    ncols=1,
    figsize=(11, 10)
)

severity_categories = [
    ("Fatal", "Fatal Collisions", 1),
    ("Serious", "Serious Collisions", 2),
    ("Slight", "Slight Collisions", 3)
]

for ax, (category, title, position) in zip(axes, severity_categories):

    values = severity_percentage[category]

    ax.plot(
        years,
        values,
        marker="o",
        markersize=7,
        linewidth=2.5
    )

    ax.set_title(title, loc="left", fontweight="bold")
    ax.set_ylabel("Percentage (%)")
    ax.set_xticks(range(len(years)))
    ax.set_xticklabels(years)

    # Display percentage values beside each point
    for x, value in enumerate(values):
        ax.annotate(
            f"{value:.2f}%",
            (x, value),
            textcoords="offset points",
            xytext=(0, 9),
            ha="center",
            fontsize=9
        )

    # Give each category an appropriate visible scale
    margin = (values.max() - values.min()) * 0.5 + 0.2
    ax.set_ylim(
        max(0, values.min() - margin),
        values.max() + margin
    )

    ax.grid(axis="y", alpha=0.3)

fig.suptitle(
    "Collision Severity Trends by Year (2021–2025)",
    fontsize=16,
    fontweight="bold"
)

fig.supxlabel("Year", fontsize=11)

fig.text(
    0.5,
    0.01,
    "Each panel uses its own vertical scale to make changes in each severity category visible.",
    ha="center",
    fontsize=9
)

plt.tight_layout(rect=[0, 0.04, 1, 0.96])

plt.savefig(
    VISUALISATION_DIR / "06_collision_severity_by_year.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()


# ============================================================
# 10. COLLISION FREQUENCY BY SPEED LIMIT
# ============================================================

speed_limit_summary = (
    df["speed_limit"]
    .value_counts()
    .sort_index()
    .reset_index()
)

speed_limit_summary.columns = [
    "speed_limit_mph",
    "collision_count"
]

speed_limit_summary["percentage"] = (
    speed_limit_summary["collision_count"] / len(df) * 100
).round(2)

print("\n" + "=" * 60)
print("COLLISION FREQUENCY BY SPEED LIMIT")
print("=" * 60)

print(speed_limit_summary.to_string(index=False))


# ============================================================
# 10. COLLISION FREQUENCY BY SPEED LIMIT CHART
# ============================================================

# Exclude invalid speed-limit records from the chart
valid_speed_summary = speed_limit_summary[
    speed_limit_summary["speed_limit_mph"] != -1
].copy()

valid_speed_summary["speed_limit_label"] = (
    valid_speed_summary["speed_limit_mph"].astype(str) + " mph"
)

valid_speed_summary = valid_speed_summary.sort_values(
    "collision_count"
)

plt.figure(figsize=(10, 6))

bars = plt.barh(
    valid_speed_summary["speed_limit_label"],
    valid_speed_summary["collision_count"]
)

plt.title("Road Collisions by Speed Limit (2021–2025)")
plt.xlabel("Number of Collisions")
plt.ylabel("Speed Limit")

plt.bar_label(
    bars,
    labels=[
        f"{count:,} ({percentage:.1f}%)"
        for count, percentage in zip(
            valid_speed_summary["collision_count"],
            valid_speed_summary["percentage"]
        )
    ],
    padding=5
)

plt.tight_layout()

plt.savefig(
    VISUALISATION_DIR / "07_collisions_by_speed_limit.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()


# ============================================================
# 11. COLLISION FREQUENCY BY URBAN OR RURAL AREA
# ============================================================

area_summary = (
    df["urban_or_rural_area"]
    .value_counts()
    .sort_index()
    .reset_index()
)

area_summary.columns = [
    "area_code",
    "collision_count"
]

area_summary["percentage"] = (
    area_summary["collision_count"] / len(df) * 100
).round(2)

print("\n" + "=" * 60)
print("COLLISION FREQUENCY BY URBAN OR RURAL AREA")
print("=" * 60)

print(area_summary.to_string(index=False))


# ============================================================
# 11. COLLISION FREQUENCY BY URBAN OR RURAL AREA CHART
# ============================================================

area_labels = {
    1: "Urban",
    2: "Rural"
}

valid_area_summary = area_summary[
    area_summary["area_code"].isin(area_labels)
].copy()

valid_area_summary["area"] = (
    valid_area_summary["area_code"].map(area_labels)
)

plt.figure(figsize=(9, 5))

bars = plt.bar(
    valid_area_summary["area"],
    valid_area_summary["collision_count"]
)

plt.title("Road Collisions by Area Type (2021–2025)")
plt.xlabel("Area Type")
plt.ylabel("Number of Collisions")

plt.bar_label(
    bars,
    labels=[
        f"{count:,} ({percentage:.2f}%)"
        for count, percentage in zip(
            valid_area_summary["collision_count"],
            valid_area_summary["percentage"]
        )
    ],
    padding=5
)

plt.tight_layout()

plt.savefig(
    VISUALISATION_DIR / "08_collisions_by_area_type.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()


# ============================================================
# 12. COLLISION FREQUENCY BY WEATHER CONDITIONS
# ============================================================

weather_summary = (
    df["weather_conditions"]
    .value_counts()
    .sort_index()
    .reset_index()
)

weather_summary.columns = [
    "weather_code",
    "collision_count"
]

weather_summary["percentage"] = (
    weather_summary["collision_count"] / len(df) * 100
).round(2)

print("\n" + "=" * 60)
print("COLLISION FREQUENCY BY WEATHER CONDITIONS")
print("=" * 60)

print(weather_summary.to_string(index=False))


# ============================================================
# 12. COLLISION FREQUENCY BY WEATHER CONDITIONS CHART
# ============================================================

weather_labels = {
    -1: "Missing / out of range",
    1: "Fine, no high winds",
    2: "Rain, no high winds",
    3: "Snow, no high winds",
    4: "Fine, high winds",
    5: "Rain, high winds",
    6: "Snow, high winds",
    7: "Fog or mist",
    8: "Other",
    9: "Unknown"
}

weather_chart = weather_summary.copy()

weather_chart["weather"] = (
    weather_chart["weather_code"].map(weather_labels)
)

weather_chart = weather_chart.sort_values("collision_count")

plt.figure(figsize=(11, 7))

bars = plt.barh(
    weather_chart["weather"],
    weather_chart["collision_count"]
)

plt.title("Road Collisions by Weather Conditions (2021–2025)")
plt.xlabel("Number of Collisions")
plt.ylabel("Weather Conditions")

plt.bar_label(
    bars,
    labels=[
        f"{count:,} ({percentage:.2f}%)"
        for count, percentage in zip(
            weather_chart["collision_count"],
            weather_chart["percentage"]
        )
    ],
    padding=5,
    fontsize=8
)

plt.tight_layout()

plt.savefig(
    VISUALISATION_DIR / "09_collisions_by_weather.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()


road_surface_summary = (
    df["road_surface_conditions"]
    .value_counts()
    .sort_index()
    .reset_index()
)

road_surface_summary.columns = [
    "road_surface_code",
    "collision_count"
]

road_surface_summary["percentage"] = (
    road_surface_summary["collision_count"] / len(df) * 100
).round(2)

print("\nCOLLISIONS BY ROAD SURFACE CONDITION")
print(road_surface_summary.to_string(index=False))

road_surface_labels = {
    -1: "Missing or out of range",
    1: "Dry",
    2: "Wet or damp",
    3: "Snow",
    4: "Frost or ice",
    5: "Flood over 3cm deep",
    9: "Unknown"
}

road_surface_chart = road_surface_summary.copy()

road_surface_chart["road_surface"] = (
    road_surface_chart["road_surface_code"]
    .map(road_surface_labels)
)

road_surface_chart = road_surface_chart.sort_values(
    "collision_count"
)

plt.figure(figsize=(11, 6))

bars = plt.barh(
    road_surface_chart["road_surface"],
    road_surface_chart["collision_count"]
)

plt.title("Road Collisions by Road Surface Condition (2021–2025)")
plt.xlabel("Number of collisions")
plt.ylabel("Road surface condition")

for bar, percentage in zip(
    bars,
    road_surface_chart["percentage"]
):
    plt.text(
        bar.get_width(),
        bar.get_y() + bar.get_height() / 2,
        f" {int(bar.get_width()):,} ({percentage:.2f}%)",
        va="center"
    )

plt.tight_layout()

plt.savefig(
    VISUALISATION_DIR / "10_collisions_by_road_surface.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

light_summary = (
    df["light_conditions"]
    .value_counts()
    .sort_index()
    .reset_index()
)

light_summary.columns = [
    "light_condition_code",
    "collision_count"
]

light_summary["percentage"] = (
    light_summary["collision_count"] / len(df) * 100
).round(2)

print("\nCOLLISIONS BY LIGHT CONDITIONS")
print(light_summary.to_string(index=False))

light_labels = {
    -1: "Missing or out of range",
    1: "Daylight",
    4: "Darkness - lights lit",
    5: "Darkness - lights unlit",
    6: "Darkness - no lighting",
    7: "Darkness - lighting unknown"
}

light_chart = light_summary.copy()

light_chart["light_condition"] = (
    light_chart["light_condition_code"]
    .map(light_labels)
)

light_chart = light_chart.sort_values("collision_count")

plt.figure(figsize=(11, 6))

bars = plt.barh(
    light_chart["light_condition"],
    light_chart["collision_count"]
)

plt.title("Road Collisions by Light Conditions (2021–2025)")
plt.xlabel("Number of collisions")
plt.ylabel("Light condition")

for bar, percentage in zip(
    bars,
    light_chart["percentage"]
):
    plt.text(
        bar.get_width(),
        bar.get_y() + bar.get_height() / 2,
        f" {int(bar.get_width()):,} ({percentage:.2f}%)",
        va="center"
    )

plt.tight_layout()

plt.savefig(
    VISUALISATION_DIR / "11_collisions_by_light_conditions.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

road_type_summary = (
    df["road_type"]
    .value_counts()
    .sort_index()
    .reset_index()
)

road_type_summary.columns = [
    "road_type_code",
    "collision_count"
]

road_type_summary["percentage"] = (
    road_type_summary["collision_count"] / len(df) * 100
).round(2)

print("\nCOLLISIONS BY ROAD TYPE")
print(road_type_summary.to_string(index=False))

road_type_labels = {
    1: "Roundabout",
    2: "One-way street",
    3: "Dual carriageway",
    6: "Single carriageway",
    7: "Slip road",
    9: "Unknown"
}

road_type_chart = road_type_summary.copy()

road_type_chart["road_type"] = (
    road_type_chart["road_type_code"]
    .map(road_type_labels)
)

road_type_chart = road_type_chart.sort_values(
    "collision_count"
)

plt.figure(figsize=(11, 6))

bars = plt.barh(
    road_type_chart["road_type"],
    road_type_chart["collision_count"]
)

plt.title("Road Collisions by Road Type (2021–2025)")
plt.xlabel("Number of collisions")
plt.ylabel("Road type")

for bar, percentage in zip(
    bars,
    road_type_chart["percentage"]
):
    plt.text(
        bar.get_width(),
        bar.get_y() + bar.get_height() / 2,
        f" {int(bar.get_width()):,} ({percentage:.2f}%)",
        va="center"
    )

plt.tight_layout()

plt.savefig(
    VISUALISATION_DIR / "12_collisions_by_road_type.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

junction_summary = (
    df["junction_detail"]
    .value_counts()
    .sort_index()
    .reset_index()
)

junction_summary.columns = [
    "junction_detail_code",
    "collision_count"
]

junction_summary["percentage"] = (
    junction_summary["collision_count"] / len(df) * 100
).round(2)

print("\nCOLLISIONS BY JUNCTION DETAIL")
print(junction_summary.to_string(index=False))

junction_labels = {
    -1: "Missing or out of range",
    0: "Not at junction or within 20 metres",
    13: "T or staggered junction",
    16: "Crossroads",
    17: "Junction with more than four arms",
    18: "Private drive or entrance",
    19: "Other junction",
    99: "Unknown (self reported)"
}

junction_chart = junction_summary.copy()

junction_chart["junction_detail"] = (
    junction_chart["junction_detail_code"]
    .map(junction_labels)
)

junction_chart = junction_chart.sort_values("collision_count")

plt.figure(figsize=(12, 7))

bars = plt.barh(
    junction_chart["junction_detail"],
    junction_chart["collision_count"]
)

plt.title("Road Collisions by Junction Detail (2021–2025)")
plt.xlabel("Number of collisions")
plt.ylabel("Junction detail")

for bar, percentage in zip(
    bars,
    junction_chart["percentage"]
):
    plt.text(
        bar.get_width(),
        bar.get_y() + bar.get_height() / 2,
        f" {int(bar.get_width()):,} ({percentage:.2f}%)",
        va="center"
    )

plt.tight_layout()

plt.savefig(
    VISUALISATION_DIR / "13_collisions_by_junction_detail.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()