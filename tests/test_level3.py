"""Unit and data quality verification tests for Level 3 tasks."""

from pathlib import Path
import pandas as pd

RAW_DATA_PATH = Path("data/raw/Dataset1.csv")
OUTPUT_3_1 = Path("outputs/tables/task_3_1_missing_value_report.csv")
SCREENSHOT_3_1 = Path("screenshots/level3/task_3_1.png")
DOCS_3_1 = Path("documentation/level3/task_3_1.txt")


def test_task_3_1_artifacts_exist():
    """Verify that all Task 3.1 required artifacts exist and have non-zero size."""
    assert OUTPUT_3_1.is_file(), f"Output table missing: {OUTPUT_3_1}"
    assert OUTPUT_3_1.stat().st_size > 500, "Output CSV is unexpectedly small"
    assert SCREENSHOT_3_1.is_file(), f"Screenshot missing: {SCREENSHOT_3_1}"
    assert SCREENSHOT_3_1.stat().st_size > 1000, "Screenshot file is unexpectedly small"
    assert DOCS_3_1.is_file(), f"Documentation note missing: {DOCS_3_1}"
    assert DOCS_3_1.stat().st_size > 100, "Documentation note is unexpectedly small"


def test_task_3_1_report_completeness_and_zero_nulls():
    """Verify report structure, 12 columns, and zero genuine missing values."""
    df_rep = pd.read_csv(OUTPUT_3_1)
    assert len(df_rep) == 12, f"Expected 12 column audit records, got {len(df_rep)}"

    required_cols = [
        "Column_Name", "Raw_Data_Type", "Total_Rows", "Null_Count",
        "Null_Percentage", "Empty_String_Count", "Placeholder_Count",
        "Placeholder_Description", "Genuine_Gaps", "Handling_Action", "Justification"
    ]
    for col in required_cols:
        assert col in df_rep.columns, f"Missing report column: {col}"

    # Zero genuine nulls and zero empty strings
    assert df_rep["Null_Count"].sum() == 0, "Found non-zero null count in report"
    assert df_rep["Empty_String_Count"].sum() == 0, "Found non-zero empty string count in report"
    assert df_rep["Genuine_Gaps"].sum() == 0, "Found non-zero genuine gaps in report"


def test_task_3_1_placeholder_counts():
    """Verify exact placeholder counts for Arrival_time and Departure_Time."""
    df_rep = pd.read_csv(OUTPUT_3_1).set_index("Column_Name")

    arr_placeholders = int(df_rep.loc["Arrival_time", "Placeholder_Count"])
    dep_placeholders = int(df_rep.loc["Departure_Time", "Placeholder_Count"])

    assert arr_placeholders == 1951, f"Expected 1,951 origin arrival placeholders, got {arr_placeholders}"
    assert dep_placeholders == 1955, f"Expected 1,955 terminus departure placeholders, got {dep_placeholders}"


def test_task_3_1_no_silent_deletion_and_nanogaon_protection():
    """Verify no silent row deletion occurred and Station_Code NAN is safely preserved."""
    df_raw = pd.read_csv(RAW_DATA_PATH, dtype=str, keep_default_na=False)
    assert len(df_raw) == 186074, f"Dataset row count altered: {len(df_raw)}"

    # Station_Code 'NAN' represents Nanogaon Road, must not be coerced to NaN
    nan_rows = df_raw[df_raw["Station_Code"] == "NAN"]
    assert len(nan_rows) == 6, f"Expected 6 rows for Station_Code NAN, got {len(nan_rows)}"
    assert (nan_rows["Station_Name"] == "NANOGAON ROA").all(), "Station NAN name mismatch"


OUTPUT_3_2_REM = Path("outputs/tables/task_3_2_duplicates_removed.csv")
OUTPUT_3_2_REP = Path("outputs/tables/task_3_2_duplicates_report.csv")
DATASET_DEDUP = Path("data/processed/dataset_dedup.csv")
SCREENSHOT_3_2 = Path("screenshots/level3/task_3_2.png")
DOCS_3_2 = Path("documentation/level3/task_3_2.txt")


