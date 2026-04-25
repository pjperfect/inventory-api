"""
Unit tests for Flask API endpoints.
Uses Flask's built-in test client to simulate HTTP requests.
"""

import pytest
from app import app
from inventory import inventory


@pytest.fixture(autouse=True)
def reset_inventory():
    """Reset inventory to a known state before each test."""
    inventory.clear()
    inventory.extend([
        {
            "id": 1,
            "product_name": "Organic Almond Milk",
            "brands": "Silk",
            "ingredients_text": "Filtered water, almonds",
            "quantity": "64 fl oz",
            "categories": "Beverages",
            "price": 4.99,
            "stock": 120
        },
        {
            "id": 2,
            "product_name": "Greek Yogurt",
            "brands": "Chobani",
            "ingredients_text": "Cultured nonfat milk",
            "quantity": "32 oz",
            "categories": "Dairy",
            "price": 6.49,
            "stock": 85
        },
    ])


@pytest.fixture
def client():
    """Return a Flask test client."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# ---------------------------------------------------------------------------
# GET /inventory
# ---------------------------------------------------------------------------

def test_get_inventory_returns_200(client):
    response = client.get("/inventory")
    assert response.status_code == 200


def test_get_inventory_returns_list(client):
    response = client.get("/inventory")
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 2


# ---------------------------------------------------------------------------
# GET /inventory/<id>
# ---------------------------------------------------------------------------

def test_get_item_returns_200(client):
    response = client.get("/inventory/1")
    assert response.status_code == 200


def test_get_item_returns_correct_item(client):
    response = client.get("/inventory/1")
    data = response.get_json()
    assert data["product_name"] == "Organic Almond Milk"


def test_get_item_returns_404_if_not_found(client):
    response = client.get("/inventory/999")
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# POST /inventory
# ---------------------------------------------------------------------------

def test_add_item_returns_201(client):
    payload = {
        "product_name": "Orange Juice",
        "brands": "Tropicana",
        "price": 3.99,
        "stock": 50
    }
    response = client.post("/inventory", json=payload)
    assert response.status_code == 201


def test_add_item_appears_in_inventory(client):
    payload = {
        "product_name": "Orange Juice",
        "brands": "Tropicana",
        "price": 3.99,
        "stock": 50
    }
    client.post("/inventory", json=payload)
    response = client.get("/inventory")
    data = response.get_json()
    assert len(data) == 3


def test_add_item_missing_fields_returns_422(client):
    payload = {"product_name": "Orange Juice"}
    response = client.post("/inventory", json=payload)
    assert response.status_code == 422


# ---------------------------------------------------------------------------
# PATCH /inventory/<id>
# ---------------------------------------------------------------------------

def test_update_item_returns_200(client):
    response = client.patch("/inventory/1", json={"price": 9.99})
    assert response.status_code == 200


def test_update_item_changes_value(client):
    client.patch("/inventory/1", json={"price": 9.99})
    response = client.get("/inventory/1")
    data = response.get_json()
    assert data["price"] == 9.99


def test_update_item_returns_404_if_not_found(client):
    response = client.patch("/inventory/999", json={"price": 9.99})
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# DELETE /inventory/<id>
# ---------------------------------------------------------------------------

def test_delete_item_returns_204(client):
    response = client.delete("/inventory/1")
    assert response.status_code == 204


def test_delete_item_removes_from_inventory(client):
    client.delete("/inventory/1")
    response = client.get("/inventory")
    data = response.get_json()
    assert len(data) == 1


def test_delete_item_returns_404_if_not_found(client):
    response = client.delete("/inventory/999")
    assert response.status_code == 404