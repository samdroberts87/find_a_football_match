import pytest
from unittest.mock import patch
import requests
from modules.validation import postcode_validation

# Mock API response for a valid postcode
mock_response_json = """
{
    "status": 200,
    "result": {
        "postcode": "BD8 7DY",
        "quality": 1,
        "eastings": 415938,
        "northings": 434169,
        "country": "England",
        "nhs_ha": "Yorkshire and the Humber",
        "longitude": -1.759482,
        "latitude": 53.803578,
        "european_electoral_region": "Yorkshire and The Humber",
        "primary_care_trust": "Bradford and Airedale Teaching",
        "region": "Yorkshire and The Humber",
        "lsoa": "Bradford 039J",
        "msoa": "Bradford 039",
        "incode": "7DY",
        "outcode": "BD8",
        "parliamentary_constituency": "Bradford West",
        "parliamentary_constituency_2024": "Bradford West",
        "admin_district": "Bradford",
        "parish": "Bradford, unparished area",
        "admin_county": null,
        "date_of_introduction": "198001",
        "admin_ward": "Manningham",
        "ced": null,
        "ccg": "NHS West Yorkshire",
        "nuts": "Bradford",
        "pfa": "West Yorkshire",
        "codes": {
            "admin_district": "E08000032",
            "admin_county": "E99999999",
            "admin_ward": "E05001359",
            "parish": "E43000274",
            "parliamentary_constituency": "E14001120",
            "parliamentary_constituency_2024": "E14001120",
            "ccg": "E38000232",
            "ccg_id": "36J",
            "ced": "E99999999",
            "nuts": "TLE41",
            "lsoa": "E01033693",
            "msoa": "E02002221",
            "lau2": "E08000032",
            "pfa": "E23000010"
        }
    }
}
"""



def test_invalid_postcode():
    with patch("requests.get") as mock_get, patch("builtins.input", return_value="INVALIDCODE"):
        mock_get.return_value.status_code = 404
        mock_get.return_value.json.return_value = {
            "status": 404,
            "error": "Postcode not found",
        }
        result = postcode_validation(max_retries=1)  # Limit retries to 1 for testing
        assert result is None  # Now expects None on failure



def test_api_server_error():
    with patch("requests.get") as mock_get, patch("builtins.input", return_value="BD8 7DY"):
        mock_get.return_value.status_code = 500
        result = postcode_validation()
        assert result is None  # Now expects None on failure


def test_postcode_validation_request_exception():
    with patch("requests.get", side_effect=requests.RequestException("Network error")), patch("builtins.input", return_value="BD8 7DY"):
        result = postcode_validation()
        assert result is None  # Now expects None on failure


def test_postcode_validation_timeout():
    with patch("requests.get", side_effect=requests.Timeout), patch("builtins.input", return_value="BD8 7DY"):
        result = postcode_validation()
        assert result is None  # Now expects None on failure