def test_task_3_2_artifacts_exist():
    """Verify that all Task 3.2 required artifacts exist and have non-zero size."""
    assert OUTPUT_3_2_REM.is_file(), f"Removed duplicates table missing: {OUTPUT_3_2_REM}"
    assert OUTPUT_3_2_REP.is_file(), f"Duplicates report missing: {OUTPUT_3_2_REP}"
    assert OUTPUT_3_2_REP.stat().st_size > 100, "Duplicates report is unexpectedly small"
    assert DATASET_DEDUP.is_file(), f"Deduplicated dataset missing: {DATASET_DEDUP}"
    assert DATASET_DEDUP.stat().st_size > 1000000, "Deduplicated dataset is unexpectedly small"
    assert SCREENSHOT_3_2.is_file(), f"Screenshot missing: {SCREENSHOT_3_2}"
    assert SCREENSHOT_3_2.stat().st_size > 1000, "Screenshot file is unexpectedly small"
    assert DOCS_3_2.is_file(), f"Documentation note missing: {DOCS_3_2}"
    assert DOCS_3_2.stat().st_size > 100, "Documentation note is unexpectedly small"


def test_task_3_2_deduplication_integrity():
    """Verify zero duplicate loss and row count matching."""
    df_raw = pd.read_csv(RAW_DATA_PATH, dtype=str)
    df_dedup = pd.read_csv(DATASET_DEDUP, dtype=str)

    assert len(df_dedup) == len(df_raw), "Deduplicated row count does not match raw row count"
    assert len(df_dedup) == 186074, f"Expected 186,074 rows, got {len(df_dedup)}"

    # Zero full row duplicates
    assert df_dedup.duplicated().sum() == 0, "Found full row duplicates in dataset_dedup.csv"

    # Zero schedule duplicates on candidate subset
    sched_dups = df_dedup.duplicated(
        subset=["Train_No", "Station_Code", "Arrival_time", "Departure_Time"]
    ).sum()
    assert sched_dups == 0, f"Found {sched_dups} schedule duplicates in dataset_dedup.csv"


def test_task_3_2_repeat_visits_preserved():
    """Verify that legitimate repeat visits (circular/loop routes) are preserved intact."""
    df_dedup = pd.read_csv(DATASET_DEDUP, dtype=str)

    # 60 rows across 20 trains must remain present
    repeat_rows = df_dedup[df_dedup.duplicated(subset=["Train_No", "Station_Code"], keep=False)]
    assert len(repeat_rows) == 60, f"Expected 60 repeat visit rows, got {len(repeat_rows)}"
    assert repeat_rows["Train_No"].nunique() == 20, f"Expected 20 repeat visit trains, got {repeat_rows['Train_No'].nunique()}"

    # Verify Darjeeling Joyride 52591 at DJ
    dj_stops = df_dedup[(df_dedup["Train_No"] == "52591") & (df_dedup["Station_Code"] == "DJ")]
    assert len(dj_stops) == 2, "Darjeeling Joyride DJ stops missing"
    assert dj_stops.iloc[0]["Arrival_time"] != dj_stops.iloc[1]["Arrival_time"]

    # Verify Delhi Ring Railway 64053 at CSB
    csb_stops = df_dedup[(df_dedup["Train_No"] == "64053") & (df_dedup["Station_Code"] == "CSB")]
    assert len(csb_stops) == 2, "Delhi Ring Railway CSB stops missing"


OUTPUT_3_3 = Path("outputs/tables/task_3_3_station_order_validation.csv")
OUTPUT_3_3_MIRROR = Path("outputs/tables/task_3_3_order_validation.csv")
SCREENSHOT_3_3 = Path("screenshots/level3/task_3_3.png")
DOCS_3_3 = Path("documentation/level3/task_3_3.txt")


def test_task_3_3_artifacts_exist():
    """Verify that all Task 3.3 required artifacts exist and have non-zero size."""
    assert OUTPUT_3_3.is_file(), f"Validation table missing: {OUTPUT_3_3}"
    assert OUTPUT_3_3.stat().st_size > 1000, "Validation table is unexpectedly small"
    assert OUTPUT_3_3_MIRROR.is_file(), f"Mirror validation table missing: {OUTPUT_3_3_MIRROR}"
    assert SCREENSHOT_3_3.is_file(), f"Screenshot missing: {SCREENSHOT_3_3}"
    assert SCREENSHOT_3_3.stat().st_size > 1000, "Screenshot file is unexpectedly small"
    assert DOCS_3_3.is_file(), f"Documentation note missing: {DOCS_3_3}"
    assert DOCS_3_3.stat().st_size > 100, "Documentation note is unexpectedly small"


