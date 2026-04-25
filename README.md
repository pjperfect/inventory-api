# Inventory API

A Flask-based REST API for an inventory management system used by retail employees.
The system allows staff to add, view, update, and delete inventory items. It also
integrates with the OpenFoodFacts API to fetch real-time product data by barcode or
name, and includes a CLI frontend for direct terminal interaction.

---

## Tech Stack

- **Flask** — web framework and REST API
- **Requests** — HTTP client for OpenFoodFacts API integration
- **Pytest** — unit testing framework
- **uv** — fast Python package manager

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/pjperfect/inventory-api.git
cd inventory-api
```

### 2. Install dependencies with `uv`

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh

uv venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
uv sync
```

---

## Running the Server

```bash
flask run
```

The API runs at `http://127.0.0.1:5000` by default.

---

## Running the CLI

Make sure the Flask server is running first, then in a separate terminal:

```bash
python cli.py
```

The CLI menu will guide you through all available actions.

---

## Running Tests

```bash
pytest tests/ -v
```

---

## API Endpoints

### Inventory

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/inventory` | Fetch all inventory items |
| `GET` | `/inventory/<id>` | Fetch a single item by ID |
| `POST` | `/inventory` | Add a new item |
| `PATCH` | `/inventory/<id>` | Update an existing item |
| `DELETE` | `/inventory/<id>` | Remove an item |

#### GET `/inventory`

```json
// 200 response
[
  {
    "id": 1,
    "product_name": "Organic Almond Milk",
    "brands": "Silk",
    "ingredients_text": "Filtered water, almonds, cane sugar, sea salt",
    "quantity": "64 fl oz",
    "categories": "Beverages",
    "price": 4.99,
    "stock": 120
  }
]
```

#### POST `/inventory`

```json
// Request body (product_name, brands, price, stock are required)
{
  "product_name": "Orange Juice",
  "brands": "Tropicana",
  "ingredients_text": "100% pure squeezed pasteurized orange juice",
  "quantity": "52 fl oz",
  "categories": "Juices, Beverages",
  "price": 3.99,
  "stock": 200
}

// 201 response
{
  "id": 6,
  "product_name": "Orange Juice",
  "brands": "Tropicana",
  "ingredients_text": "100% pure squeezed pasteurized orange juice",
  "quantity": "52 fl oz",
  "categories": "Juices, Beverages",
  "price": 3.99,
  "stock": 200
}
```

#### PATCH `/inventory/<id>`

```json
// Request body (any subset of fields)
{ "price": 4.49, "stock": 180 }

// 200 response
{
  "id": 6,
  "product_name": "Orange Juice",
  "brands": "Tropicana",
  "price": 4.49,
  "stock": 180
}
```

#### DELETE `/inventory/<id>`

```
// 204 No Content on success
// 404 Not Found if item does not exist
```

---

### External API Integration (OpenFoodFacts)

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/inventory/barcode/<barcode>` | Fetch product details from OpenFoodFacts by barcode |
| `GET` | `/inventory/search?name=<name>` | Search OpenFoodFacts by product name |

#### GET `/inventory/barcode/<barcode>`

```json
// 200 response
{
  "product_name": "Almond Milk",
  "brands": "Silk",
  "ingredients_text": "Filtered water, almonds",
  "quantity": "64 fl oz",
  "categories": "Beverages",
  "price": 0.0,
  "stock": 0
}

// 404 response
{ "error": "Product not found" }
```

#### GET `/inventory/search?name=almond milk`

```json
// 200 response
[
  {
    "product_name": "Almond Milk",
    "brands": "Silk",
    "ingredients_text": "Filtered water, almonds",
    "quantity": "64 fl oz",
    "categories": "Beverages",
    "price": 0.0,
    "stock": 0
  }
]
```

---

## CLI Commands

Once the CLI is running (`python cli.py`), the following options are available:

| Option | Action |
|--------|--------|
| `1` | View all inventory items |
| `2` | View a single item by ID |
| `3` | Add a new item manually |
| `4` | Add an item from OpenFoodFacts by barcode |
| `5` | Search OpenFoodFacts by product name |
| `6` | Update an item's price or stock |
| `7` | Delete an item |
| `8` | Exit |

### Example CLI Session

```
===== Inventory Management System =====
1. View all inventory items
2. View a single item
3. Add a new item manually
4. Add an item from OpenFoodFacts by barcode
5. Search OpenFoodFacts by name
6. Update an item
7. Delete an item
8. Exit
=======================================
Enter your choice: 4

Enter barcode: 012345678901

Product found:
----------------------------------------
  product_name: Almond Milk
  brands: Silk
  price: 0.0
  stock: 0
----------------------------------------
Set price: 4.99
Set stock quantity: 100

Item added to inventory!
```

---

## Project Structure

```
inventory-api/
├── app.py              # Flask app and all API endpoints
├── inventory.py        # In-memory inventory array and helpers
├── external_api.py     # OpenFoodFacts API integration
├── cli.py              # CLI frontend
├── tests/
│   ├── __init__.py
│   ├── test_endpoints.py    # Tests for Flask API endpoints
│   ├── test_external_api.py # Tests for OpenFoodFacts integration
│   └── test_cli.py          # Tests for CLI commands
├── pyproject.toml      # uv dependencies
└── README.md
```