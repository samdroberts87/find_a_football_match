import pytest
from unittest.mock import patch, MagicMock
from modules.geolocation import get_travel_miles, get_coordinates


def test_get_travel_miles_large_number():
    with patch("builtins.input", return_value="10000"):
        result = get_travel_miles()
        assert result == 10000.0


def test_get_travel_miles_valid():
    with patch("builtins.input", return_value="25.5"):
        result = get_travel_miles()
        assert result == 25.5


def test_get_travel_miles_valid_integer():
    with patch("builtins.input", return_value="10"):
        result = get_travel_miles()
        assert result == 10.0


def test_get_travel_miles_invalid_string():
    with patch("builtins.input", side_effect=["abc", "25"]):
        result = get_travel_miles()
        assert result == 25.0


def test_get_travel_miles_invalid_special_characters():
    with patch("builtins.input", side_effect=["$", "10.5"]):
        result = get_travel_miles()
        assert result == 10.5


def test_get_travel_miles_negative():
    with patch("builtins.input", side_effect=["-5", "10"]):
        result = get_travel_miles()
        assert result == 10.0


def test_get_travel_miles_zero():
    with patch("builtins.input", return_value="0"):
        result = get_travel_miles()
        assert result == 0.0


@patch("geopy.geocoders.Nominatim.geocode")
def test_get_coordinates_valid_postcode(mock_geocode):
    mock_geocode.return_value = MagicMock(latitude=53.803578, longitude=-1.759482)
    result = get_coordinates("BD8 7DY")
    assert result == (53.803578, -1.759482)


@patch("geopy.geocoders.Nominatim.geocode", return_value=None)
def test_get_coordinates_invalid_postcode(mock_geocode):
    result = get_coordinates("INVALID")
    assert result is None
