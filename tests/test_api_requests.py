import pytest
from unittest.mock import patch
from modules.api_requests import get_fixtures


@patch("requests.get")
def test_get_fixtures_no_fixtures(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"data": []}
    result = get_fixtures("2024-10-19")
    assert result == []


@patch("requests.get")
def test_get_fixtures_with_fixtures(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "data": [
            {"homeTeam": {"name": "Liverpool"}},
            {"homeTeam": {"name": "Manchester United"}},
        ]
    }
    result = get_fixtures("2024-10-19")
    assert result == ["Liverpool", "Manchester United"]


@patch("requests.get")
def test_get_fixtures_api_failure(mock_get):
    mock_get.return_value.status_code = 500
    result = get_fixtures("2024-10-19")
    assert result == []