def test_task_3_3_validation_integrity_and_bounds():
    """Verify all 11,113 trains are validated and zero negative diffs exist."""
    df_val = pd.read_csv(OUTPUT_3_3)
    assert len(df_val) == 11113, f"Expected 11,113 trains, got {len(df_val)}"

    required_cols = [
        "Train_No", "Total_Stops", "Total_Distance_km", "Has_Negative_Diff",
        "Negative_Diff_Count", "Has_Zero_Diff", "Zero_Diff_Count",
        "Has_Large_Jump", "Large_Jump_Count", "Validation_Status", "Flag_Reasons"
    ]
    for col in required_cols:
        assert col in df_val.columns, f"Missing required column: {col}"

    # Zero negative distance decreases in the entire dataset
    assert (df_val["Has_Negative_Diff"] == False).all(), "Found negative distance decrease in dataset"
    assert df_val["Negative_Diff_Count"].sum() == 0, "Non-zero negative diff count"

    # Category counts
    status_counts = df_val["Validation_Status"].value_counts()
    assert status_counts["PASSED (Strictly Monotonic)"] == 10845
    assert status_counts["FLAGGED: Repeated Distance (Integer Rounding)"] == 233
    assert status_counts["FLAGGED: Long Non-Stop Run"] == 35

    # Every flagged train has a reason
    flagged = df_val[df_val["Validation_Status"] != "PASSED (Strictly Monotonic)"]
    assert (flagged["Flag_Reasons"] != "").all()
    assert (flagged["Flag_Reasons"] != "None (Fully Monotonic)").all()


def test_station_ordering_known_and_synthetic():
    """Section 09 QA rule: known well-ordered train passes; synthetic out-of-order train is flagged."""
    from src.level3.task_3_3_station_order import validate_train_ordering

    # 1. Known well-ordered train: Train 107
    df_raw = pd.read_csv(DATASET_DEDUP, dtype=str)
    df_raw["SN_num"] = pd.to_numeric(df_raw["SN"], errors="coerce")
    df_raw["Distance_num"] = pd.to_numeric(df_raw["Distance"], errors="coerce")

    t107_stops = df_raw[df_raw["Train_No"] == "107"]
    result_107 = validate_train_ordering("107", t107_stops)
    assert result_107["Has_Negative_Diff"] == False
    assert result_107["Validation_Status"] == "PASSED (Strictly Monotonic)"

    # 2. Synthetic out-of-order train
    synthetic_stops = pd.DataFrame([
        {"Train_No": "99999", "SN_num": 1, "Distance_num": 0},
        {"Train_No": "99999", "SN_num": 2, "Distance_num": 100},
        {"Train_No": "99999", "SN_num": 3, "Distance_num": 50},  # Negative decrease!
        {"Train_No": "99999", "SN_num": 4, "Distance_num": 200},
    ])
    result_synth = validate_train_ordering("99999", synthetic_stops)
    assert result_synth["Has_Negative_Diff"] == True
    assert "Negative Distance Transition" in result_synth["Validation_Status"]
    assert "negative distance transition" in result_synth["Flag_Reasons"]


OUTPUT_3_4_VERIFIED = Path("data/processed/dataset_verified.csv")
OUTPUT_3_4_SUMMARY = Path("outputs/tables/task_3_4_data_quality_summary.csv")
SCREENSHOT_3_4 = Path("screenshots/level3/task_3_4.png")
DOCS_3_4 = Path("documentation/level3/task_3_4.txt")
EXPECTED_RAW_HASH = "8353639af562e88ceb8feb26454221d50fc97b38dc752e3fe6a7a0235f9ecd57"


