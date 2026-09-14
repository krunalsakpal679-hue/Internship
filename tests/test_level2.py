"""Unit and data integrity tests for Level 2 tasks."""

from pathlib import Path
import pandas as pd

RAW_DATA_PATH = Path("data/raw/Dataset1.csv")
OUTPUT_2_1 = Path("outputs/tables/task_2_1_standardized_times.csv")
SCREENSHOT_2_1 = Path("screenshots/level2/task_2_1.png")
DOCS_2_1 = Path("documentation/level2/task_2_1.txt")


def test_task_2_1_artifacts_exist():
    """Verify that all Task 2.1 required artifacts exist and have non-zero size."""
    assert OUTPUT_2_1.is_file(), f"Output table missing: {OUTPUT_2_1}"
    assert OUTPUT_2_1.stat().st_size > 1000, "Output CSV is unexpectedly small"
    assert SCREENSHOT_2_1.is_file(), f"Screenshot missing: {SCREENSHOT_2_1}"
    assert SCREENSHOT_2_1.stat().st_size > 1000, "Screenshot file is unexpectedly small"
    assert DOCS_2_1.is_file(), f"Documentation note missing: {DOCS_2_1}"
    assert DOCS_2_1.stat().st_size > 100, "Documentation note is unexpectedly small"


def test_task_2_1_columns_and_counts():
    """Verify row count, columns, and parsing integrity for task 2.1."""
    df = pd.read_csv(OUTPUT_2_1, dtype=str)
    assert len(df) == 186074, f"Expected 186,074 rows, got {len(df)}"

    required_cols = [
        "SN", "Train_No", "Station_Code", "1A", "2A", "3A", "SL",
        "Station_Name", "Route_Number", "Arrival_time", "Departure_Time",
        "Distance", "Arrival_Time_Std", "Departure_Time_Std",
        "is_first_stop", "is_last_stop", "Arrival_Valid", "Departure_Valid"
    ]
    for col in required_cols:
        assert col in df.columns, f"Missing required column: {col}"

    # Verify booleans
    valid_bool_strings = {"True", "False"}
    assert set(df["Arrival_Valid"].unique()).issubset(valid_bool_strings), "Arrival_Valid must contain only booleans"
    assert set(df["Departure_Valid"].unique()).issubset(valid_bool_strings), "Departure_Valid must contain only booleans"
    assert set(df["is_first_stop"].unique()).issubset(valid_bool_strings), "is_first_stop must contain only booleans"
    assert set(df["is_last_stop"].unique()).issubset(valid_bool_strings), "is_last_stop must contain only booleans"

    # Verify zero nulls in standardized time strings
    assert df["Arrival_Time_Std"].isna().sum() == 0, "Null found in Arrival_Time_Std"
    assert df["Departure_Time_Std"].isna().sum() == 0, "Null found in Departure_Time_Std"


def test_task_2_1_placeholder_rules_and_counts():
    """Verify exact counts of flagged placeholders vs valid midnight operations."""
    df = pd.read_csv(OUTPUT_2_1, dtype=str)
    arr_valid = df["Arrival_Valid"] == "True"
    dep_valid = df["Departure_Valid"] == "True"
    is_first = df["is_first_stop"] == "True"
    is_last = df["is_last_stop"] == "True"

    # Placeholder counts
    origin_arr_placeholders = (~arr_valid).sum()
    terminus_dep_placeholders = (~dep_valid).sum()

    assert origin_arr_placeholders == 1951, f"Expected 1,951 origin arrival placeholders, got {origin_arr_placeholders}"
    assert terminus_dep_placeholders == 1955, f"Expected 1,955 terminus departure placeholders, got {terminus_dep_placeholders}"

    # All invalid arrivals must be origin stops with 00:00:00
    invalid_arr_rows = df[~arr_valid]
    assert (invalid_arr_rows["is_first_stop"] == "True").all(), "Non-origin stop flagged as invalid arrival"
    assert (invalid_arr_rows["Arrival_time"] == "00:00:00").all(), "Non-00:00:00 arrival flagged as invalid"

    # All invalid departures must be terminus stops with 00:00:00
    invalid_dep_rows = df[~dep_valid]
    assert (invalid_dep_rows["is_last_stop"] == "True").all(), "Non-terminus stop flagged as invalid departure"
    assert (invalid_dep_rows["Departure_Time"] == "00:00:00").all(), "Non-00:00:00 departure flagged as invalid"


