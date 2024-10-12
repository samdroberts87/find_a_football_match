import pytest
from main import postcode_validation, convert_date_format, get_travel_miles
from unittest.mock import patch, MagicMock
import json

# Example mock data response from the API for a valid postcode (Bradford city AFC)
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


##### POSTCODE TESTS ######
# Test for postcode validation
def test_postcode_validation():
    # Load mock data using json
    mock_response_data = json.loads(mock_response_json)

    # Patch 'requests.get' to mock API response
    with patch("requests.get") as mock_get:
        # Mock the response status and json data
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response_data

        # Call your function to validate the postcode
        result = postcode_validation("BD8 7DY")

        # Check if the function returns True for a valid postcode
        assert result == True


def test_invalid_postcode():
    # Mock response for an invalid postcode (404 Not Found)
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 404
        mock_get.return_value.json.return_value = {
            "status": 404,
            "error": "Postcode not found",
        }

        result = postcode_validation("INVALIDCODE")
        assert result == False


def test_api_server_error():
    # Mock response for a server error (500)
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 500
        result = postcode_validation("BD8 7DY")
        assert result == False


##### DATE FORMAT TESTS #####
# Test for valid date format conversion
def test_convert_date_format_valid():
    with patch("builtins.input", side_effect=["12/10/2024"]):
        result = convert_date_format()
        assert result == "2024-10-12"  # Check if the date is correctly formatted


# Test for invalid date format and then valid
def test_convert_date_format_invalid_then_valid():
    with patch(
        "builtins.input", side_effect=["12/34/2024", "32/10/2024", "15/10/2024"]
    ):
        result = convert_date_format()
        assert result == "2024-10-15"  # The final valid input should be accepted


# Test invalid input multiple times
def test_convert_date_format_multiple_invalid():
    with patch("builtins.input", side_effect=["abcd", "1234", "12/10/2024"]):
        result = convert_date_format()
        assert result == "2024-10-12"  # Only the last valid date should be returned


##### TESTS FOR DISTANCE #####
# Test for valid numeric input
def test_get_travel_miles_valid():
    with patch("builtins.input", return_value="25.5"):
        result = get_travel_miles()
        assert result == 25.5  # Check that the function returns the correct float value


# Test for valid integer input
def test_get_travel_miles_valid_integer():
    with patch("builtins.input", return_value="10"):
        result = get_travel_miles()
        assert result == 10.0  # Check that the function returns 10.0 as a float


# Test for invalid input (string)
def test_get_travel_miles_invalid_string():
    with patch("builtins.input", side_effect=["abc", "25"]):
        result = get_travel_miles()
        assert result == 25.0  # The valid input should be accepted after invalid ones


# Test for invalid input (special characters)
def test_get_travel_miles_invalid_special_characters():
    with patch("builtins.input", side_effect=["$", "10.5"]):
        result = get_travel_miles()
        assert result == 10.5  # Check that valid float is returned


# Test for negative input
def test_get_travel_miles_negative():
    with patch("builtins.input", side_effect=["-5", "10"]):
        result = get_travel_miles()
        assert result == 10.0  # The valid input should be accepted after negative input


# Test for zero input
def test_get_travel_miles_zero():
    with patch("builtins.input", return_value="0"):
        result = get_travel_miles()
        assert result == 0.0  # Check that zero is accepted and returned correctly
