# Data Sources

## 1. Data Provider

The datasets used in this project are published by the **UK Department for Transport (DfT)** through its official Road Safety Open Data service.

**Official source:**  
https://www.gov.uk/government/statistical-data-sets/road-safety-open-data

## 2. Datasets Used

This project uses three official CSV datasets covering the latest five-year period selected for analysis (2021–2025).

| Dataset | File | Records |
|---|---|---:|
| Collisions | `dft-road-casualty-statistics-collision-last-5-years.csv` | 513,801 |
| Vehicles | `dft-road-casualty-statistics-vehicle-last-5-years.csv` | 937,265 |
| Casualties | `dft-road-casualty-statistics-casualty-last-5-years.csv` | 652,821 |
| **Total** | | **2,103,887** |

## 3. Data Documentation

The official DfT Open Dataset Data Guide (2025) is also used to understand the dataset structure, column definitions and numerical classification codes.

**Data guide:**  
https://www.gov.uk/government/statistical-data-sets/road-safety-open-data

Local file: `documentation/dft-road-casualty-statistics-road-safety-open-dataset-data-guide-2025.xlsx`

## 4. Data Scope

The project analyses reported road collisions, vehicles and casualties in Great Britain between 2021 and 2025.

The datasets are linked using `collision_index`, allowing collision records to be connected with their associated vehicles and casualties.

## 5. Data Storage

The original CSV datasets are stored locally in the project's `data/raw/` directory and are excluded from the GitHub repository because of their file sizes.

Users wishing to reproduce the analysis should download the corresponding datasets directly from the official DfT source.

## 6. Data Usage and Attribution

The original datasets remain the property of their respective publishers and are subject to the terms of use stated by the Department for Transport.

The Python scripts, SQL queries, analysis and visualisations developed for this project are original project work. The project's MIT licence applies to the original code, not automatically to the third-party datasets.