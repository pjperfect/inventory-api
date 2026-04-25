"""
Unit tests for OpenFoodFacts API integration.
Uses unittest.mock to simulate API responses without real network calls.
"""

import pytest
from unittest.mock import patch, MagicMock
from external_api import fetch_product_by_barcode, fetch_product_by_name


# ---------------------------------------------------------------------------
# fetch_product_by_barcode
# ---------------------------------------------------------------------------

def test_fetch_product_by_barcode_success():
    """Returns formatted product when API responds with status 1."""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "status": 1,
        "product": {
            "product_name": "Almond Milk",
            "brands": "Silk",
            "ingredients_text": "Water, almonds",
            "quantity": "64 fl oz",
            "categories": "Beverages",
        }
    }

    with patch("external_api.requests.get", return_value=mock_response):
        result = fetch_product_by_barcode("012345678901")

    assert result is not None
    assert result["product_name"] == "Almond Milk"
    assert result["brands"] == "Silk"
    assert result["price"] == 0.0
    assert result["stock"] == 0


def test_fetch_product_by_barcode_not_found():
    """Returns None when API responds with status 0."""
    mock_response = MagicMock()
    mock_response.json.return_value = {"status": 0}

    with patch("external_api.requests.get", return_value=mock_response):
        result = fetch_product_by_barcode("000000000000")

    assert result is None


def test_fetch_product_by_barcode_network_error():
    """Returns None on network failure."""
    import requests as req
    with patch("external_api.requests.get", side_effect=req.exceptions.RequestException):
        result = fetch_product_by_barcode("012345678901")

    assert result is None


# ---------------------------------------------------------------------------
# fetch_product_by_name
# ---------------------------------------------------------------------------

def test_fetch_product_by_name_returns_list():
    """Returns a list of formatted products on success."""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "products": [
            {
                "product_name": "Almond Milk",
                "brands": "Silk",
                "ingredients_text": "Water, almonds",
                "quantity": "64 fl oz",
                "categories": "Beverages",
            },
            {
                "product_name": "Oat Milk",
                "brands": "Oatly",
                "ingredients_text": "Water, oats",
                "quantity": "32 fl oz",
                "categories": "Beverages",
            }
        ]
    }

    with patch("external_api.requests.get", return_value=mock_response):
        results = fetch_product_by_name("almond milk")

    assert isinstance(results, list)
    assert len(results) == 2
    assert results[0]["product_name"] == "Almond Milk"


def test_fetch_product_by_name_network_error():
    """Returns empty list on network failure."""
    import requests as req
    with patch("external_api.requests.get", side_effect=req.exceptions.RequestException):
        results = fetch_product_by_name("almond milk")

    assert results == []