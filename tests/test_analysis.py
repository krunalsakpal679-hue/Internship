"""Test Suite: Analytical Tables, Pivot Tables, Cross-tabulations, and Chart Artifacts.

Covers:
- test_station_frequency: station-level traffic reconciliation and hub volume integrity.
- test_pivot_and_crosstab: marginal and cell-level reconciliation of pivot tables and cross-tabs.
- test_charts_generated: non-empty chart existence and valid visual dimensions.
"""

from pathlib import Path
import pandas as pd
import pytest

STATION_FREQ_PATH = Path("outputs/tables/task_2_4_station_frequency.csv")
STATION_PIVOT_PATH = Path("outputs/tables/task_5_1_station_pivot.csv")
ROUTE_CROSSTAB_PATH = Path("outputs/tables/task_5_2_route_crosstab.csv")

CHART_DURATION_TYPE = Path("outputs/charts/task_4_3_duration_by_route_type.png")
CHART_TRAFFIC_TOP15 = Path("outputs/charts/task_4_3_high_traffic_stations.png")
CHART_HISTOGRAM = Path("outputs/charts/task_4_3_duration_histogram.png")
CHART_HEATMAP = Path("outputs/charts/task_5_3_station_pivot_heatmap.png")
CHART_CROSSTAB_BAR = Path("outputs/charts/task_5_3_route_crosstab_bar.png")


def test_station_frequency():
    """Verify station frequency table integrity and top station rankings."""
    assert STATION_FREQ_PATH.is_file(), f"Station frequency table missing: {STATION_FREQ_PATH}"
    df_freq = pd.read_csv(STATION_FREQ_PATH)

    assert len(df_freq) == 8147, f"Expected 8,147 stations, got {len(df_freq)}"
    assert list(df_freq.columns) == ["Rank", "Station_Code", "Station_Name", "Train_Count", "Stop_Count"]

    # Invariant: Station train counts strictly positive
    assert (df_freq["Train_Count"] > 0).all()

    # Spot-check top hub (CSMT)
    top_station = df_freq.iloc[0]
    assert top_station["Station_Code"] == "CSMT"
    assert top_station["Train_Count"] == 1027


def test_pivot_and_crosstab_reconciliation():
    """Verify pivot table and structural cross-tab reconcile with source counts."""
    assert STATION_PIVOT_PATH.is_file()
    assert ROUTE_CROSSTAB_PATH.is_file()

    df_pivot = pd.read_csv(STATION_PIVOT_PATH)
    df_cross = pd.read_csv(ROUTE_CROSSTAB_PATH)

    # 1. Pivot Table Reconciliations
    assert len(df_pivot) == 8147
    assert (df_pivot["Total_Distinct_Trains"] == df_pivot["Short"] + df_pivot["Medium"] + df_pivot["Long"]).all()

    # Spot-check key stations
    pivot_indexed = df_pivot.set_index("Station_Code")
    assert pivot_indexed.loc["CSMT", "Short"] == 804
    assert pivot_indexed.loc["BZA", "Long"] == 316
    assert pivot_indexed.loc["SDAH", "Medium"] == 348
    assert pivot_indexed.loc["MSB", "Long"] == 0

    # 2. Structural Cross-tab Reconciliations
    assert len(df_cross) == 11
    services = df_cross[df_cross["Prefix_Digit"] != "All"]
    assert services["Short"].sum() == 3860
    assert services["Medium"].sum() == 3518
    assert services["Long"].sum() == 3735
    assert services["Total_Trains"].sum() == 11113

    # Spot-check key series
    cross_indexed = df_cross.set_index("Prefix_Digit")
    assert cross_indexed.loc["1", "Long"] == 1998
    assert cross_indexed.loc["9", "Short"] == 1578
    assert cross_indexed.loc["9", "Long"] == 0


def test_charts_generated():
    """Verify all Level 4 and Level 5 analytical chart PNG files exist and are non-empty."""
    required_charts = [
        CHART_DURATION_TYPE,
        CHART_TRAFFIC_TOP15,
        CHART_HISTOGRAM,
        CHART_HEATMAP,
        CHART_CROSSTAB_BAR
    ]
    for chart in required_charts:
        assert chart.is_file(), f"Chart file missing: {chart}"
        assert chart.stat().st_size > 50000, f"Chart file unexpectedly small ({chart.stat().st_size} bytes): {chart}"
