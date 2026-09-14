"""Unit and data quality verification tests for Level 5 tasks."""

from pathlib import Path
import pandas as pd
import pytest

OUTPUT_5_1 = Path("outputs/tables/task_5_1_station_pivot.csv")
STATION_FREQ_2_4 = Path("outputs/tables/task_2_4_station_frequency.csv")
SCREENSHOT_5_1 = Path("screenshots/level5/task_5_1.png")
DOCS_5_1 = Path("documentation/level5/task_5_1.txt")


def test_task_5_1_artifacts_exist():
    """Verify that all Task 5.1 required artifacts exist and have non-zero size."""
    assert OUTPUT_5_1.is_file(), f"Pivot table missing: {OUTPUT_5_1}"
    assert OUTPUT_5_1.stat().st_size > 50000, "Pivot table CSV is unexpectedly small"
    assert SCREENSHOT_5_1.is_file(), f"Screenshot missing: {SCREENSHOT_5_1}"
    assert SCREENSHOT_5_1.stat().st_size > 1000, "Screenshot file is unexpectedly small"
    assert DOCS_5_1.is_file(), f"Documentation note missing: {DOCS_5_1}"
    assert DOCS_5_1.stat().st_size > 100, "Documentation note is unexpectedly small"


def test_task_5_1_pivot_reconciliation_with_task_2_4():
    """Verify all 8,147 station row totals reconcile exactly with Task 2.4 frequencies."""
    df_pivot = pd.read_csv(OUTPUT_5_1)
    df_freq = pd.read_csv(STATION_FREQ_2_4)

    assert len(df_pivot) == 8147, f"Expected 8,147 stations in pivot table, got {len(df_pivot)}"

    required_cols = [
        "Station_Code", "Station_Name", "Short", "Medium", "Long",
        "Total_Distinct_Trains", "Pct_Short", "Pct_Medium", "Pct_Long"
    ]
    for col in required_cols:
        assert col in df_pivot.columns, f"Missing column in pivot table: {col}"

    # Internal consistency: Total == Short + Medium + Long
    assert (df_pivot["Total_Distinct_Trains"] == df_pivot["Short"] + df_pivot["Medium"] + df_pivot["Long"]).all(), \
        "Internal sum mismatch in pivot table"

    # External reconciliation with Task 2.4
    merged = pd.merge(df_pivot, df_freq, on="Station_Code")
    assert len(merged) == 8147, "Merge with Task 2.4 dropped stations"
    diffs = (merged["Total_Distinct_Trains"] != merged["Train_Count"]).sum()
    assert diffs == 0, f"Found {diffs} mismatches with Task 2.4 train frequencies"


def test_task_5_1_spot_checks():
    """Spot-check individual key hub stations in pivot table."""
    df_pivot = pd.read_csv(OUTPUT_5_1).set_index("Station_Code")

    # CSMT (Short route leader)
    csmt = df_pivot.loc["CSMT"]
    assert csmt["Short"] == 804
    assert csmt["Medium"] == 138
    assert csmt["Long"] == 85
    assert csmt["Total_Distinct_Trains"] == 1027

    # BZA (Long route leader)
    bza = df_pivot.loc["BZA"]
    assert bza["Long"] == 316
    assert bza["Medium"] == 69
    assert bza["Short"] == 31
    assert bza["Total_Distinct_Trains"] == 416

    # MSB (Suburban only, zero long routes)
    msb = df_pivot.loc["MSB"]
    assert msb["Long"] == 0
    assert msb["Short"] == 484
    assert msb["Medium"] == 254
    assert msb["Total_Distinct_Trains"] == 738

    # SDAH (Medium route leader)
    sdah = df_pivot.loc["SDAH"]
    assert sdah["Medium"] == 348
    assert sdah["Short"] == 339
    assert sdah["Long"] == 58
    assert sdah["Total_Distinct_Trains"] == 745


OUTPUT_5_2 = Path("outputs/tables/task_5_2_route_crosstab.csv")
SCREENSHOT_5_2 = Path("screenshots/level5/task_5_2.png")
DOCS_5_2 = Path("documentation/level5/task_5_2.txt")


def test_task_5_2_artifacts_exist():
    """Verify that all Task 5.2 required artifacts exist and have non-zero size."""
    assert OUTPUT_5_2.is_file(), f"Cross-tab table missing: {OUTPUT_5_2}"
    assert OUTPUT_5_2.stat().st_size > 500, "Cross-tab CSV is unexpectedly small"
    assert SCREENSHOT_5_2.is_file(), f"Screenshot missing: {SCREENSHOT_5_2}"
    assert SCREENSHOT_5_2.stat().st_size > 1000, "Screenshot file is unexpectedly small"
    assert DOCS_5_2.is_file(), f"Documentation note missing: {DOCS_5_2}"
    assert DOCS_5_2.stat().st_size > 100, "Documentation note is unexpectedly small"


