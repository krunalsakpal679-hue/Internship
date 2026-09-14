"""Unit and data quality verification tests for Level 4 tasks."""

from pathlib import Path
import pandas as pd
import pytest

VERIFIED_DATA_PATH = Path("data/processed/dataset_verified.csv")
OUTPUT_4_1 = Path("outputs/tables/task_4_1_duration_by_route_type.csv")
OUTPUT_4_1_MIRROR = Path("outputs/tables/task_4_1_duration_comparison.csv")
SCREENSHOT_4_1 = Path("screenshots/level4/task_4_1.png")
DOCS_4_1 = Path("documentation/level4/task_4_1.txt")


def test_task_4_1_artifacts_exist():
    """Verify that all Task 4.1 required artifacts exist and have non-zero size."""
    assert OUTPUT_4_1.is_file(), f"Output table missing: {OUTPUT_4_1}"
    assert OUTPUT_4_1.stat().st_size > 200, "Output CSV is unexpectedly small"
    assert OUTPUT_4_1_MIRROR.is_file(), f"Mirror table missing: {OUTPUT_4_1_MIRROR}"
    assert OUTPUT_4_1_MIRROR.stat().st_size > 200, "Mirror CSV is unexpectedly small"
    assert SCREENSHOT_4_1.is_file(), f"Screenshot missing: {SCREENSHOT_4_1}"
    assert SCREENSHOT_4_1.stat().st_size > 1000, "Screenshot file is unexpectedly small"
    assert DOCS_4_1.is_file(), f"Documentation note missing: {DOCS_4_1}"
    assert DOCS_4_1.stat().st_size > 100, "Documentation note is unexpectedly small"


def test_task_4_1_route_types_present_and_reconciled():
    """Assert all 3 route types and network total are present and reconcile with train counts."""
    df_comp = pd.read_csv(OUTPUT_4_1)

    required_cols = [
        "Route_Type", "Total_Trains", "Computable_Trains", "Excluded_Trains",
        "Mean_Duration_Minutes", "Median_Duration_Minutes", "Std_Duration_Minutes",
        "Min_Duration_Minutes", "Max_Duration_Minutes", "Mean_Duration_Hours",
        "Median_Duration_Hours", "Sample_Assessment"
    ]
    for col in required_cols:
        assert col in df_comp.columns, f"Missing required column: {col}"

    route_types = list(df_comp["Route_Type"])
    assert "Short" in route_types, "Short route type missing"
    assert "Medium" in route_types, "Medium route type missing"
    assert "Long" in route_types, "Long route type missing"
    assert "Overall (All Routes)" in route_types, "Overall summary row missing"

    df_indexed = df_comp.set_index("Route_Type")

    # Train counts per tier
    assert df_indexed.loc["Short", "Total_Trains"] == 3860
    assert df_indexed.loc["Medium", "Total_Trains"] == 3518
    assert df_indexed.loc["Long", "Total_Trains"] == 3735
    assert df_indexed.loc["Overall (All Routes)", "Total_Trains"] == 11113

    # Computable counts
    assert df_indexed.loc["Short", "Computable_Trains"] == 3860
    assert df_indexed.loc["Medium", "Computable_Trains"] == 3518
    assert df_indexed.loc["Long", "Computable_Trains"] == 3729
    assert df_indexed.loc["Overall (All Routes)", "Computable_Trains"] == 11107

    # Excluded counts
    assert df_indexed.loc["Short", "Excluded_Trains"] == 0
    assert df_indexed.loc["Medium", "Excluded_Trains"] == 0
    assert df_indexed.loc["Long", "Excluded_Trains"] == 6
    assert df_indexed.loc["Overall (All Routes)", "Excluded_Trains"] == 6


def test_task_4_1_durations_bounds_and_hierarchy():
    """Verify strictly increasing duration hierarchy and valid duration bounds."""
    df_comp = pd.read_csv(OUTPUT_4_1).set_index("Route_Type")

    short_mean = df_indexed_mean = df_comp.loc["Short", "Mean_Duration_Minutes"]
    med_mean = df_comp.loc["Medium", "Mean_Duration_Minutes"]
    long_mean = df_comp.loc["Long", "Mean_Duration_Minutes"]

    short_med = df_comp.loc["Short", "Median_Duration_Minutes"]
    med_med = df_comp.loc["Medium", "Median_Duration_Minutes"]
    long_med = df_comp.loc["Long", "Median_Duration_Minutes"]

    # Mean hierarchy: Short < Medium < Long
    assert short_mean < med_mean < long_mean, f"Mean hierarchy violated: {short_mean} < {med_mean} < {long_mean}"

    # Median hierarchy: Short < Medium < Long
    assert short_med < med_med < long_med, f"Median hierarchy violated: {short_med} < {med_med} < {long_med}"

    # Expected exact rounded metrics
    assert round(short_mean, 2) == 49.50
    assert round(med_mean, 2) == 142.02
    assert round(long_mean, 2) == 637.34

    assert round(short_med, 2) == 52.00
    assert round(med_med, 2) == 135.00
    assert round(long_med, 2) == 555.00

    # Bounds
    assert df_comp.loc["Short", "Min_Duration_Minutes"] >= 5.0
    assert df_comp.loc["Short", "Max_Duration_Minutes"] <= 80.0
    assert df_comp.loc["Medium", "Min_Duration_Minutes"] >= 81.0
    assert df_comp.loc["Medium", "Max_Duration_Minutes"] <= 240.0
    assert df_comp.loc["Long", "Min_Duration_Minutes"] >= 241.0
    assert df_comp.loc["Long", "Max_Duration_Minutes"] <= 1440.0


