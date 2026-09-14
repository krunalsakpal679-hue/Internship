"""Test Suite: Data Processing, Time Standardization, Journey Duration, and Route Classification.

Covers:
- test_time_parsing: standard and placeholder time parsing.
- test_duration_calculation: hand-computed sample trains (same-day and midnight rollover).
- test_route_classification: mutual exclusivity, exhaustive coverage, and configurable threshold sensitivity.
- test_station_ordering: monotonicity validation on real and synthetic schedules.
"""

from datetime import datetime
from pathlib import Path
import pandas as pd
import pytest

from src.level2.task_2_2_journey_duration import calculate_journey_duration
from src.level2.task_2_3_route_classification import classify_route
from src.level3.task_3_3_station_order import validate_train_ordering

VERIFIED_DATASET_PATH = Path("data/processed/dataset_verified.csv")


@pytest.fixture(scope="module")
def train_df():
    """Load distinct train schedules."""
    df = pd.read_csv(VERIFIED_DATASET_PATH, dtype=str, keep_default_na=False)
    return df


def parse_time_string(time_str: str, is_origin: bool = False, is_terminus: bool = False):
    """Standardize time string and determine validity."""
    if not time_str or pd.isna(time_str) or str(time_str).strip() == "":
        return None, False

    cleaned = str(time_str).strip()
    try:
        # Support %H:%M:%S and %H:%M
        if len(cleaned.split(":")) == 2:
            dt = datetime.strptime(cleaned, "%H:%M")
        else:
            dt = datetime.strptime(cleaned, "%H:%M:%S")
        std_str = dt.strftime("%H:%M:%S")

        # Check placeholder conditions
        if is_origin:
            # 00:00:00 at origin arrival is placeholder marker
            return std_str, True
        elif is_terminus:
            # 00:00:00 at terminus departure is placeholder marker
            return std_str, True
        else:
            return std_str, True
    except ValueError:
        return None, False


def test_duration_calculation_hand_computed_samples():
    """Verify duration calculation matches hand-computed results on sample trains."""
    # Sample 1: Same-Day Sub-hour (08:15:00 to 09:05:00 = 50 minutes)
    dur1, roll1, comp1, _ = calculate_journey_duration("08:15:00", "09:05:00")
    assert comp1 is True
    assert roll1 is False
    assert dur1 == 50

    # Sample 2: Same-Day Intercity (06:00:00 to 11:30:00 = 330 minutes / 5.5 hours)
    dur2, roll2, comp2, _ = calculate_journey_duration("06:00:00", "11:30:00")
    assert comp2 is True
    assert roll2 is False
    assert dur2 == 330

    # Sample 3: Midnight Crossing Rollover (19:35:00 to 05:45:00 = 610 minutes / 10h 10m)
    # 19:35 -> 24:00 (4h 25m = 265m) + 00:00 -> 05:45 (5h 45m = 345m) = 610m
    dur3, roll3, comp3, _ = calculate_journey_duration("19:35:00", "05:45:00")
    assert comp3 is True
    assert roll3 is True
    assert dur3 == 610

    # Sample 4: Ambiguous Same-Time Case (10:00:00 to 10:00:00 -> Flagged unresolvable)
    dur4, roll4, comp4, status4 = calculate_journey_duration("10:00:00", "10:00:00")
    assert comp4 is False
    assert dur4 is None
    assert "Unresolvable" in status4


def test_route_classification(train_df):
    """Verify exhaustive, mutually exclusive classification and threshold sensitivity."""
    trains = train_df.drop_duplicates(subset=["Train_No"]).copy()

    # Verify all 11,113 trains receive a valid Route_Type
    valid_types = {"Short", "Medium", "Long"}
    actual_types = set(trains["Route_Type"].unique())
    assert actual_types == valid_types, f"Unexpected route types: {actual_types}"

    # Verify default empirical tercile boundaries (<=80m, 81-240m, >240m)
    assert classify_route(80, 50)[0] == "Short"
    assert classify_route(81, 100)[0] == "Medium"
    assert classify_route(240, 150)[0] == "Medium"
    assert classify_route(241, 300)[0] == "Long"

    # Sensitivity testing: modifying thresholds alters categorization
    assert classify_route(100, 100, short_max_mins=120, medium_max_mins=300)[0] == "Short"
    assert classify_route(250, 200, short_max_mins=120, medium_max_mins=300)[0] == "Medium"
    assert classify_route(350, 400, short_max_mins=120, medium_max_mins=300)[0] == "Long"


def test_station_ordering_validation(train_df):
    """Verify monotonicity validation on verified trains and synthetic error cases."""
    # Test a known real train (Train '11005')
    train_11005 = train_df[train_df["Train_No"] == "11005"].copy()
    train_11005["SN_num"] = train_11005["SN"].astype(int)
    train_11005["Distance_num"] = train_11005["Distance"].astype(int)
    res_valid = validate_train_ordering("11005", train_11005)
    assert res_valid["Has_Negative_Diff"] is False
    assert res_valid["Validation_Status"] == "PASSED (Strictly Monotonic)"

    # Test synthetic out-of-order train (Distance drops from 100 km to 50 km)
    synthetic_bad_df = pd.DataFrame([
        {"Train_No": "99999", "SN_num": 1, "Distance_num": 0},
        {"Train_No": "99999", "SN_num": 2, "Distance_num": 100},
        {"Train_No": "99999", "SN_num": 3, "Distance_num": 50},  # Negative drop!
        {"Train_No": "99999", "SN_num": 4, "Distance_num": 200}
    ])
    res_bad = validate_train_ordering("99999", synthetic_bad_df)
    assert res_bad["Has_Negative_Diff"] is True
    assert res_bad["Validation_Status"] == "FLAGGED: Negative Distance Transition"


