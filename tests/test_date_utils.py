import pytest
from unittest.mock import patch
from datetime import datetime, timedelta
from modules.date_utils import convert_date_format

# function to generate dates dynamically
def get_test_dates():
    today = datetime.now()
    valid_date = today + timedelta(weeks=4)  # Within the 5-week range
    future_invalid_date = today + timedelta(weeks=6)  # More than 5 weeks in the future
    past_date = today - timedelta(days=10)  # 10 days in the past

    return {
        "valid_date": valid_date.strftime("%d/%m/%Y"),
        "future_invalid_date": future_invalid_date.strftime("%d/%m/%Y"),
        "past_date": past_date.strftime("%d/%m/%Y"),
        "valid_date_output": valid_date.strftime("%Y-%m-%d"),
    }

# Test for a valid date within range
def test_convert_date_format_valid_date():
    test_dates = get_test_dates()
    with patch("builtins.input", side_effect=[test_dates["valid_date"]]):
        result = convert_date_format()
        assert result == test_dates["valid_date_output"]

# Test for an invalid day in a 30-day month
def test_convert_date_format_invalid_day():
    test_dates = get_test_dates()
    with patch("builtins.input", side_effect=["31/04/2024", test_dates["valid_date"]]):
        result = convert_date_format()
        assert result == test_dates["valid_date_output"]

# Test for a date more than 5 weeks in the future
def test_convert_date_format_future_date():
    test_dates = get_test_dates()
    with patch("builtins.input", side_effect=[test_dates["future_invalid_date"], test_dates["valid_date"]]):
        result = convert_date_format()
        assert result == test_dates["valid_date_output"]

# Test for an invalid format (no slashes)
def test_convert_date_format_invalid_format():
    test_dates = get_test_dates()
    with patch("builtins.input", side_effect=["12112024", test_dates["valid_date"]]):
        result = convert_date_format()
        assert result == test_dates["valid_date_output"]

# Test for a past date
def test_convert_date_format_past_date():
    test_dates = get_test_dates()
    with patch("builtins.input", side_effect=[test_dates["past_date"], test_dates["valid_date"]]):
        result = convert_date_format()
        assert result == test_dates["valid_date_output"]