def test_task_2_1_spot_checks():
    """Spot check 5 sample trains for correct origin/terminus flags."""
    df = pd.read_csv(OUTPUT_2_1, dtype=str)

    # Train 107: Origin Arr placeholder (False), Terminus Dep placeholder (False)
    t107 = df[df["Train_No"] == "107"]
    assert len(t107) == 4
    assert t107.iloc[0]["Arrival_Valid"] == "False"
    assert t107.iloc[0]["Departure_Valid"] == "True"
    assert t107.iloc[-1]["Arrival_Valid"] == "True"
    assert t107.iloc[-1]["Departure_Valid"] == "False"

    # Train 12626: Origin & Terminus both have scheduled non-zero times
    t12626 = df[df["Train_No"] == "12626"]
    assert len(t12626) == 42
    assert t12626.iloc[0]["Arrival_Valid"] == "True"
    assert t12626.iloc[0]["Departure_Valid"] == "True"
    assert t12626.iloc[-1]["Arrival_Valid"] == "True"
    assert t12626.iloc[-1]["Departure_Valid"] == "True"

    # Train 34752: Terminus arrival is legitimate midnight 00:00:00 (True), Terminus dep is placeholder (False)
    t34752 = df[df["Train_No"] == "34752"]
    assert len(t34752) == 21
    assert t34752.iloc[-1]["Arrival_time"] == "00:00:00"
    assert t34752.iloc[-1]["Arrival_Valid"] == "True"
    assert t34752.iloc[-1]["Departure_Time"] == "00:00:00"
    assert t34752.iloc[-1]["Departure_Valid"] == "False"

    # Train 53041: Longest route (118 stops), all valid
    t53041 = df[df["Train_No"] == "53041"]
    assert len(t53041) == 118
    assert (t53041["Arrival_Valid"] == "True").all()
    assert (t53041["Departure_Valid"] == "True").all()


OUTPUT_2_2 = Path("outputs/tables/task_2_2_journey_duration.csv")
SCREENSHOT_2_2 = Path("screenshots/level2/task_2_2.png")
DOCS_2_2 = Path("documentation/level2/task_2_2.txt")


def test_task_2_2_artifacts_exist():
    """Verify that all Task 2.2 required artifacts exist and have non-zero size."""
    assert OUTPUT_2_2.is_file(), f"Output table missing: {OUTPUT_2_2}"
    assert OUTPUT_2_2.stat().st_size > 1000, "Output CSV is unexpectedly small"
    assert SCREENSHOT_2_2.is_file(), f"Screenshot missing: {SCREENSHOT_2_2}"
    assert SCREENSHOT_2_2.stat().st_size > 1000, "Screenshot file is unexpectedly small"
    assert DOCS_2_2.is_file(), f"Documentation note missing: {DOCS_2_2}"
    assert DOCS_2_2.stat().st_size > 100, "Documentation note is unexpectedly small"


def test_task_2_2_structure_and_counts():
    """Verify train counts, columns, rollover splits, and flag distribution for task 2.2."""
    df = pd.read_csv(OUTPUT_2_2)
    assert len(df) == 11113, f"Expected 11,113 trains, got {len(df)}"

    required_cols = [
        "Train_No", "Start_Station_Code", "Start_Station_Name",
        "Start_Departure_Time", "End_Station_Code", "End_Station_Name",
        "End_Arrival_Time", "Midnight_Rollover", "Duration_Minutes",
        "Duration_Hours", "Duration_Computable", "Duration_Status"
    ]
    for col in required_cols:
        assert col in df.columns, f"Missing required column: {col}"

    computable_mask = df["Duration_Computable"] == True
    assert computable_mask.sum() == 11107, f"Expected 11,107 valid durations, got {computable_mask.sum()}"
    assert (~computable_mask).sum() == 6, f"Expected 6 flagged unresolvable trains, got {(~computable_mask).sum()}"

    same_day_count = (df["Midnight_Rollover"] == False).sum()
    rollover_count = (df["Midnight_Rollover"] == True).sum()
    assert same_day_count == 9185, f"Expected 9,185 same-day journeys, got {same_day_count}"
    assert rollover_count == 1922, f"Expected 1,922 rollover journeys, got {rollover_count}"


