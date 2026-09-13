"""Tests for Level 1 Basic Data Review."""

from pathlib import Path
import pandas as pd

RAW_DATA_PATH = Path("data/raw/Dataset1.csv")
OUTPUT_1_1 = Path("outputs/tables/task_1_1_dataset_overview.csv")
SCREENSHOT_1_1 = Path("screenshots/level1/task_1_1.png")
DOCS_1_1 = Path("documentation/level1/task_1_1.txt")


def test_task_1_1_shape_and_columns():
    """Verify df.shape[0] > 0 and df.shape[1] == header column count."""
    with open(RAW_DATA_PATH, "r", encoding="utf-8") as f:
        header_cols = [c.strip(' "\n') for c in f.readline().split(",")]

    df = pd.read_csv(RAW_DATA_PATH, dtype=str)
    assert df.shape[0] > 0, "Dataset rows must be greater than 0"
    assert df.shape[0] == 186074, "Dataset must have exactly 186,074 rows"
    assert df.shape[1] == len(header_cols), "Column count must equal header count"
    assert df.columns.tolist() == header_cols, "Column names must exactly match header"


def test_task_1_1_output_artifacts():
    """Verify generated artifacts for task 1.1 exist and are non-empty."""
    assert OUTPUT_1_1.is_file(), "outputs/tables/task_1_1_dataset_overview.csv must exist"
    assert OUTPUT_1_1.stat().st_size > 0, "Overview CSV must not be empty"

    out_df = pd.read_csv(OUTPUT_1_1)
    assert "metric" in out_df.columns and "value" in out_df.columns, "Overview CSV must have metric, value columns"
    records_row = out_df[out_df["metric"] == "total_records"]
    assert len(records_row) == 1, "Must have total_records metric"
    assert int(records_row.iloc[0]["value"]) == 186074, "total_records must be 186,074"

    assert SCREENSHOT_1_1.is_file(), "screenshots/level1/task_1_1.png must exist"
    assert SCREENSHOT_1_1.stat().st_size > 1000, "Screenshot file too small"

    assert DOCS_1_1.is_file(), "documentation/level1/task_1_1.txt must exist"


def test_task_1_2_start_end_integrity():
    """Verify task 1.2 output table integrity, completeness, and spot checks."""
    output_1_2 = Path("outputs/tables/task_1_2_start_end_stations.csv")
    assert output_1_2.is_file(), "outputs/tables/task_1_2_start_end_stations.csv must exist"

    df = pd.read_csv(output_1_2, dtype=str)
    assert len(df) == 11113, f"Expected 11,113 trains, found {len(df)}"
    assert df["Start_Station_Code"].isna().sum() == 0, "Found null Start_Station_Code"
    assert df["Start_Station_Name"].isna().sum() == 0, "Found null Start_Station_Name"
    assert df["End_Station_Code"].isna().sum() == 0, "Found null End_Station_Code"
    assert df["End_Station_Name"].isna().sum() == 0, "Found null End_Station_Name"

    # Spot checks
    t107 = df[df["Train_No"] == "107"]
    assert len(t107) == 1
    assert t107.iloc[0]["Start_Station_Code"] == "SWV"
    assert t107.iloc[0]["End_Station_Code"] == "MAO"
    assert int(t107.iloc[0]["Total_Stations"]) == 4

    t12626 = df[df["Train_No"] == "12626"]
    assert len(t12626) == 1
    assert t12626.iloc[0]["Start_Station_Code"] == "NDLS"
    assert t12626.iloc[0]["End_Station_Code"] == "TVC"
    assert int(t12626.iloc[0]["Total_Stations"]) == 42

    assert Path("screenshots/level1/task_1_2.png").is_file()
    assert Path("documentation/level1/task_1_2.txt").is_file()


def test_task_1_3_stops_integrity():
    """Verify task 1.3 stop counts reconciliation and sum integrity."""
    output_1_3 = Path("outputs/tables/task_1_3_stops_per_train.csv")
    output_1_2 = Path("outputs/tables/task_1_2_start_end_stations.csv")
    assert output_1_3.is_file(), "outputs/tables/task_1_3_stops_per_train.csv must exist"

    df_stops = pd.read_csv(output_1_3, dtype={"Train_No": str, "Stop_Count": int})
    assert len(df_stops) == 11113, f"Expected 11,113 trains, got {len(df_stops)}"
    assert df_stops["Stop_Count"].sum() == 186074, "Sum of stops must equal 186,074"
    assert (df_stops["Stop_Count"] >= 2).all(), "All trains must have >= 2 stops"
    assert df_stops["Stop_Count"].max() == 118, "Max stops must be 118"
    assert df_stops["Stop_Count"].min() == 2, "Min stops must be 2"

    # Cross-reconcile with Task 1.2
    df_12 = pd.read_csv(output_1_2, dtype={"Train_No": str, "Total_Stations": int})
    merged = df_stops.merge(df_12, on="Train_No")
    assert len(merged) == 11113
    assert (merged["Stop_Count"] == merged["Total_Stations"]).all(), "Mismatch between Stop_Count and Total_Stations"

    assert Path("screenshots/level1/task_1_3.png").is_file()
    assert Path("documentation/level1/task_1_3.txt").is_file()


def test_task_1_4_max_min_stops():
    """Verify task 1.4 max and min stops identification, ties, and metadata."""
    output_1_4 = Path("outputs/tables/task_1_4_max_min_stops.csv")
    assert output_1_4.is_file(), "outputs/tables/task_1_4_max_min_stops.csv must exist"

    df = pd.read_csv(output_1_4, dtype={"Train_No": str, "Stop_Count": int})
    assert len(df) == 1250, f"Expected 1,250 extreme rows (1 max + 1,249 min), got {len(df)}"

    # Max stop assertions
    max_part = df[df["Category"] == "MAXIMUM_STOPS"]
    assert len(max_part) == 1, "Expected exactly 1 maximum stop train"
    assert max_part.iloc[0]["Train_No"] == "53041"
    assert max_part.iloc[0]["Stop_Count"] == 118
    assert max_part.iloc[0]["Start_Station_Code"] == "HWH"
    assert max_part.iloc[0]["End_Station_Code"] == "JYG"

    # Min stop assertions
    min_part = df[df["Category"] == "MINIMUM_STOPS"]
    assert len(min_part) == 1249, "Expected exactly 1,249 minimum stop trains"
    assert (min_part["Stop_Count"] == 2).all(), "All minimum stop trains must have exactly 2 stops"

    # Verify notable non-stop trains exist in min_part
    min_train_ids = set(min_part["Train_No"])
    assert "12049" in min_train_ids, "Gatimaan Express 12049 must be in min stops list"
    assert "12267" in min_train_ids, "Duronto Express 12267 must be in min stops list"

    assert Path("screenshots/level1/task_1_4.png").is_file()
    assert Path("documentation/level1/task_1_4.txt").is_file()
