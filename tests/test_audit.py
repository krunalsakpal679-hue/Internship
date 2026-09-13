"""Automated test suite for dataset audit verification."""

from pathlib import Path
import pandas as pd

REPORT_PATH = Path("outputs/reports/dataset_audit_report.md")
SCREENSHOT_PATH = Path("screenshots/level1/dataset_audit.png")
DOCS_PATH = Path("documentation/level1/dataset_audit.txt")
DATA_PATH = Path("data/raw/Dataset1.csv")

def test_audit_artifacts_exist():
    assert REPORT_PATH.is_file(), "Audit report markdown missing"
    assert REPORT_PATH.stat().st_size > 1000, "Audit report markdown is too short"
    assert SCREENSHOT_PATH.is_file(), "Audit screenshot visual missing"
    assert SCREENSHOT_PATH.stat().st_size > 10000, "Audit screenshot is too small"
    assert DOCS_PATH.is_file(), "Audit documentation missing"

def test_dataset_completeness():
    df = pd.read_csv(DATA_PATH, dtype=str)
    assert df.shape == (186074, 12), f"Unexpected shape {df.shape}"
    assert df.isna().sum().sum() == 0, "Null values found in raw dataset"
    assert df["Train_No"].nunique() == 11113, "Unexpected unique train count"
    assert df["Station_Code"].nunique() == 8147, "Unexpected unique station code count"