def test_task_4_1_spot_checks():
    """Spot-check individual trains from verified dataset against computed metrics."""
    df_ver = pd.read_csv(VERIFIED_DATA_PATH, dtype=str, keep_default_na=False)

    # Train 107
    t107 = df_ver[df_ver["Train_No"] == "107"].iloc[0]
    assert t107["Route_Type"] == "Medium"
    assert float(t107["Duration_Minutes"]) == 105.0

    # Train 12424
    t12424 = df_ver[df_ver["Train_No"] == "12424"].iloc[0]
    assert t12424["Route_Type"] == "Long"
    assert float(t12424["Duration_Minutes"]) == 950.0


OUTPUT_4_2 = Path("outputs/tables/task_4_2_high_traffic_stations.csv")
STATION_FREQ_2_4 = Path("outputs/tables/task_2_4_station_frequency.csv")
SCREENSHOT_4_2 = Path("screenshots/level4/task_4_2.png")
DOCS_4_2 = Path("documentation/level4/task_4_2.txt")


def test_task_4_2_artifacts_exist():
    """Verify that all Task 4.2 required artifacts exist and have non-zero size."""
    assert OUTPUT_4_2.is_file(), f"Output table missing: {OUTPUT_4_2}"
    assert OUTPUT_4_2.stat().st_size > 5000, "High traffic CSV is unexpectedly small"
    assert SCREENSHOT_4_2.is_file(), f"Screenshot missing: {SCREENSHOT_4_2}"
    assert SCREENSHOT_4_2.stat().st_size > 1000, "Screenshot file is unexpectedly small"
    assert DOCS_4_2.is_file(), f"Documentation note missing: {DOCS_4_2}"
    assert DOCS_4_2.stat().st_size > 100, "Documentation note is unexpectedly small"


def test_task_4_2_high_traffic_integrity_and_existence():
    """Verify high-traffic stations list is non-empty, non-total, and exists in base table."""
    df_ht = pd.read_csv(OUTPUT_4_2)
    df_freq = pd.read_csv(STATION_FREQ_2_4)

    # 1. Non-empty, non-total list (830 stations = 10.19% of network)
    assert len(df_ht) == 830, f"Expected 830 high-traffic stations, got {len(df_ht)}"
    assert 0 < len(df_ht) < len(df_freq), "High-traffic list is either empty or equals total stations"

    # 2. Assert every reported high-traffic station exists in station frequency table
    base_station_codes = set(df_freq["Station_Code"])
    ht_station_codes = set(df_ht["Station_Code"])
    missing = ht_station_codes - base_station_codes
    assert len(missing) == 0, f"Found stations in high-traffic list not in base table: {missing}"

    # 3. Minimum train count in high traffic list is at least 48 (90th percentile)
    assert df_ht["Train_Count"].min() >= 48, f"Found station below 90th percentile cutoff: {df_ht['Train_Count'].min()}"

    # 4. Top 3 stations
    assert df_ht.iloc[0]["Station_Code"] == "CSMT"
    assert df_ht.iloc[0]["Train_Count"] == 1027
    assert df_ht.iloc[1]["Station_Code"] == "KYN"
    assert df_ht.iloc[1]["Train_Count"] == 828
    assert df_ht.iloc[2]["Station_Code"] == "TNA"
    assert df_ht.iloc[2]["Train_Count"] == 796


def test_task_4_2_tier_distribution():
    """Verify tier assignments and counts within high-traffic table."""
    df_ht = pd.read_csv(OUTPUT_4_2)
    tier_counts = df_ht["Traffic_Tier"].value_counts()

    assert tier_counts["Tier 1: Mega Hub (Top 1%)"] == 83
    assert tier_counts["Tier 2: Major Hub (Top 5%)"] == 328
    assert tier_counts["Tier 3: Regional Hub (Top 10%)"] == 419

    # Tier train count boundaries
    t1_min = df_ht[df_ht["Traffic_Tier"] == "Tier 1: Mega Hub (Top 1%)"]["Train_Count"].min()
    t2_min = df_ht[df_ht["Traffic_Tier"] == "Tier 2: Major Hub (Top 5%)"]["Train_Count"].min()
    t3_min = df_ht[df_ht["Traffic_Tier"] == "Tier 3: Regional Hub (Top 10%)"]["Train_Count"].min()

    assert t1_min >= 233
    assert t2_min >= 91
    assert t3_min >= 48


