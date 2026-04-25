"""
Unit tests for CLI commands.
Uses unittest.mock to simulate HTTP requests made by the CLI.
"""

from unittest.mock import patch, MagicMock
import cli


def test_view_all_success(capsys):
    """CLI view_all prints items when API returns 200."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {"id": 1, "product_name": "Almond Milk", "brands": "Silk",
         "price": 4.99, "stock": 100, "ingredients_text": "",
         "quantity": "", "categories": ""}
    ]

    with patch("cli.requests.get", return_value=mock_response):
        cli.view_all()

    captured = capsys.readouterr()
    assert "Almond Milk" in captured.out


def test_view_single_not_found(capsys):
    """CLI view_single prints not found message on 404."""
    mock_response = MagicMock()
    mock_response.status_code = 404

    with patch("cli.requests.get", return_value=mock_response):
        with patch("builtins.input", return_value="999"):
            cli.view_single()

    captured = capsys.readouterr()
    assert "not found" in captured.out


def test_delete_item_cancelled(capsys):
    """CLI delete_item cancels when user does not confirm."""
    with patch("builtins.input", side_effect=["1", "n"]):
        cli.delete_item()

    captured = capsys.readouterr()
    assert "Cancelled" in captured.out


def test_add_item_invalid_price(capsys):
    """CLI add_item handles invalid price input gracefully."""
    with patch("builtins.input", side_effect=[
        "Test Product", "Test Brand", "", "", "", "not-a-price"
    ]):
        cli.add_item_manually()

    captured = capsys.readouterr()
    assert "Invalid" in captured.out