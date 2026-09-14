"""Unit and integration tests for Level 6 Interactive Route Enquiry Application."""

from pathlib import Path
import pytest
from app.train_enquiry import TrainRouteEnquiryEngine, compute_segment_duration

SAMPLE_REPORT_PATH = Path("outputs/reports/enquiry_test_sample.txt")
SCREENSHOT_PATH = Path("screenshots/level6/task_6_1.png")
DOCS_PATH = Path("documentation/level6/task_6_1.txt")


@pytest.fixture(scope="module")
def engine():
    """Module-level fixture to load engine once for all tests."""
    return TrainRouteEnquiryEngine()


def test_task_6_1_artifacts_exist():
    """Verify that all Task 6.1 output, evidence, and documentation files exist."""
    assert SAMPLE_REPORT_PATH.is_file(), f"Sample report missing: {SAMPLE_REPORT_PATH}"
    assert SAMPLE_REPORT_PATH.stat().st_size > 1000, "Sample report is unexpectedly small"

    assert SCREENSHOT_PATH.is_file(), f"Screenshot missing: {SCREENSHOT_PATH}"
    assert SCREENSHOT_PATH.stat().st_size > 1000, "Screenshot is unexpectedly small"

    assert DOCS_PATH.is_file(), f"Documentation note missing: {DOCS_PATH}"
    assert DOCS_PATH.stat().st_size > 100, "Documentation note is unexpectedly small"


def test_segment_duration_calculation():
    """Verify midnight-safe duration helper."""
    # Same-day duration
    mins1, fmt1 = compute_segment_duration("08:00:00", "09:15:00")
    assert mins1 == 75
    assert fmt1 == "1h 15m"

    # Midnight rollover duration
    mins2, fmt2 = compute_segment_duration("23:30:00", "01:15:00")
    assert mins2 == 105
    assert fmt2 == "1h 45m"

    # Short sub-hour duration
    mins3, fmt3 = compute_segment_duration("10:00:00", "10:45:00")
    assert mins3 == 45
    assert fmt3 == "45m"


def test_engine_initialization(engine):
    """Verify engine indexes stations and trains correctly."""
    assert len(engine.code_to_name) == 8147
    assert len(engine.train_schedules) == 11113
    assert "CSMT" in engine.code_to_name
    assert "NDLS" in engine.code_to_name
    assert "BZA" in engine.code_to_name


def test_station_resolution(engine):
    """Verify code, name, case-insensitive, and trimmed whitespace station resolution."""
    # By exact Code
    res_code = engine.resolve_station("CSMT")
    assert res_code == ("CSMT", "CST-MUMBAI")

    # Lowercase code with whitespace
    res_lower = engine.resolve_station("  csmt  ")
    assert res_lower == ("CSMT", "CST-MUMBAI")

    # By Station Name (case-insensitive)
    res_name = engine.resolve_station("kalyan jn")
    assert res_name == ("KYN", "KALYAN JN")

    # Unknown station
    res_unknown = engine.resolve_station("XYZ_NONEXISTENT_STATION")
    assert res_unknown is None


def test_valid_query_with_direct_trains(engine):
    """Verify query between valid connected stations returns sorted direct trains."""
    response = engine.search_direct_trains("CSMT", "KYN")
    assert response["status"] == "SUCCESS"
    assert response["count"] > 0
    assert len(response["results"]) == response["count"]

    # Verify first train properties
    first = response["results"][0]
    assert first["Source_Code"] == "CSMT"
    assert first["Dest_Code"] == "KYN"
    assert first["Distance_km"] in [53, 54]  # CSMT (0 km) to KYN (53-54 km)
    assert first["Duration_Minutes"] > 0

    # Verify sorting by departure time
    dep_times = [t["Departure_Time"] for t in response["results"]]
    assert dep_times == sorted(dep_times)


def test_station_code_vs_name_interchangeability(engine):
    """Verify identical results whether querying by station codes or station names."""
    res_by_code = engine.search_direct_trains("BZA", "MAS")
    res_by_name = engine.search_direct_trains("VIJAYWADA JN", "CHENNAI CENTRAL")

    assert res_by_code["status"] == "SUCCESS"
    assert res_by_name["status"] == "SUCCESS"
    assert res_by_code["count"] == res_by_name["count"]

    trains_by_code = [t["Train_No"] for t in res_by_code["results"]]
    trains_by_name = [t["Train_No"] for t in res_by_name["results"]]
    assert trains_by_code == trains_by_name


def test_no_direct_trains_query(engine):
    """Verify explicit non-empty response when no direct trains connect two stations."""
    response = engine.search_direct_trains("KOTA JN", "DIBRUGARH")
    assert response["status"] == "NO_DIRECT_TRAINS"
    assert response["count"] == 0
    assert "No direct trains found" in response["message"]
    assert len(response["results"]) == 0


def test_invalid_station_query(engine):
    """Verify clean error message without crash on unknown station input."""
    # Invalid source
    res1 = engine.search_direct_trains("FAKE_SOURCE_STN", "CSMT")
    assert res1["status"] == "ERROR"
    assert "Unknown or invalid source station" in res1["message"]

    # Invalid destination
    res2 = engine.search_direct_trains("CSMT", "FAKE_DEST_STN")
    assert res2["status"] == "ERROR"
    assert "Unknown or invalid destination station" in res2["message"]


def test_same_source_and_destination_query(engine):
    """Verify explicit validation rejection when source equals destination."""
    response = engine.search_direct_trains("CSMT", "CST-MUMBAI")
    assert response["status"] == "ERROR"
    assert "identical" in response["message"].lower() or "same" in response["message"].lower()
    assert response["count"] == 0


def test_strict_directionality(engine):
    """Verify that source must be strictly BEFORE destination in sequence."""
    # Query Mumbai to Thane
    res_fwd = engine.search_direct_trains("CSMT", "TNA")
    assert res_fwd["status"] == "SUCCESS"
    for train in res_fwd["results"]:
        assert train["Distance_km"] > 0
        assert train["Source_Code"] == "CSMT"
        assert train["Dest_Code"] == "TNA"
