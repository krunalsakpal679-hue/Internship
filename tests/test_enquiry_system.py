"""Test Suite: Interactive Route Enquiry Application.

Covers:
- test_enquiry_system_valid: direct-train queries return expected trains sorted by departure time.
- test_enquiry_system_no_results: explicit empty result with explanatory message for disconnected pairs.
- test_enquiry_system_invalid_station: handled user error for non-existent station codes/names.
- test_enquiry_system_same_station: rejected query for identical source and destination.
- test_enquiry_system_normalization: case and whitespace insensitivity across codes and names.
- test_enquiry_system_strict_directionality: reverse-direction trains not falsely returned.
"""

from pathlib import Path
import pytest
from app.train_enquiry import TrainRouteEnquiryEngine

SAMPLE_REPORT_PATH = Path("outputs/reports/enquiry_test_sample.txt")


@pytest.fixture(scope="module")
def engine():
    """Load train enquiry engine once."""
    return TrainRouteEnquiryEngine()


def test_enquiry_system_valid(engine):
    """Verify valid query returns expected direct trains sorted by departure time."""
    response = engine.search_direct_trains("CSMT", "KYN")
    assert response["status"] == "SUCCESS"
    assert response["count"] > 0
    assert len(response["results"]) == response["count"]

    # Verify first train
    first = response["results"][0]
    assert first["Source_Code"] == "CSMT"
    assert first["Dest_Code"] == "KYN"
    assert first["Distance_km"] in [53, 54]
    assert first["Duration_Minutes"] > 0

    # Verify chronological sorting
    dep_times = [t["Departure_Time"] for t in response["results"]]
    assert dep_times == sorted(dep_times)


def test_enquiry_system_no_results(engine):
    """Verify disconnected station pair returns explicit NO_DIRECT_TRAINS message."""
    response = engine.search_direct_trains("KOTA JN", "DIBRUGARH")
    assert response["status"] == "NO_DIRECT_TRAINS"
    assert response["count"] == 0
    assert len(response["results"]) == 0
    assert "No direct trains found" in response["message"]


def test_enquiry_system_invalid_station(engine):
    """Verify unknown station names/codes return clean ERROR without crashing."""
    # Unknown source
    res1 = engine.search_direct_trains("INVALID_SOURCE_CODE", "CSMT")
    assert res1["status"] == "ERROR"
    assert "Unknown or invalid source station" in res1["message"]

    # Unknown destination
    res2 = engine.search_direct_trains("CSMT", "INVALID_DEST_CODE")
    assert res2["status"] == "ERROR"
    assert "Unknown or invalid destination station" in res2["message"]


def test_enquiry_system_same_station(engine):
    """Verify query with identical source and destination is rejected."""
    response = engine.search_direct_trains("CSMT", "CST-MUMBAI")
    assert response["status"] == "ERROR"
    assert "identical" in response["message"].lower() or "same" in response["message"].lower()
    assert response["count"] == 0


def test_enquiry_system_normalization(engine):
    """Verify case, whitespace, and code/name interchangeability."""
    res_code = engine.search_direct_trains("  bza  ", "  mas  ")
    res_name = engine.search_direct_trains("VIJAYWADA JN", "CHENNAI CENTRAL")

    assert res_code["status"] == "SUCCESS"
    assert res_name["status"] == "SUCCESS"
    assert res_code["count"] == res_name["count"]

    trains_code = [t["Train_No"] for t in res_code["results"]]
    trains_name = [t["Train_No"] for t in res_name["results"]]
    assert trains_code == trains_name


def test_enquiry_system_strict_directionality(engine):
    """Verify that source strictly precedes destination in travel sequence."""
    response = engine.search_direct_trains("CSMT", "TNA")
    assert response["status"] == "SUCCESS"
    for train in response["results"]:
        assert train["Distance_km"] > 0
        assert train["Source_Code"] == "CSMT"
        assert train["Dest_Code"] == "TNA"
