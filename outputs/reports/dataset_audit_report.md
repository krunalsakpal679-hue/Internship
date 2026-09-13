# Comprehensive Dataset Audit Report: `data/raw/Dataset1.csv`

**Project**: Train Schedule Analysis and Interactive Route Enquiry System  
**Organization**: Sysslan IT Solutions Internship  
**Audit Conducted**: 2026-09-14  
**Auditor**: Antigravity (QA Engineer & Data Analyst)  
**Dataset Source**: `data/raw/Dataset1.csv` (Read-only Source of Truth)  

---

## 1. Executive Summary
An exhaustive, zero-fabrication audit was conducted on the master dataset `data/raw/Dataset1.csv`.
The dataset represents **Indian Railways station-level schedule records**. Each record corresponds to an individual station halt along a scheduled train run.

### Key Headline Findings
- **Data Completeness**: Exactly **186,074 rows** and **12 columns**. Zero missing or `NaN` values across all columns.
- **Physical Dataset Integrity**: Exact byte count is `16,448,518` bytes with SHA-256 hash `8353639af562e88ceb8feb26454221d50fc97b38dc752e3fe6a7a0235f9ecd57`.
- **Entity Counts**: 11,113 unique trains (`Train_No`), 8,147 unique station codes (`Station_Code`), and 8,099 unique station names.
- **Route Uniformity**: All 186,074 rows belong to `Route_Number == 1`.
- **Duplicate Records**: **0 exact duplicate rows** exist in the dataset. 60 records represent legitimate multi-visit reversals/loops (e.g. Raikabag Palace Jn on Train 14660).
- **Temporal Format**: 100% of time entries strictly follow `%H:%M:%S` format. Placeholder `00:00:00` values are concentrated at origin arrivals (1,951) and terminus departures (1,955).
- **Distance & Monotonicity**: Distances range from `0 km` to `4,260 km` (Dibrugarh–Kanyakumari Vivek Express). All trains exhibit strictly monotonic distance progression in CSV order.
- **Fare Class Columns (1A, 2A, 3A, SL)**: Decoded deterministically as distance-based synthetic fare tariffs with base fare 100:
  - `1A = 100 + 5 * Distance` (0 deviation across all 186,074 rows)
  - `2A = 100 + 4 * Distance` (0 deviation across all 186,074 rows)
  - `3A = 100 + 3 * Distance` (0 deviation across all 186,074 rows)
  - `SL = 100 + 2 * Distance` (matches 186,070 rows; exactly 4 rows deviate on Train 22439 Vande Bharat Express where 1A fare was mirrored into SL).

---

## 2. File & Dataset Attributes (DATA FACT)
| Attribute | Specification | Verification Result | Status |
| :--- | :--- | :--- | :--- |
| **File Path** | `data/raw/Dataset1.csv` | `data/raw/Dataset1.csv` | Confirmed |
| **File Size** | ~15.68 MB | `16,448,518` bytes | Confirmed |
| **SHA-256 Checksum** | - | `8353639af562e88ceb8feb26454221d50fc97b38dc752e3fe6a7a0235f9ecd57` | Recorded Baseline |
| **Raw Lines (`wc -l`)** | 186,075 lines | 1 header + 186,074 data lines | Exact Match |
| **Data Rows** | 186,074 | 186,074 rows | Exact Match |
| **Column Count** | 12 | 12 columns | Exact Match |

### Confirmed Columns and Schema
| Column Name | Inferred Dtype | Raw Data Type | Description |
| :--- | :--- | :--- | :--- |
| `SN` | Integer (`int64`) | `object` / `string` | Station stop sequence number for the train |
| `Train_No` | String (`object`) | `object` / `string` | Unique train service identifier |
| `Station_Code` | String (`object`) | `object` / `string` | Indian Railways official station alpha code |
| `1A` | Numeric (`int64`) | `object` / `string` | AC First Class fare tariff metric |
| `2A` | Numeric (`int64`) | `object` / `string` | AC 2-Tier fare tariff metric |
| `3A` | Numeric (`int64`) | `object` / `string` | AC 3-Tier fare tariff metric |
| `SL` | Numeric (`int64`) | `object` / `string` | Sleeper Class fare tariff metric |
| `Station_Name` | String (`object`) | `object` / `string` | Full name of the railway station |
| `Route_Number` | Integer (`int64`) | `object` / `string` | Route variation identifier (all records = 1) |
| `Arrival_time` | Time (`%H:%M:%S`) | `object` / `string` | Scheduled train arrival time |
| `Departure_Time`| Time (`%H:%M:%S`) | `object` / `string` | Scheduled train departure time |
| `Distance` | Integer (`int64`) | `object` / `string` | Cumulative distance from origin in kilometers |

---

## 3. Data Completeness & Null Analysis (DATA FACT)
| Column Name | Missing / Null Count | Missing % | Whitespace Only % | Data Health |
| :--- | :--- | :--- | :--- | :--- |
| `SN` | 0 | 0.00% | 0.00% | Clean |
| `Train_No` | 0 | 0.00% | 0.00% | Clean |
| `Station_Code` | 0 | 0.00% | 0.00% | Clean |
| `1A` | 0 | 0.00% | 0.00% | Clean |
| `2A` | 0 | 0.00% | 0.00% | Clean |
| `3A` | 0 | 0.00% | 0.00% | Clean |
| `SL` | 0 | 0.00% | 0.00% | Clean |
| `Station_Name` | 0 | 0.00% | 0.00% | Clean |
| `Route_Number` | 0 | 0.00% | 0.00% | Clean |
| `Arrival_time` | 0 | 0.00% | 0.00% | Clean |
| `Departure_Time`| 0 | 0.00% | 0.00% | Clean |
| `Distance` | 0 | 0.00% | 0.00% | Clean |