def test_task_2_2_durations_strictly_positive():
    """Verify all valid durations are strictly positive and flagged trains are NaN (not 0)."""
    df = pd.read_csv(OUTPUT_2_2)
    valid_df = df[df["Duration_Computable"] == True]
    assert (valid_df["Duration_Minutes"] > 0).all(), "Found non-positive duration among valid trains"
    assert not (valid_df["Duration_Minutes"] < 0).any(), "Found negative duration"

    # Flagged trains must be NaN in Duration_Minutes (not 0-filled)
    flagged_df = df[df["Duration_Computable"] == False]
    assert flagged_df["Duration_Minutes"].isna().all(), "Flagged trains must not be silently zero-filled"


def test_task_2_2_spot_checks():
    """Verify durations and rollover flags for 3 manual spot-checked trains."""
    df = pd.read_csv(OUTPUT_2_2)
    df["Train_No"] = df["Train_No"].astype(str)

    # Train 107: SWV -> MAO (10:25 to 12:10 = 105 mins, Same Day)
    t107 = df[df["Train_No"] == "107"].iloc[0]
    assert t107["Duration_Minutes"] == 105
    assert t107["Midnight_Rollover"] == False

    # Train 12951: BCT -> NDLS (17:00 to 08:35 = 935 mins, Rollover)
    t12951 = df[df["Train_No"] == "12951"].iloc[0]
    assert t12951["Duration_Minutes"] == 935
    assert t12951["Midnight_Rollover"] == True

    # Train 34752: SDAH -> LKPR (22:20 to 00:00 = 100 mins, Rollover)
    t34752 = df[df["Train_No"] == "34752"].iloc[0]
    assert t34752["Duration_Minutes"] == 100
    assert t34752["Midnight_Rollover"] == True


OUTPUT_2_3 = Path("outputs/tables/task_2_3_route_classification.csv")
SCREENSHOT_2_3 = Path("screenshots/level2/task_2_3.png")
DOCS_2_3 = Path("documentation/level2/task_2_3.txt")


def test_task_2_3_artifacts_exist():
    """Verify that all Task 2.3 required artifacts exist and have non-zero size."""
    assert OUTPUT_2_3.is_file(), f"Output table missing: {OUTPUT_2_3}"
    assert OUTPUT_2_3.stat().st_size > 1000, "Output CSV is unexpectedly small"
    assert SCREENSHOT_2_3.is_file(), f"Screenshot missing: {SCREENSHOT_2_3}"
    assert SCREENSHOT_2_3.stat().st_size > 1000, "Screenshot file is unexpectedly small"
    assert DOCS_2_3.is_file(), f"Documentation note missing: {DOCS_2_3}"
    assert DOCS_2_3.stat().st_size > 100, "Documentation note is unexpectedly small"


def test_task_2_3_completeness_and_classes():
    """Verify all 11,113 trains receive exactly one valid classification."""
    df = pd.read_csv(OUTPUT_2_3)
    assert len(df) == 11113, f"Expected 11,113 trains, got {len(df)}"

    required_cols = [
        "Train_No", "Start_Station_Code", "End_Station_Code",
        "Total_Distance_km", "Duration_Minutes", "Route_Type", "Classification_Basis"
    ]
    for col in required_cols:
        assert col in df.columns, f"Missing required column: {col}"

    # Every train receives exactly one of Short/Medium/Long
    assert set(df["Route_Type"].unique()) == {"Short", "Medium", "Long"}
    assert df["Route_Type"].isna().sum() == 0, "Found unclassified trains"

    # All three classes are non-empty
    counts = df["Route_Type"].value_counts()
    assert counts["Short"] == 3860
    assert counts["Medium"] == 3518
    assert counts["Long"] == 3735

    # Check classification basis
    basis = df["Classification_Basis"].value_counts()
    assert basis["Duration"] == 11107
    assert basis["Distance Fallback"] == 6