def test_task_3_4_artifacts_exist():
    """Verify that all Task 3.4 required artifacts exist and have non-zero size."""
    assert OUTPUT_3_4_VERIFIED.is_file(), f"Verified dataset missing: {OUTPUT_3_4_VERIFIED}"
    assert OUTPUT_3_4_VERIFIED.stat().st_size > 10000000, "Verified dataset is unexpectedly small"
    assert OUTPUT_3_4_SUMMARY.is_file(), f"Quality summary missing: {OUTPUT_3_4_SUMMARY}"
    assert OUTPUT_3_4_SUMMARY.stat().st_size > 500, "Quality summary is unexpectedly small"
    assert SCREENSHOT_3_4.is_file(), f"Screenshot missing: {SCREENSHOT_3_4}"
    assert SCREENSHOT_3_4.stat().st_size > 1000, "Screenshot file is unexpectedly small"
    assert DOCS_3_4.is_file(), f"Documentation note missing: {DOCS_3_4}"
    assert DOCS_3_4.stat().st_size > 100, "Documentation note is unexpectedly small"


def test_task_3_4_verified_dataset_integrity():
    """Verify verified dataset row count, train count, columns, and data completeness."""
    df_ver = pd.read_csv(OUTPUT_3_4_VERIFIED, dtype=str, keep_default_na=False)

    # Exact row and train count matching
    assert len(df_ver) == 186074, f"Expected 186,074 rows, got {len(df_ver)}"
    assert df_ver["Train_No"].nunique() == 11113, f"Expected 11,113 trains, got {df_ver['Train_No'].nunique()}"
    assert df_ver["Station_Code"].nunique() == 8147, f"Expected 8,147 stations, got {df_ver['Station_Code'].nunique()}"

    # Required 21 columns present
    expected_cols = [
        "SN", "Train_No", "Station_Code", "1A", "2A", "3A", "SL", "Station_Name",
        "Route_Number", "Arrival_time", "Departure_Time", "Distance",
        "Arrival_Time_Std", "Departure_Time_Std", "Arrival_Valid", "Departure_Valid",
        "Duration_Minutes", "Duration_Hours", "Duration_Status", "Route_Type",
        "Order_Validation_Status"
    ]
    for col in expected_cols:
        assert col in df_ver.columns, f"Missing required column in verified dataset: {col}"

    # Zero empty strings in core columns
    core_cols = ["SN", "Train_No", "Station_Code", "Station_Name", "Route_Number",
                 "Arrival_time", "Departure_Time", "Distance", "Route_Type"]
    for col in core_cols:
        assert not (df_ver[col] == "").any(), f"Found empty string in column {col}"

    # Station Code NAN preservation
    nan_rows = df_ver[df_ver["Station_Code"] == "NAN"]
    assert len(nan_rows) == 6, f"Expected 6 rows for Station NAN, got {len(nan_rows)}"
    assert (nan_rows["Station_Name"] == "NANOGAON ROA").all(), "Station NAN name mismatch"

    # Route_Type distribution covers all three categories
    route_types = set(df_ver["Route_Type"].unique())
    assert route_types == {"Short", "Medium", "Long"}, f"Unexpected route types: {route_types}"


def test_task_3_4_raw_dataset_untouched():
    """Verify raw dataset checksum is 100% byte-for-byte identical to baseline."""
    import hashlib
    hasher = hashlib.sha256()
    with open(RAW_DATA_PATH, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            hasher.update(chunk)
    actual_hash = hasher.hexdigest()
    assert actual_hash == EXPECTED_RAW_HASH, f"Raw dataset altered! Expected {EXPECTED_RAW_HASH}, got {actual_hash}"


def test_task_3_4_data_quality_summary_reconciliation():
    """Verify data quality summary table stages and reconciliation totals."""
    df_sum = pd.read_csv(OUTPUT_3_4_SUMMARY)

    assert len(df_sum) == 5, f"Expected 5 summary stages, got {len(df_sum)}"
    assert list(df_sum["Stage_ID"]) == [
        "Level 3 Baseline", "Task 3.1", "Task 3.2", "Task 3.3", "Task 3.4"
    ]

    # Zero rows removed across the entire data quality pipeline
    assert df_sum["Removed_Count"].sum() == 0, "Found non-zero removed count in summary"

    # Final retained count is 186,074 across all stages
    assert (df_sum["Final_Count"] == 186074).all(), "Final count mismatch in summary table"
    assert (df_sum["Quality_Status"].isin(["PASSED", "VERIFIED"])).all(), "Found failed status in summary"

