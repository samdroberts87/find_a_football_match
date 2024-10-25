import pytest
from unittest.mock import patch
from modules.date_utils import convert_date_format


# Test for a valid date within range
def test_convert_date_format_valid_date():
    with patch("builtins.input", side_effect=["12/11/2024"]):
        result = convert_date_format()
        assert result == "2024-11-12"


# Test for an invalid day in a 30-day month
def test_convert_date_format_invalid_day():
    with patch(
        "builtins.input", side_effect=["31/04/2024", "30/04/2024", "12/11/2024"]
    ):
        result = convert_date_format()
        assert result == "2024-11-12"


# Test for a date more than 36 days in the future
def test_convert_date_format_future_date():
    with patch("builtins.input", side_effect=["15/12/2024", "12/11/2024"]):
        result = convert_date_format()
        assert result == "2024-11-12"


# Test for an invalid format (no slashes)
def test_convert_date_format_invalid_format():
    with patch("builtins.input", side_effect=["12112024", "12/11/2024"]):
        result = convert_date_format()
        assert result == "2024-11-12"


# Test for a past date
def test_convert_date_format_past_date():
    with patch("builtins.input", side_effect=["10/10/2023", "12/11/2024"]):
        result = convert_date_format()
        assert result == "2024-11-12"