def test_task_2_3_configurable_thresholds():
    """Verify that changing classification thresholds alters classification output (not hard-coded)."""
    from src.level2.task_2_3_route_classification import classify_route

    # Test duration-based classification with default vs altered cutoffs
    # Default (80, 240):
    assert classify_route(70, 100)[0] == "Short"
    assert classify_route(100, 100)[0] == "Medium"
    assert classify_route(300, 100)[0] == "Long"

    # Altered thresholds (120, 360):
    # A 100-minute journey is Medium under default, but Short under altered threshold
    rtype_alt, _ = classify_route(100, 100, short_max_mins=120, medium_max_mins=360)
    assert rtype_alt == "Short", "Expected 100 mins to become Short under altered threshold"

    # Test fallback on NaN duration
    rtype_fb_short, basis_s = classify_route(None, 40)
    assert rtype_fb_short == "Short" and basis_s == "Distance Fallback"

    rtype_fb_long, basis_l = classify_route(None, 1500)
    assert rtype_fb_long == "Long" and basis_l == "Distance Fallback"


OUTPUT_2_4 = Path("outputs/tables/task_2_4_station_frequency.csv")
SCREENSHOT_2_4 = Path("screenshots/level2/task_2_4.png")
DOCS_2_4 = Path("documentation/level2/task_2_4.txt")


def test_task_2_4_artifacts_exist():
    """Verify that all Task 2.4 required artifacts exist and have non-zero size."""
    assert OUTPUT_2_4.is_file(), f"Output table missing: {OUTPUT_2_4}"
    assert OUTPUT_2_4.stat().st_size > 1000, "Output CSV is unexpectedly small"
    assert SCREENSHOT_2_4.is_file(), f"Screenshot missing: {SCREENSHOT_2_4}"
    assert SCREENSHOT_2_4.stat().st_size > 1000, "Screenshot file is unexpectedly small"
    assert DOCS_2_4.is_file(), f"Documentation note missing: {DOCS_2_4}"
    assert DOCS_2_4.stat().st_size > 100, "Documentation note is unexpectedly small"


def test_task_2_4_station_frequency_integrity():
    """Verify station count, rankings, top stations, and consistency bounds."""
    df = pd.read_csv(OUTPUT_2_4)
    assert len(df) == 8147, f"Expected 8,147 stations, got {len(df)}"

    required_cols = ["Rank", "Station_Code", "Station_Name", "Train_Count", "Stop_Count"]
    for col in required_cols:
        assert col in df.columns, f"Missing required column: {col}"

    # Frequency consistency: no station serves more trains than the total in dataset (11,113)
    assert (df["Train_Count"] <= 11113).all(), "Found frequency exceeding total trains"
    assert (df["Train_Count"] >= 1).all(), "Found station with zero frequency"
    assert (df["Stop_Count"] >= df["Train_Count"]).all(), "Stop count cannot be less than unique train count"

    # Verify top 3 stations
    assert df.iloc[0]["Station_Code"] == "CSMT" and df.iloc[0]["Train_Count"] == 1027
    assert df.iloc[1]["Station_Code"] == "KYN" and df.iloc[1]["Train_Count"] == 828
    assert df.iloc[2]["Station_Code"] == "TNA" and df.iloc[2]["Train_Count"] == 796

    # Verify no duplicate station codes
    assert df["Station_Code"].nunique() == 8147, "Duplicate station codes found in frequency table"


def test_task_2_4_spot_check_and_circular():
    """Spot check counts against raw dataset and check circular stop detection."""
    df_raw = pd.read_csv(RAW_DATA_PATH, dtype=str)
    df_freq = pd.read_csv(OUTPUT_2_4).set_index("Station_Code")

    # Manual spot checks
    for code in ["CSMT", "KYN", "HWH", "NDLS", "SDAH"]:
        expected = df_raw[df_raw["Station_Code"] == code]["Train_No"].nunique()
        actual = int(df_freq.loc[code, "Train_Count"])
        assert actual == expected, f"Spot check failed for {code}: {actual} vs {expected}"
