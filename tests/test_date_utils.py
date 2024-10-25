import pytest
from unittest.mock import patch
from modules.date_utils import convert_date_format


def test_convert_date_format_out_of_range():
    with patch(
        "builtins.input", side_effect=["32/12/2024", "15/13/2024", "15/10/2024"]
    ):
        result = convert_date_format()
        assert result == "2024-10-15"


def test_convert_date_format_past_year():
    with patch("builtins.input", side_effect=["12/10/2023", "12/10/2024"]):
        result = convert_date_format()
        assert result == "2024-10-12"


def test_convert_date_format_valid():
    with patch("builtins.input", side_effect=["12/10/2024"]):
        result = convert_date_format()
        assert result == "2024-10-12"


def test_convert_date_format_invalid_then_valid():
    with patch(
        "builtins.input", side_effect=["12/34/2024", "32/10/2024", "15/10/2024"]
    ):
        result = convert_date_format()
        assert result == "2024-10-15"


def test_convert_date_format_multiple_invalid():
    with patch("builtins.input", side_effect=["abcd", "1234", "12/10/2024"]):
        result = convert_date_format()
        assert result == "2024-10-12"


def test_convert_date_format_multiple_invalid():
    with patch(
        "builtins.input", side_effect=["29/02/2025", "31/09/2024", "12/10/2024"]
    ):
        result = convert_date_format()
        assert result == "2024-10-12"
