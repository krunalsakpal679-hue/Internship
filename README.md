# Train Schedule Analysis and Interactive Route Enquiry System

**Sysslan IT Solutions Internship Project**  
**Author**: Krunal Sakpal  
**Technology Stack**: Python 3.14, Pandas, NumPy, Matplotlib, Seaborn, Pytest  
**Repository**: [https://github.com/krunalsakpal679-hue/Internship.git](https://github.com/krunalsakpal679-hue/Internship.git)  

---

## 1. Project Overview

The **Train Schedule Analysis and Interactive Route Enquiry System** is an end-to-end Python data engineering, exploratory data analysis (EDA), and interactive search application built on Indian Railways schedule data. 

The project ingests **186,074 station-level halt records**, reconstructs discrete train journeys across **11,113 unique trains** and **8,147 railway stations**, performs multi-tier data cleaning and monotonicity validation, derives national transit insights through cross-tabulations and publication-grade charts, and provides an instant command-line route enquiry engine (< 5ms response latency).

---

## 2. Dataset Architecture & Raw Schema

The read-only source of truth is stored at [`data/raw/Dataset1.csv`](file:///c:/Internship/data/raw/Dataset1.csv) (SHA-256: `8353639af562e88ceb8feb26454221d50fc97b38dc752e3fe6a7a0235f9ecd57`).

> [!IMPORTANT]
> **Data Model Constraint**: Each row in `Dataset1.csv` represents an **individual station halt along a train route**, NOT an entire train. Individual trains are reconstructed by grouping rows on `Train_No` and ordering them by sequence number (`SN`) and track distance (`Distance`).

### Dataset Specifications
- **Total Station-Level Rows**: 186,074 rows
- **Unique Trains**: 11,113 distinct train numbers
- **Unique Station Codes**: 8,147 alpha codes
- **Unique Station Names**: 8,099 distinct station names
- **Missing / Null Values**: Exactly 0 missing values across all 12 raw columns

### Column Schema
| Column Name | Ingestion Dtype | Description |
| :--- | :--- | :--- |
| `SN` | String / Object | Stop sequence index along the train route |
| `Train_No` | String / Object | Unique train service identifier (e.g. `'11005'`, `'290'`) |
| `Station_Code` | String / Object | Official Indian Railways alpha code (e.g. `'CSMT'`, `'NAN'`) |
| `1A` | Numeric (`int64`) | AC First Class fare tariff metric ($100 + 5 \times \text{Distance}$) |
| `2A` | Numeric (`int64`) | AC 2-Tier fare tariff metric ($100 + 4 \times \text{Distance}$) |
| `3A` | Numeric (`int64`) | AC 3-Tier fare tariff metric ($100 + 3 \times \text{Distance}$) |
| `SL` | Numeric (`int64`) | Sleeper Class fare tariff metric ($100 + 2 \times \text{Distance}$) |
| `Station_Name` | String / Object | Full official station name (e.g. `'CST-MUMBAI'`) |
| `Route_Number` | String / Object | Route variant identifier (uniformly `'1'` across all rows) |
| `Arrival_time` | String / Object | Scheduled arrival timestamp (`%H:%M:%S`) |
| `Departure_Time`| String / Object | Scheduled departure timestamp (`%H:%M:%S`) |
| `Distance` | Numeric (`int64`) | Cumulative track distance from origin in kilometers (0 to 4,260 km) |

---

## 3. Project Structure

```text
c:\Internship\
├── app/
│   └── train_enquiry.py          # Interactive Route Enquiry CLI application
├── data/
│   ├── raw/
│   │   └── Dataset1.csv          # Read-only master raw dataset (186,074 rows)
│   └── processed/
│       ├── dataset_dedup.csv     # Intermediate deduplicated schedule data
│       └── dataset_verified.csv  # Final verified analytical dataset (21 columns)
├── documentation/
│   ├── level1/ to level6/        # Per-task documentation notes (21 files)
│   ├── technical_documentation.md# Complete system architecture and methodology report
│   ├── task_tracker.csv          # 21-task completion and artifact mapping ledger
│   ├── git_checkpoint_tracker.csv# 9-checkpoint phase-based Git tracking ledger
│   ├── session_log.md            # Comprehensive chronological session audit log
│   └── testing_summary.md        # QA test suite and mutation testing report
├── outputs/
│   ├── charts/                   # High-resolution visualization PNGs (150 DPI)
│   ├── tables/                   # Tabular CSV outputs and analytical summaries
│   └── reports/                  # Detailed markdown reports and audit logs
├── screenshots/
│   ├── level1/ to level6/        # Verification screenshot evidence (21 task PNGs)
│   └── testing/                  # Checkpoint 6 pytest execution evidence
├── src/
│   ├── level0/                   # Dataset audit logic
│   ├── level1/                   # Level 1: Basic data review scripts
│   ├── level2/                   # Level 2: Simple data processing scripts
│   ├── level3/                   # Level 3: Data quality & cleaning scripts
│   ├── level4/                   # Level 4: Exploratory data analysis & visualizations
│   ├── level5/                   # Level 5: Advanced analysis & cross-tabulations
│   ├── level6/                   # Level 6: Application runners
│   ├── testing/                  # Pytest report and evidence generators
│   └── validation/               # 9-part evidence chain audit script
├── tests/                        # Modular pytest test suite (11 test modules, 83 tests)
├── .gitignore                    # Python, environment, and cache ignore rules
├── requirements.txt              # Dependency manifest
└── README.md                     # Project documentation
```

---

## 4. Setup & Installation

### Prerequisites
- Python 3.10+ (tested on Python 3.14.3)
- Git 2.40+

### Step-by-Step Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/krunalsakpal679-hue/Internship.git
   cd Internship
   ```

2. **Create & Activate Virtual Environment**:
   ```bash
   # On Windows PowerShell:
   python -m venv .venv
   .venv\Scripts\Activate.ps1

   # On Linux / macOS:
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify Environment**:
   ```bash
   python -m pytest
   ```

---

## 5. How to Run Pipeline Scripts & Application

### 5.1. Interactive Route Enquiry System (Level 6 CLI Application)
Launch the interactive CLI search tool to find direct trains between any two Indian Railways stations:
```bash
python app/train_enquiry.py
```
- **Usage**: Enter source and destination station codes (e.g. `CSMT`, `KYN`) or full station names (e.g. `CST-MUMBAI`, `KALYAN JN`).
- **Options**: Type `help` for search tips, `sample` to run built-in test routes, or `exit` to quit.

To execute automated batch verification of test scenarios:
```bash
python src/level6/task_6_1_runner.py
```

### 5.2. Running Analytical Level Pipelines
Run scripts individually by analytical level:

* **Level 0 (Dataset Audit)**:
  ```bash
  python src/level0/dataset_audit.py
  ```
* **Level 1 (Basic Data Review)**:
  ```bash
  python src/level1/task_1_1_overview.py
  python src/level1/task_1_2_start_end.py
  python src/level1/task_1_3_stops_per_train.py
  python src/level1/task_1_4_max_min_stops.py
  ```
* **Level 2 (Simple Data Processing)**:
  ```bash
  python src/level2/task_2_1_standardize_times.py
  python src/level2/task_2_2_journey_duration.py
  python src/level2/task_2_3_route_classification.py
  python src/level2/task_2_4_station_frequency.py
  ```
* **Level 3 (Data Quality & Verified Dataset)**:
  ```bash
  python src/level3/task_3_1_missing_values.py
  python src/level3/task_3_2_duplicates.py
  python src/level3/task_3_3_station_order.py
  python src/level3/task_3_4_save_verified.py
  ```
* **Level 4 (Exploratory Analysis & Visualizations)**:
  ```bash
  python src/level4/task_4_1_duration_comparison.py
  python src/level4/task_4_2_high_traffic_stations.py
  python src/level4/task_4_3_visualizations.py
  python src/level4/task_4_4_summary_insights.py
  ```
* **Level 5 (Advanced Pivot Tables & Cross-tabulations)**:
  ```bash
  python src/level5/task_5_1_pivot_tables.py
  python src/level5/task_5_2_crosstab.py
  python src/level5/task_5_3_comparative_charts.py
  python src/level5/task_5_4_advanced_insights.py
  ```
* **Evidence Chain Audit & Quality Report**:
  ```bash
  python src/validation/evidence_audit.py
  python src/testing/generate_test_report.py
  ```

---

## 6. Automated Testing & Quality Assurance

The project includes an automated test suite executed via `pytest`:

```bash
python -m pytest -v
```

### Test Suite Architecture (83 Tests / 100% Pass)
| Test Module | Scope & Invariants Validated | Tests |
| :--- | :--- | :---: |
| [`tests/test_foundation.py`](file:///c:/Internship/tests/test_foundation.py) | Directory layout, raw dataset presence, task and checkpoint trackers | 3 |
| [`tests/test_audit.py`](file:///c:/Internship/tests/test_audit.py) | Raw dataset completeness, schema verification, audit markdown | 2 |
| [`tests/test_dataset.py`](file:///c:/Internship/tests/test_dataset.py) | SHA-256 raw immutability, zero-null invariant, Nanogaon protection | 4 |
| [`tests/test_processing.py`](file:///c:/Internship/tests/test_processing.py) | Time parsing, midnight rollover duration math, route classification terciles | 4 |
| [`tests/test_analysis.py`](file:///c:/Internship/tests/test_analysis.py) | Station frequency integrity, pivot & cross-tab reconciliation, chart artifacts | 3 |
| [`tests/test_enquiry_system.py`](file:///c:/Internship/tests/test_enquiry_system.py) | Valid queries, disconnected city pairs, invalid stations, same-station rejection | 6 |
| [`tests/test_level1.py`](file:///c:/Internship/tests/test_level1.py) | Level 1 dataset overview, start/end stations, stop counts | 5 |
| [`tests/test_level2.py`](file:///c:/Internship/tests/test_level2.py) | Level 2 standardized times, journey durations, terciles, station frequencies | 14 |
| [`tests/test_level3.py`](file:///c:/Internship/tests/test_level3.py) | Level 3 missing values, deduplication, distance monotonicity, verified dataset | 14 |
| [`tests/test_level4.py`](file:///c:/Internship/tests/test_level4.py) | Level 4 duration comparisons, high-traffic hubs, visualizations, insights | 10 |
| [`tests/test_level5.py`](file:///c:/Internship/tests/test_level5.py) | Level 5 pivot tables, structural cross-tabs, heatmap/bar charts, advanced insights | 9 |
| [`tests/test_train_enquiry.py`](file:///c:/Internship/tests/test_train_enquiry.py) | Level 6 CLI application fixtures, duration helpers, and 5 mandatory scenarios | 9 |
| **TOTAL** | **Comprehensive Full Pipeline Coverage** | **83 / 83** |

---

## 7. Summary of Key Analytical Findings

All analytical observations are grounded in verifiable dataset calculations:

1. **Duration Hierarchy Reflects Three Service Paradigms**:
   - **Short Routes** ($\le 80$ min): 3,860 trains (34.73%) | Mean duration **49.50 min** (0.82 h, median 52.0 m).
   - **Medium Routes** (81–240 min): 3,518 trains (31.66%) | Mean duration **142.02 min** (2.37 h, median 135.0 m).
   - **Long Routes** ($> 240$ min): 3,735 trains (33.61%) | Mean duration **637.34 min** (10.62 h, median 555.0 m).
   *(Source: [`outputs/tables/task_4_1_duration_by_route_type.csv`](file:///c:/Internship/outputs/tables/task_4_1_duration_by_route_type.csv))*

2. **Top-Decile Hub Rule (80/20 Transit Criticality)**:
   - Applying the 90th percentile cutoff ($\ge 48$ trains) isolates **830 high-traffic stations** (10.19% of network stations) handling the vast majority of national rail movements, while 89.8% (7,317 stations) operate as low-frequency halts (median 10 trains).
   - Top national hubs: **CSMT (CST-Mumbai, 1,027 trains)**, **KYN (Kalyan Jn, 828 trains)**, **TNA (Thane, 796 trains)**, **SDAH (Sealdah, 745 trains)**, **MSB (Chennai Beach, 738 trains)**, **HWH (Howrah Jn, 699 trains)**.
   *(Source: [`outputs/tables/task_4_2_high_traffic_stations.csv`](file:///c:/Internship/outputs/tables/task_4_2_high_traffic_stations.csv))*

3. **Fleet Structural Composition & Route Alignment**:
   - `1xxxx` (Mail/Express): Contributes **1,998 Long routes** (53.49% of all Long routes nationwide).
   - `9xxxx` (Mumbai Suburban): Supplies **1,578 Short routes** (40.88% of all Short routes nationwide).
   - `5xxxx` (Conventional Passenger): Provides **2,137 trains** spanning Long (954), Medium (894), and Short (289).
   *(Source: [`outputs/tables/task_5_2_route_crosstab.csv`](file:///c:/Internship/outputs/tables/task_5_2_route_crosstab.csv))*

---

## 8. Known Limitations & Methodological Disclosures

1. **Timetable Date Offsets**: The raw schedule dataset does not contain calendar days or multi-day trip offsets (Day 1, Day 2). Overnight journeys are modeled with single-day midnight rollover ($\Delta T \pmod{1440\text{ min}}$).
2. **Excluded Unresolvable Trains**: Exactly **6 trains** (0.054% of network) exhibited identical start and end clock times in the raw timetable, yielding 0-minute duration markers; these are flagged and safely excluded from duration averages with zero sample distortion.
3. **Station Name Variants**: 48 station names share identical names across different railway zones; station alpha codes (`Station_Code`) serve as the unambiguous primary key.
4. **Direct Journey Routing**: The CLI enquiry engine is designed for direct single-train routing and does not evaluate multi-leg transfers.

---

## 9. Acknowledgements & Credits

This project was developed by **Krunal Sakpal** as part of the **Sysslan IT Solutions Internship Program**.  
Sincere gratitude to the mentors and engineering team at Sysslan IT Solutions for their guidance on data quality standards, software engineering principles, and data analysis practices.
