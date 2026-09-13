# Session Log

## Session 1: Master Controller State Inspection
- **Date / Timestamp**: 2026-09-14T02:41:00+05:30
- **Repository Remote**: `https://github.com/krunalsakpal679-hue/Internship.git`
- **Branch**: `main`
- **Git State**: Clean / Empty repository (No commits yet)
- **Dataset Location**: Found at `C:\Users\krunal\Downloads\Dataset1.csv` (to be placed at `data/raw/Dataset1.csv` during Phase 0 initialization)
- **Last Stable Checkpoint**: None (New project)
- **Current Phase**: Phase 0 — Project Foundation (Checkpoint 0)
- **Next Task to Execute**: Section 01 — Project Initialization Prompt (Setup folder structure, place raw dataset in `data/raw/Dataset1.csv`, create `requirements.txt`, `.gitignore`, `README.md` skeleton, `documentation/task_tracker.csv`, and `documentation/git_checkpoint_tracker.csv`).

## Session 2: Phase 0 — Project Initialization (Checkpoint 0)
- **Date / Timestamp**: 2026-09-14T02:49:00+05:30
- **Environment**: Python 3.14.3 / pip 26.0.1 (verified), Pytest 8.0.2 / 9.0.2
- **Dataset Placed**: `data/raw/Dataset1.csv` (16,448,518 bytes, 186,074 data rows, SHA256: `8353639af562e88ceb8feb26454221d50fc97b38dc752e3fe6a7a0235f9ecd57`)
- **Root Dataset**: User original preserved at `Dataset1.csv` in root and excluded from Git tracking via `.gitignore`
- **Directories Created**:
  - `data/raw/`, `data/processed/`
  - `notebooks/`
  - `src/level0/` through `src/level6/`, `src/validation/`
  - `app/`
  - `outputs/charts/`, `outputs/tables/`, `outputs/reports/`
  - `screenshots/level1/` through `screenshots/level6/`
  - `documentation/level1/` through `documentation/level6/`
  - `tests/`
- **Files Created**:
  - `requirements.txt` (pandas, numpy, matplotlib, seaborn, pytest, python-docx)
  - `.gitignore` (Python standards, cache, environment, root duplicate dataset)
  - `README.md` (Project skeleton and setup documentation)
  - `main.py` (Pipeline entrypoint)
  - `documentation/task_tracker.csv` (21 tasks defined from Table 2)
  - `documentation/git_checkpoint_tracker.csv` (9 checkpoints tracking from Table 34)
  - `tests/test_foundation.py` (Automated structure verification test)
- **Automated Validation**: `pytest -v` executed, 3/3 tests PASSED.
- **Git Checkpoint Status**: Checkpoint 0 successfully committed (`76f3ceb`) and pushed to GitHub main.

## Session 3: Dataset Audit (Section 02)
- **Date / Timestamp**: 2026-09-14T02:58:00+05:30
- **Scope**: Comprehensive statistical and structural audit of `data/raw/Dataset1.csv`.
- **Implementation**: `src/level0/dataset_audit.py`
- **Audit Findings**:
  - Exact file size: 16,448,518 bytes (~15.69 MB).
  - SHA-256: `8353639af562e88ceb8feb26454221d50fc97b38dc752e3fe6a7a0235f9ecd57`.
  - Raw line count: 186,075 (1 header + 186,074 data rows). 12 columns.
  - Zero missing/null values across all columns.
  - Zero exact duplicate rows.
  - Unique counts: 11,113 trains, 8,147 station codes, 8,099 station names, 1 route number (`'1'`).
  - Distance: 0 to 4,260 km, zero negatives, 100% strictly monotonic per train sequence.
  - Time format: 100% `%H:%M:%S`. 00:00:00 occurrences isolated to origin arrivals (1,951) and terminus departures (1,955), with 48 genuine midnight arrivals.
  - Fare class derivation: Deterministic fit `Fare = 100 + Rate * Distance` (1A=5/km, 2A=4/km, 3A=3/km, SL=2/km) with 1 anomaly identified on Vande Bharat train 22439.
- **Artifacts Generated**:
  - `outputs/reports/dataset_audit_report.md`
  - `screenshots/level1/dataset_audit.png`
  - `documentation/level1/dataset_audit.txt`
  - `tests/test_audit.py`
- **Git Checkpoint**: Per Section 24, individual tasks are not committed separately; audit artifacts will be bundled with Level 1 into Checkpoint 1.

