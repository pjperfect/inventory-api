"""
OpenFoodFacts API integration.

Provides functions to search for products by barcode or name
and format the results to match our inventory structure.
"""

import requests

BASE_URL = "https://world.openfoodfacts.org"


def fetch_product_by_barcode(barcode: str) -> dict | None:
    """
    Fetch a product from OpenFoodFacts by barcode.

    Returns a formatted product dict on success, or None if not found.
    """
    try:
        response = requests.get(f"{BASE_URL}/api/v0/product/{barcode}.json", timeout=5)

        # Guard against empty or non-JSON responses
        if response.status_code != 200 or not response.content:
            return None

        data = response.json()

        # OpenFoodFacts returns status 1 if the product was found
        if data.get("status") != 1:
            return None

        return _format_product(data["product"])

    except (
        requests.exceptions.RequestException,
        requests.exceptions.JSONDecodeError,
    ) as e:
        print(f"[external_api] Request failed: {e}")
        return None


def fetch_product_by_name(name: str) -> list[dict]:
    """
    Search for products on OpenFoodFacts by name.

    Returns a list of up to 5 formatted product dicts.
    """
    try:
        response = requests.get(
            f"{BASE_URL}/cgi/search.pl",
            params={
                "search_terms": name,
                "search_simple": 1,
                "action": "process",
                "json": 1,
                "page_size": 5,
            },
            timeout=5,
        )

        # Guard against empty or non-JSON responses
        if response.status_code != 200 or not response.content:
            return []

        data = response.json()
        products = data.get("products", [])
        return [_format_product(p) for p in products if p.get("product_name")]

    except (
        requests.exceptions.RequestException,
        requests.exceptions.JSONDecodeError,
    ) as e:
        print(f"[external_api] Request failed: {e}")
        return []


def _format_product(product: dict) -> dict:
    """
    Format an OpenFoodFacts product dict to match our inventory structure.

    Strips out fields we don't need and fills in defaults for missing ones.
    """
    return {
        "product_name": product.get("product_name", "Unknown"),
        "brands": product.get("brands", "Unknown"),
        "ingredients_text": product.get("ingredients_text", ""),
        "quantity": product.get("quantity", ""),
        "categories": product.get("categories", ""),
        "price": 0.0,
        "stock": 0,
    }
