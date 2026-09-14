"""Test Suite: Dataset Loading, Integrity, and Cleaning Verification.

Covers:
- test_dataset_loading: raw & verified datasets load, expected schema present, row counts match.
- test_data_cleaning: zero unresolved nulls in schedule fields, raw file integrity (SHA-256 match).
"""

import hashlib
from pathlib import Path
import pandas as pd
import pytest

RAW_DATASET_PATH = Path("data/raw/Dataset1.csv")
VERIFIED_DATASET_PATH = Path("data/processed/dataset_verified.csv")

EXPECTED_RAW_SHA256 = "8353639af562e88ceb8feb26454221d50fc97b38dc752e3fe6a7a0235f9ecd57"

RAW_COLUMNS = [
    "SN", "Train_No", "Station_Code", "1A", "2A", "3A", "SL",
    "Station_Name", "Route_Number", "Arrival_time", "Departure_Time", "Distance"
]

VERIFIED_COLUMNS = [
    "SN", "Train_No", "Station_Code", "1A", "2A", "3A", "SL",
    "Station_Name", "Route_Number", "Arrival_time", "Departure_Time", "Distance",
    "Arrival_Time_Std", "Departure_Time_Std", "Arrival_Valid", "Departure_Valid",
    "Duration_Minutes", "Duration_Hours", "Duration_Status", "Route_Type", "Order_Validation_Status"
]


@pytest.fixture(scope="module")
def raw_df():
    """Load raw dataset."""
    assert RAW_DATASET_PATH.is_file(), f"Raw dataset not found at {RAW_DATASET_PATH}"
    return pd.read_csv(RAW_DATASET_PATH, dtype=str, keep_default_na=False)


@pytest.fixture(scope="module")
def verified_df():
    """Load processed verified dataset."""
    assert VERIFIED_DATASET_PATH.is_file(), f"Verified dataset not found at {VERIFIED_DATASET_PATH}"
    return pd.read_csv(VERIFIED_DATASET_PATH, dtype=str, keep_default_na=False)


def test_dataset_loading(raw_df, verified_df):
    """Verify raw and verified datasets load with exact row counts and column definitions."""
    # Raw dataset shape & columns
    assert len(raw_df) == 186074, f"Expected 186,074 raw rows, got {len(raw_df)}"
    assert list(raw_df.columns) == RAW_COLUMNS, f"Raw column mismatch: {list(raw_df.columns)}"

    # Verified dataset shape & columns
    assert len(verified_df) == 186074, f"Expected 186,074 verified rows, got {len(verified_df)}"
    assert list(verified_df.columns) == VERIFIED_COLUMNS, f"Verified column mismatch: {list(verified_df.columns)}"


def test_data_cleaning_no_nulls(verified_df):
    """Verify cleaned dataset contains zero unresolved nulls or empty strings in schedule fields."""
    critical_cols = [
        "SN", "Train_No", "Station_Code", "Station_Name", "Route_Number",
        "Arrival_Time_Std", "Departure_Time_Std", "Distance", "Route_Type", "Order_Validation_Status"
    ]
    for col in critical_cols:
        empty_count = (verified_df[col] == "").sum()
        null_count = verified_df[col].isna().sum()
        assert empty_count == 0, f"Found {empty_count} empty strings in column {col}"
        assert null_count == 0, f"Found {null_count} nulls in column {col}"


def test_raw_file_untouched_checksum():
    """Verify data/raw/Dataset1.csv has not been modified using SHA-256 integrity check."""
    hasher = hashlib.sha256()
    with open(RAW_DATASET_PATH, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    actual_hash = hasher.hexdigest()
    assert actual_hash == EXPECTED_RAW_SHA256, f"Raw dataset SHA-256 changed! Expected {EXPECTED_RAW_SHA256}, got {actual_hash}"


def test_nanogaon_protection(verified_df):
    """Verify station code 'NAN' (Nanogaon Road) was protected and not parsed as NaN."""
    nan_rows = verified_df[verified_df["Station_Code"] == "NAN"]
    assert len(nan_rows) == 6, f"Expected 6 rows for station code 'NAN', found {len(nan_rows)}"
    assert (nan_rows["Station_Name"] == "NANOGAON ROA").all()