def test_task_5_2_crosstab_reconciliation():
    """Verify that cross-tabulation table reconciles with 11,113 total trains and 3 route types."""
    df_ct = pd.read_csv(OUTPUT_5_2)
    assert len(df_ct) == 11, f"Expected 11 rows (0-9 plus All), got {len(df_ct)}"

    required_cols = [
        "Prefix_Digit", "Service_Category", "Short", "Medium", "Long", "Total_Trains",
        "Pct_Short", "Pct_Medium", "Pct_Long", "Col_Pct_Short", "Col_Pct_Medium", "Col_Pct_Long"
    ]
    for col in required_cols:
        assert col in df_ct.columns, f"Missing column in crosstab: {col}"

    # Verify individual service rows (excluding 'All')
    df_services = df_ct[df_ct["Prefix_Digit"] != "All"]
    assert len(df_services) == 10

    # Internal row sums
    assert (df_services["Total_Trains"] == df_services["Short"] + df_services["Medium"] + df_services["Long"]).all()

    # Column sum reconciliations
    assert df_services["Short"].sum() == 3860
    assert df_services["Medium"].sum() == 3518
    assert df_services["Long"].sum() == 3735
    assert df_services["Total_Trains"].sum() == 11113

    # Total row verification
    total_row = df_ct[df_ct["Prefix_Digit"] == "All"].iloc[0]
    assert total_row["Short"] == 3860
    assert total_row["Medium"] == 3518
    assert total_row["Long"] == 3735
    assert total_row["Total_Trains"] == 11113


def test_task_5_2_spot_checks():
    """Spot-check specific service series in Task 5.2 cross-tab."""
    df_ct = pd.read_csv(OUTPUT_5_2).set_index("Prefix_Digit")

    # 9xxxx (Mumbai Suburban EMU)
    row_9 = df_ct.loc["9"]
    assert row_9["Short"] == 1578
    assert row_9["Medium"] == 172
    assert row_9["Long"] == 0
    assert row_9["Total_Trains"] == 1750
    assert row_9["Pct_Short"] == 90.17

    # 1xxxx (Mail / Express)
    row_1 = df_ct.loc["1"]
    assert row_1["Long"] == 1998
    assert row_1["Medium"] == 235
    assert row_1["Short"] == 80
    assert row_1["Total_Trains"] == 2313
    assert row_1["Col_Pct_Long"] == 53.49

    # 3xxxx (Kolkata EMU) - zero long routes
    row_3 = df_ct.loc["3"]
    assert row_3["Long"] == 0
    assert row_3["Short"] == 720
    assert row_3["Medium"] == 716

    # 4xxxx (Chennai / Delhi EMU) - zero long routes
    row_4 = df_ct.loc["4"]
    assert row_4["Long"] == 0
    assert row_4["Short"] == 710
    assert row_4["Medium"] == 401


HEATMAP_5_3 = Path("outputs/charts/task_5_3_station_pivot_heatmap.png")
BAR_5_3 = Path("outputs/charts/task_5_3_route_crosstab_bar.png")
SCREENSHOT_5_3 = Path("screenshots/level5/task_5_3.png")
DOCS_5_3 = Path("documentation/level5/task_5_3.txt")


def test_task_5_3_artifacts_exist():
    """Verify that all Task 5.3 visual and documentation artifacts exist and are non-empty."""
    assert HEATMAP_5_3.is_file(), f"Heatmap chart missing: {HEATMAP_5_3}"
    assert HEATMAP_5_3.stat().st_size > 50000, f"Heatmap chart unexpectedly small: {HEATMAP_5_3.stat().st_size} bytes"

    assert BAR_5_3.is_file(), f"Grouped bar chart missing: {BAR_5_3}"
    assert BAR_5_3.stat().st_size > 50000, f"Grouped bar chart unexpectedly small: {BAR_5_3.stat().st_size} bytes"

    assert SCREENSHOT_5_3.is_file(), f"Screenshot missing: {SCREENSHOT_5_3}"
    assert SCREENSHOT_5_3.stat().st_size > 1000, "Screenshot file is unexpectedly small"

    assert DOCS_5_3.is_file(), f"Documentation note missing: {DOCS_5_3}"
    assert DOCS_5_3.stat().st_size > 100, "Documentation note is unexpectedly small"


REPORT_5_4 = Path("documentation/level5/task_5_4_advanced_insights.md")
SCREENSHOT_5_4 = Path("screenshots/level5/task_5_4.png")
DOCS_5_4 = Path("documentation/level5/task_5_4.txt")


def test_task_5_4_artifacts_exist():
    """Verify that all Task 5.4 report and documentation artifacts exist and are non-empty."""
    assert REPORT_5_4.is_file(), f"Insights report missing: {REPORT_5_4}"
    assert REPORT_5_4.stat().st_size > 2000, f"Insights report unexpectedly small: {REPORT_5_4.stat().st_size} bytes"

    assert SCREENSHOT_5_4.is_file(), f"Screenshot missing: {SCREENSHOT_5_4}"
    assert SCREENSHOT_5_4.stat().st_size > 1000, "Screenshot file is unexpectedly small"

    assert DOCS_5_4.is_file(), f"Documentation note missing: {DOCS_5_4}"
    assert DOCS_5_4.stat().st_size > 100, "Documentation note is unexpectedly small"


def test_task_5_4_content_and_citations():
    """Verify that Level 5 insights report includes key factual data points and classifications."""
    content = REPORT_5_4.read_text(encoding="utf-8")

    # Verify classification tags
    assert "[DATA FACT]" in content, "Missing [DATA FACT] classification tags in report"
    assert "[INTERPRETATION]" in content, "Missing [INTERPRETATION] classification tags in report"

    # Verify key data citations
    assert "BZA" in content and "316" in content, "Missing BZA Long route leader citation"
    assert "CSMT" in content and "804" in content, "Missing CSMT Short route leader citation"
    assert "SDAH" in content and "348" in content, "Missing SDAH Medium route leader citation"
    assert "1xxxx" in content and "1,998" in content, "Missing 1xxxx Mail/Express Long route citation"
    assert "9xxxx" in content and "1,578" in content, "Missing 9xxxx Mumbai EMU Short route citation"
    assert "5xxxx" in content and "2,137" in content, "Missing 5xxxx Conventional Passenger fleet citation"



