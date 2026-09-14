# Test Suite Summary & Quality Assurance Report

**Project**: Train Schedule Analysis and Interactive Route Enquiry System Using Python  
**Organization**: Sysslan IT Solutions Internship  
**Phase**: Checkpoint 6 — Full Testing Suite  
**Test Runner**: Pytest 9.0.2 on Python 3.14.3 (Windows)  
**Total Test Modules**: 11 test modules  
**Total Tests Executed**: **83 passed / 83 total (100% PASS)**  
**Raw Test Report**: [`outputs/reports/test_results.txt`](file:///c:/Internship/outputs/reports/test_results.txt)  
**Evidence Screenshot**: [`screenshots/testing/checkpoint_6.png`](file:///c:/Internship/screenshots/testing/checkpoint_6.png)  

---

## 1. Test Architecture & Modular Coverage

The project implements a multi-layered automated test architecture validating data integrity, processing algorithms, analytical tables, visual charts, and interactive user enquiry systems:

| Test Module | Test Focus & Scope | Tests Passed | Status |
| :--- | :--- | :---: | :---: |
| [`tests/test_foundation.py`](file:///c:/Internship/tests/test_foundation.py) | Directory structure, raw dataset presence, task tracker & session logs | 3 / 3 | **100% PASS** |
| [`tests/test_audit.py`](file:///c:/Internship/tests/test_audit.py) | Raw dataset completeness, schema verification, audit trail artifacts | 2 / 2 | **100% PASS** |
| [`tests/test_dataset.py`](file:///c:/Internship/tests/test_dataset.py) | Raw/verified schema integrity, SHA-256 raw file immutability, zero-null invariant, Nanogaon protection | 4 / 4 | **100% PASS** |
| [`tests/test_processing.py`](file:///c:/Internship/tests/test_processing.py) | Time parsing, midnight rollover duration calculation, route classification, station monotonicity | 4 / 4 | **100% PASS** |
| [`tests/test_analysis.py`](file:///c:/Internship/tests/test_analysis.py) | Station frequency integrity, pivot table reconciliation, cross-tab reconciliation, chart artifacts | 3 / 3 | **100% PASS** |
| [`tests/test_enquiry_system.py`](file:///c:/Internship/tests/test_enquiry_system.py) | Direct route enquiry queries, disconnected pairs, invalid stations, same-station rejection, normalization | 6 / 6 | **100% PASS** |
| [`tests/test_level1.py`](file:///c:/Internship/tests/test_level1.py) | Level 1 dataset overview, start/end station detection, stops per train, max/min stops | 5 / 5 | **100% PASS** |
| [`tests/test_level2.py`](file:///c:/Internship/tests/test_level2.py) | Level 2 standardized times, journey durations, empirical route classification, station frequencies | 14 / 14 | **100% PASS** |
| [`tests/test_level3.py`](file:///c:/Internship/tests/test_level3.py) | Level 3 missing values, deduplication integrity, station order monotonicity, verified dataset save | 14 / 14 | **100% PASS** |
| [`tests/test_level4.py`](file:///c:/Internship/tests/test_level4.py) | Level 4 duration comparisons, high-traffic hubs (top-decile tiers), visualizations, insights summary | 10 / 10 | **100% PASS** |
| [`tests/test_level5.py`](file:///c:/Internship/tests/test_level5.py) | Level 5 pivot tables, structural cross-tabs, heatmap/bar visualizations, advanced insights | 9 / 9 | **100% PASS** |
| [`tests/test_train_enquiry.py`](file:///c:/Internship/tests/test_train_enquiry.py) | Level 6 CLI application fixtures, duration helpers, and 5 mandatory validation scenarios | 9 / 9 | **100% PASS** |
| **TOTAL** | **Comprehensive Full Pipeline Coverage** | **83 / 83** | **100% PASS** |

---

## 2. Core Invariants Verified by Test Suite

1. **Zero Raw Modification & Immutability**:
   * Verified that `data/raw/Dataset1.csv` matches SHA-256 hash `8353639af562e88ceb8feb26454221d50fc97b38dc752e3fe6a7a0235f9ecd57` with 0 byte alterations.
2. **Deterministic Data Reconciliation**:
   * All 8,147 station row totals in pivot table (`outputs/tables/task_5_1_station_pivot.csv`) reconcile 100% with Task 2.4 frequencies (`Train_Count`).
   * Structural cross-tabulation sums match 11,113 unique trains (Short: 3,860, Medium: 3,518, Long: 3,735) with 0 discrepancies.
3. **Midnight Rollover Mathematical Correctness**:
   * Verified same-day sub-hour (50m), same-day intercity (330m), and midnight crossing (19:35 to 05:45 = 610m) durations against hand-computed ground truth.
4. **Suburban & Commuter Protection**:
   * Preserved all 60 legitimate repeat visits across 20 circular/loop routes.
   * Protected station code `'NAN'` (Nanogaon Road) from erroneous NaN coercion.
5. **Interactive Enquiry Rigor**:
   * Strict direct train enforcement ($	ext{Source SN} < 	ext{Destination SN}$).
   * Sub-5ms query performance via inverted index.
   * Graceful, user-friendly error messages on invalid stations and disconnected city pairs.

---

## 3. Negative Testing & Mutation Verification

* **Mutation Test Protocol**: Intentionally injected logic mutations into route classification logic (`classify_route`) and verified that the test runner immediately failed with actionable tracebacks.
* **Restoration**: Restored verified logic and confirmed clean 100% pass across all 83 test assertions.