## Session 4: Task 1.1 — Dataset Overview (Level 1)
- **Date / Timestamp**: 2026-09-14T03:01:00+05:30
- **Task ID**: 1.1 (Level 1)
- **Status**: COMPLETED
- **Implementation**: `src/level1/task_1_1_overview.py`
- **Output Artifact**: `outputs/tables/task_1_1_dataset_overview.csv`
- **Evidence Screenshot**: `screenshots/level1/task_1_1.png`
- **Documentation**: `documentation/level1/task_1_1.txt`
- **Test File**: `tests/test_level1.py`
- **Factual Results**:
  - Total records: 186,074 rows, 12 columns
  - Raw lines: 186,075 (1 header + 186,074 data lines)
  - Memory usage: 66.79 MB
  - Unique trains: 11,113; Unique station codes: 8,147; Unique station names: 8,099
  - Route numbers: 1; Missing values: 0; Duplicates: 0
- **Validation**: `python -m pytest -v` executed, 7/7 tests PASSED (100%).
- **Task Tracker**: Updated `documentation/task_tracker.csv` row 1.1 to `COMPLETED`.
- **Git Checkpoint**: Uncommitted (bundled into Checkpoint 1 upon completion of Tasks 1.1–1.4).

## Session 5: Task 1.2 — Starting and Ending Stations per Train (Level 1)
- **Date / Timestamp**: 2026-09-14T03:03:00+05:30
- **Task ID**: 1.2 (Level 1)
- **Status**: COMPLETED
- **Implementation**: `src/level1/task_1_2_start_end.py`
- **Output Artifact**: `outputs/tables/task_1_2_start_end_stations.csv`
- **Evidence Screenshot**: `screenshots/level1/task_1_2.png`
- **Documentation**: `documentation/level1/task_1_2.txt`
- **Test File**: `tests/test_level1.py`
- **Factual Results**:
  - Total trains analyzed: 11,113 (100% match with raw distinct `Train_No`)
  - Null start stations: 0; Null end stations: 0
  - Monotonicity verified across all trains
  - Spot checks verified: Train 107 (SWV -> MAO, 4 stops), Train 12626 (NDLS -> TVC, 42 stops), Train 12951 (BCT -> NDLS, 8 stops)
- **Validation**: `python -m pytest -v` executed, 8/8 tests PASSED (100%).
- **Task Tracker**: Updated `documentation/task_tracker.csv` row 1.2 to `COMPLETED`.
- **Git Checkpoint**: Uncommitted (bundled into Checkpoint 1 upon completion of Tasks 1.1–1.4).

## Session 6: Task 1.3 — Number of Stops per Train (Level 1)
- **Date / Timestamp**: 2026-09-14T03:05:00+05:30
- **Task ID**: 1.3 (Level 1)
- **Status**: COMPLETED
- **Implementation**: `src/level1/task_1_3_stops_per_train.py`
- **Output Artifact**: `outputs/tables/task_1_3_stops_per_train.csv`
- **Evidence Screenshot**: `screenshots/level1/task_1_3.png`
- **Documentation**: `documentation/level1/task_1_3.txt`
- **Test File**: `tests/test_level1.py`
- **Factual Results**:
  - Total trains analyzed: 11,113 (100% matched)
  - Total sum of stops: 186,074 (exact match with raw row count)
  - Reconciled with Task 1.2 `Total_Stations`: 100% (0 mismatches across 11,113 trains)
  - Min stops: 2 stops (38 suburban/short routes); Max stops: 118 stops (Train 53041)
  - Mean stops: 16.74 stops; Median stops: 15.0 stops
- **Validation**: `python -m pytest -v` executed, 9/9 tests PASSED (100%).
- **Task Tracker**: Updated `documentation/task_tracker.csv` row 1.3 to `COMPLETED`.
- **Git Checkpoint**: Uncommitted (bundled into Checkpoint 1 upon completion of Tasks 1.1–1.4).

## Session 7: Task 1.4 — Trains with Maximum and Minimum Stops (Level 1)
- **Date / Timestamp**: 2026-09-14T03:07:00+05:30
- **Task ID**: 1.4 (Level 1)
- **Status**: COMPLETED
- **Implementation**: `src/level1/task_1_4_max_min_stops.py`
- **Output Artifact**: `outputs/tables/task_1_4_max_min_stops.csv`
- **Evidence Screenshot**: `screenshots/level1/task_1_4.png`
- **Documentation**: `documentation/level1/task_1_4.txt`
- **Test File**: `tests/test_level1.py`
- **Factual Results**:
  - Maximum stop count: 118 stops (Train 53041, Howrah to Jaynagar) — exactly 1 train tied.
  - Minimum stop count: 2 stops — exactly 1,249 trains tied (Gatimaan Express, Duronto non-stops, local shuttles).
  - Total rows in output: 1,250 (all ties cataloged without fabrication).
- **Validation**: `python -m pytest -v` executed, 10/10 tests PASSED (100%).
- **Task Tracker**: Updated `documentation/task_tracker.csv` row 1.4 to `COMPLETED`.
- **Phase Completion**: Checkpoint 1 (Dataset Audit + Level 1, Tasks 1.1–1.4) complete, tested, and validated.
