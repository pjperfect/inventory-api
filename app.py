"""
Flask REST API for the Inventory Management System.

Endpoints
---------
GET    /inventory                                           — fetch all inventory items
GET    /inventory/<id>                                      — fetch a single item
POST   /inventory                                           — add a new item
PATCH  /inventory/<id>                                      — update an existing item
DELETE /inventory/<id>                                      — remove an item
GET    /inventory/barcode/<barcode>                         — fetch product from OpenFoodFacts by barcode
GET    /inventory/search?name=<name>                        — search OpenFoodFacts by product name
"""

from flask import Flask, request, jsonify, make_response
from inventory import inventory, get_next_id, find_item
from external_api import fetch_product_by_barcode, fetch_product_by_name

app = Flask(__name__)


# ---------------------------------------------------------------------------
# GET /inventory — fetch all items
# ---------------------------------------------------------------------------


@app.route("/inventory", methods=["GET"])
def get_inventory():
    """Return the full inventory list."""
    return make_response(jsonify(inventory), 200)


# ---------------------------------------------------------------------------
# GET /inventory/<id> — fetch a single item by ID
# ---------------------------------------------------------------------------


@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_item(item_id):
    """Return a single inventory item by ID."""
    item = find_item(item_id)
    if not item:
        return make_response(
            jsonify({"error": f"Item with id {item_id} not found"}), 404
        )
    return make_response(jsonify(item), 200)


# ---------------------------------------------------------------------------
# POST /inventory — add a new item
# ---------------------------------------------------------------------------


@app.route("/inventory", methods=["POST"])
def add_item():
    """
    Add a new item to the inventory.

    Expects JSON with at least: product_name, brands, price, stock.
    """
    data = request.get_json(silent=True) or {}

    # Validate required fields
    required = ["product_name", "brands", "price", "stock"]
    missing = [field for field in required if field not in data]
    if missing:
        return make_response(
            jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 422
        )

    new_item = {
        "id": get_next_id(),
        "product_name": data["product_name"],
        "brands": data["brands"],
        "ingredients_text": data.get("ingredients_text", ""),
        "quantity": data.get("quantity", ""),
        "categories": data.get("categories", ""),
        "price": data["price"],
        "stock": data["stock"],
    }

    inventory.append(new_item)
    return make_response(jsonify(new_item), 201)


# ---------------------------------------------------------------------------
# PATCH /inventory/<id> — update an existing item
# ---------------------------------------------------------------------------


@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
    """
    Update an existing inventory item.

    Accepts any subset of item fields to update.
    """
    item = find_item(item_id)
    if not item:
        return make_response(
            jsonify({"error": f"Item with id {item_id} not found"}), 404
        )

    data = request.get_json(silent=True) or {}

    # Only update fields that are provided
    updatable_fields = [
        "product_name",
        "brands",
        "ingredients_text",
        "quantity",
        "categories",
        "price",
        "stock",
    ]
    for field in updatable_fields:
        if field in data:
            item[field] = data[field]

    return make_response(jsonify(item), 200)


# ---------------------------------------------------------------------------
# DELETE /inventory/<id> — remove an item from the inventory
# ---------------------------------------------------------------------------


@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    """Remove an item from the inventory by ID."""
    item = find_item(item_id)
    if not item:
        return make_response(
            jsonify({"error": f"Item with id {item_id} not found"}), 404
        )

    inventory.remove(item)
    return make_response("", 204)


# --------------------------------------------------------------------------------
# GET /inventory/barcode/<barcode> — fetch a product from OpenFoodFacts by barcode
# --------------------------------------------------------------------------------


@app.route("/inventory/barcode/<string:barcode>", methods=["GET"])
def get_by_barcode(barcode):
    """Fetch a product from OpenFoodFacts by barcode."""
    product = fetch_product_by_barcode(barcode)
    if not product:
        return make_response(jsonify({"error": "Product not found"}), 404)
    return make_response(jsonify(product), 200)


# ---------------------------------------------------------------------------
# GET /inventory/search — search OpenFoodFacts by product name
# ---------------------------------------------------------------------------


@app.route("/inventory/search", methods=["GET"])
def search_products():
    """Search OpenFoodFacts by product name."""
    name = request.args.get("name", "").strip()
    if not name:
        return make_response(
            jsonify({"error": "name query parameter is required"}), 422
        )
    products = fetch_product_by_name(name)
    return make_response(jsonify(products), 200)


if __name__ == "__main__":
    app.run(debug=True)