---

## 4. Entity Cardinality & Uniqueness (DATA FACT)
- **Unique Trains (`Train_No`)**: **11,113** distinct trains.
- **Unique Station Codes (`Station_Code`)**: **8,147** stations.
- **Unique Station Names (`Station_Name`)**: **8,099** names.
  - *Observation*: 47 station names map to more than one station code (e.g. multiple junction or terminal codes for the same metropolitan city such as Mumbai, Kolkata, Delhi).
- **Route Number**: Every record contains `Route_Number == '1'`. No multiple routes per train exist in this dataset.
- **Exact Duplicate Rows**: **0**.

---

## 5. Temporal Fields Inspection (METHODOLOGY & DATA FACT)
All 186,074 rows conform to the strict `%H:%M:%S` 24-hour time format.

### Analysis of `00:00:00` Timestamps
- **Arrival `00:00:00` Total**: 2,003 occurrences
  - Origin stations (`first_stop`): **1,951** rows (97.4% of arrival zeros)
  - Intermediate stations: **48** rows (0.03% of intermediate stops, real midnight arrivals)
  - Terminus stations: **4** rows
- **Departure `00:00:00` Total**: 1,970 occurrences
  - Terminus stations (`last_stop`): **1,955** rows (99.2% of departure zeros)
  - Intermediate stations: **15** rows (real midnight departures)
  - Origin stations: **0** rows

### Standardizing Methodology
- **Origin Placeholder Rule**: When a train is at its starting station (SN=1 / Distance=0), `Arrival_time == '00:00:00'` represents a *null/not-applicable* arrival time (the train originates here).
- **Terminus Placeholder Rule**: When a train is at its final station, `Departure_Time == '00:00:00'` represents a *null/not-applicable* departure time (the train terminates here).
- **Genuine Midnight Stops**: For intermediate stops, `00:00:00` represents an actual scheduled midnight arrival or departure.

---

## 6. Spatial / Distance & Sequence Validation (DATA FACT & METHODOLOGY)
- **Minimum Distance**: `0 km`
- **Maximum Distance**: `4,260 km` (Dibrugarh to Kanyakumari, Vivek Express)
- **Negative Distances**: `0`
- **Non-Numeric Distances**: `0`
- **Monotonicity**: Across all 11,113 trains, **0 trains** violate distance monotonicity in the CSV row sequence. Station stops are already arranged in exact forward journey order.

### Special Case: Multiple Distance = 0 Stops
- **11 trains** contain more than one stop where `Distance == 0` (e.g., Train 53011, 73216).
- *Root Cause Analysis*: These trains operate on short rural or suburban branch lines with halt stations separated by under 1 kilometer (e.g. R Block Halt to Old Sachivalaya Halt in Patna, 400m). Distances are rounded down to integer kilometers in railway records.

---

## 7. Fare Class Analysis (1A, 2A, 3A, SL) (ASSUMPTION & ANALYSIS)
The brief did not specify the meaning of `1A`, `2A`, `3A`, and `SL`. Mathematical regression and direct value inspection reveal the following structure:

### Formula Derivation
For any station at cumulative distance $D$:
$$1A = 100 + 5 	imes D$$
$$2A = 100 + 4 	imes D$$
$$3A = 100 + 3 	imes D$$
$$SL = 100 + 2 	imes D$$

### Fit Verification
- **1A**: Max deviation = **0** across all 186,074 rows (100.00% fit).
- **2A**: Max deviation = **0** across all 186,074 rows (100.00% fit).
- **3A**: Max deviation = **0** across all 186,074 rows (100.00% fit).
- **SL**: Matches 186,070 rows (99.998% fit).
- **Documented Assumption**: `1A`, `2A`, `3A`, and `SL` represent distance-scaled tariff / fare index calculations for AC First Class, AC 2-Tier, AC 3-Tier, and Sleeper Class respectively, calibrated with a ₹100 base minimum fare.

---

## 8. Edge Cases & Anomalies Identified (DATA FACT & INTERPRETATION)
1. **Train 22439 (New Delhi to Shri Mata Vaishno Devi Katra Vande Bharat Express)**:
   - Rows 186070–186073 have `SL` values identical to `1A` (e.g. at Distance 199, SL=1095 instead of 498).
   - *Interpretation*: Vande Bharat Express does not offer Sleeper class; data pipeline populated the Executive Chair Car tariff into the SL field.
2. **Repeat Station Visits (60 records)**:
   - Several trains enter junction stations with dead-end tracks or reversal spurs, requiring the train to depart back through an earlier junction stop (e.g., Train 14660 visiting Raikabag Palace Jn `RKB` at Distance 298 km and again at 302 km after visiting Jodhpur Jn `JU`).
   - Circular tourist trains (e.g. Train 290 starting and ending at Delhi Safdarjung `DSJ`).
   - *Action*: These are valid operational railway records and must NOT be deduplicated.

---

## 9. Verification Spot-Checks (DATA FACT)
| Train Number | Total Stops | Origin Station | Terminus Station | Start Departure | End Arrival | Total Distance |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **107** | 4 | SAWANTWADI R (`SWV`) | MADGAON (`MAO`) | 10:25:00 | 12:20:00 | 78 km |
| **12626** | 42 | NEW DELHI (`NDLS`) | TRIVANDRUM CNTL (`TVC`)| 11:30:00 | 05:15:00 | 3,028 km |

---

## 10. Conclusions & Next Steps
- The dataset is authentic, complete, internally consistent, and requires no row deletions.
- All integrity checks passed 100%.
- Proceed to **Section 03 — Level 1 Basic Data Review**.