CHART_4_3_DUR = Path("outputs/charts/task_4_3_duration_by_route_type.png")
CHART_4_3_DUR_MIRROR = Path("outputs/charts/task_4_3_duration_by_route.png")
CHART_4_3_HT = Path("outputs/charts/task_4_3_high_traffic_stations.png")
CHART_4_3_HIST = Path("outputs/charts/task_4_3_duration_histogram.png")
SCREENSHOT_4_3 = Path("screenshots/level4/task_4_3.png")
DOCS_4_3 = Path("documentation/level4/task_4_3.txt")


def test_task_4_3_artifacts_exist():
    """Verify that all Task 4.3 required chart artifacts exist and have non-zero size."""
    assert CHART_4_3_DUR.is_file(), f"Duration chart missing: {CHART_4_3_DUR}"
    assert CHART_4_3_DUR.stat().st_size > 10000, "Duration chart is unexpectedly small"

    assert CHART_4_3_DUR_MIRROR.is_file(), f"Mirror duration chart missing: {CHART_4_3_DUR_MIRROR}"
    assert CHART_4_3_DUR_MIRROR.stat().st_size > 10000, "Mirror duration chart is unexpectedly small"

    assert CHART_4_3_HT.is_file(), f"High traffic chart missing: {CHART_4_3_HT}"
    assert CHART_4_3_HT.stat().st_size > 10000, "High traffic chart is unexpectedly small"

    assert CHART_4_3_HIST.is_file(), f"Histogram chart missing: {CHART_4_3_HIST}"
    assert CHART_4_3_HIST.stat().st_size > 10000, "Histogram chart is unexpectedly small"

    assert SCREENSHOT_4_3.is_file(), f"Screenshot missing: {SCREENSHOT_4_3}"
    assert SCREENSHOT_4_3.stat().st_size > 1000, "Screenshot file is unexpectedly small"

    assert DOCS_4_3.is_file(), f"Documentation note missing: {DOCS_4_3}"
    assert DOCS_4_3.stat().st_size > 100, "Documentation note is unexpectedly small"


SUMMARY_4_4_MD = Path("documentation/level4/task_4_4_key_observations.md")
SUMMARY_4_4_MIRROR = Path("documentation/level4/task_4_4_summary.md")
SCREENSHOT_4_4 = Path("screenshots/level4/task_4_4.png")
DOCS_4_4 = Path("documentation/level4/task_4_4.txt")


def test_task_4_4_artifacts_exist():
    """Verify that all Task 4.4 required report artifacts exist and have non-zero size."""
    assert SUMMARY_4_4_MD.is_file(), f"Summary markdown missing: {SUMMARY_4_4_MD}"
    assert SUMMARY_4_4_MD.stat().st_size > 1000, "Summary markdown is unexpectedly small"

    assert SUMMARY_4_4_MIRROR.is_file(), f"Mirror summary markdown missing: {SUMMARY_4_4_MIRROR}"
    assert SUMMARY_4_4_MIRROR.stat().st_size > 1000, "Mirror summary markdown is unexpectedly small"

    assert SCREENSHOT_4_4.is_file(), f"Screenshot missing: {SCREENSHOT_4_4}"
    assert SCREENSHOT_4_4.stat().st_size > 1000, "Screenshot file is unexpectedly small"

    assert DOCS_4_4.is_file(), f"Documentation note missing: {DOCS_4_4}"
    assert DOCS_4_4.stat().st_size > 100, "Documentation note is unexpectedly small"


def test_task_4_4_summary_content_and_citations():
    """Verify summary markdown contains required sections, citations, and classification tags."""
    content = SUMMARY_4_4_MD.read_text(encoding="utf-8")

    # Check for distinctions
    assert "[DATA FACT]" in content, "Missing [DATA FACT] tag in summary"
    assert "[INTERPRETATION]" in content, "Missing [INTERPRETATION] tag in summary"
    assert "[METHODOLOGY" in content, "Missing [METHODOLOGY] tag in summary"

    # Check for specific cited numbers
    assert "49.50" in content, "Short route duration figure not cited"
    assert "142.02" in content, "Medium route duration figure not cited"
    assert "637.34" in content, "Long route duration figure not cited"
    assert "1,027" in content or "1027" in content, "CSMT train count not cited"
    assert "830" in content, "High-traffic count not cited"
    assert "8,147" in content or "8147" in content, "Total stations count not cited"



