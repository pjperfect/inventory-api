"""
CLI frontend for the Inventory Management System.

Interacts with the Flask API running at http://127.0.0.1:5000.
Run the Flask app first before using the CLI:
    flask run

Usage:
    python cli.py
"""

import requests

BASE_URL = "http://127.0.0.1:5000"


# ---------------------------------------------------------------------------
# Display helpers
# ---------------------------------------------------------------------------


def print_item(item: dict):
    """Pretty print a single inventory item."""
    print("\n" + "-" * 40)
    for key, value in item.items():
        print(f"  {key}: {value}")
    print("-" * 40)


def print_menu():
    """Print the main menu."""
    print("\n===== Inventory Management System =====")
    print("1. View all inventory items")
    print("2. View a single item")
    print("3. Add a new item manually")
    print("4. Add an item from OpenFoodFacts by barcode")
    print("5. Search OpenFoodFacts by name")
    print("6. Update an item")
    print("7. Delete an item")
    print("8. Exit")
    print("=======================================")


# ---------------------------------------------------------------------------
# CLI actions
# ---------------------------------------------------------------------------


def view_all():
    """Fetch and display all inventory items."""
    response = requests.get(f"{BASE_URL}/inventory")
    if response.status_code == 200:
        items = response.json()
        if not items:
            print("\nNo items in inventory.")
        for item in items:
            print_item(item)
    else:
        print(f"\nError fetching inventory: {response.status_code}")


def view_single():
    """Fetch and display a single inventory item by ID."""
    try:
        item_id = int(input("\nEnter item ID: "))
    except ValueError:
        print("Invalid ID — must be an integer.")
        return

    response = requests.get(f"{BASE_URL}/inventory/{item_id}")
    if response.status_code == 200:
        print_item(response.json())
    elif response.status_code == 404:
        print(f"\nItem with id {item_id} not found.")
    else:
        print(f"\nError: {response.status_code}")


def add_item_manually():
    """Prompt the user for item details and add it to the inventory."""
    print("\n--- Add New Item ---")
    product_name = input("Product name: ").strip()
    brands = input("Brand: ").strip()
    ingredients_text = input("Ingredients (optional): ").strip()
    quantity = input("Quantity (optional): ").strip()
    categories = input("Categories (optional): ").strip()

    try:
        price = float(input("Price: "))
        stock = int(input("Stock: "))
    except ValueError:
        print(
            "Invalid price or stock — price must be a number, stock must be an integer."
        )
        return

    payload = {
        "product_name": product_name,
        "brands": brands,
        "ingredients_text": ingredients_text,
        "quantity": quantity,
        "categories": categories,
        "price": price,
        "stock": stock,
    }

    response = requests.post(f"{BASE_URL}/inventory", json=payload)
    if response.status_code == 201:
        print("\nItem added successfully!")
        print_item(response.json())
    else:
        print(f"\nError adding item: {response.json()}")


def add_item_by_barcode():
    """
    Fetch product details from OpenFoodFacts by barcode
    and add it to the inventory after confirming price and stock.
    """
    barcode = input("\nEnter barcode: ").strip()
    response = requests.get(f"{BASE_URL}/inventory/barcode/{barcode}")

    if response.status_code == 404:
        print(f"\nNo product found for barcode: {barcode}")
        return
    elif response.status_code != 200:
        print(f"\nError: {response.status_code}")
        return

    product = response.json()
    print("\nProduct found:")
    print_item(product)

    try:
        price = float(input("Set price: "))
        stock = int(input("Set stock quantity: "))
    except ValueError:
        print("Invalid price or stock.")
        return

    product["price"] = price
    product["stock"] = stock

    add_response = requests.post(f"{BASE_URL}/inventory", json=product)
    if add_response.status_code == 201:
        print("\nItem added to inventory!")
        print_item(add_response.json())
    else:
        print(f"\nError adding item: {add_response.json()}")


def search_by_name():
    """
    Search OpenFoodFacts by product name and optionally
    add a result to the inventory.
    """
    name = input("\nEnter product name to search: ").strip()
    response = requests.get(f"{BASE_URL}/inventory/search", params={"name": name})

    if response.status_code != 200:
        print(f"\nError: {response.status_code}")
        return

    products = response.json()
    if not products:
        print("\nNo products found.")
        return

    print(f"\nFound {len(products)} result(s):")
    for i, product in enumerate(products, 1):
        print(f"\n[{i}] {product['product_name']} — {product['brands']}")

    try:
        choice = int(input("\nEnter number to add to inventory (0 to cancel): "))
        if choice == 0:
            return
        selected = products[choice - 1]
    except (ValueError, IndexError):
        print("Invalid selection.")
        return

    try:
        price = float(input("Set price: "))
        stock = int(input("Set stock quantity: "))
    except ValueError:
        print("Invalid price or stock.")
        return

    selected["price"] = price
    selected["stock"] = stock

    add_response = requests.post(f"{BASE_URL}/inventory", json=selected)
    if add_response.status_code == 201:
        print("\nItem added to inventory!")
        print_item(add_response.json())
    else:
        print(f"\nError: {add_response.json()}")


def update_item():
    """Update price or stock of an existing inventory item."""
    try:
        item_id = int(input("\nEnter item ID to update: "))
    except ValueError:
        print("Invalid ID.")
        return

    print("What would you like to update?")
    print("1. Price")
    print("2. Stock")
    print("3. Both")
    choice = input("Choice: ").strip()

    payload = {}

    if choice in ("1", "3"):
        try:
            payload["price"] = float(input("New price: "))
        except ValueError:
            print("Invalid price.")
            return

    if choice in ("2", "3"):
        try:
            payload["stock"] = int(input("New stock: "))
        except ValueError:
            print("Invalid stock.")
            return

    if not payload:
        print("Nothing to update.")
        return

    response = requests.patch(f"{BASE_URL}/inventory/{item_id}", json=payload)
    if response.status_code == 200:
        print("\nItem updated successfully!")
        print_item(response.json())
    elif response.status_code == 404:
        print(f"\nItem with id {item_id} not found.")
    else:
        print(f"\nError: {response.json()}")


def delete_item():
    """Delete an inventory item by ID."""
    try:
        item_id = int(input("\nEnter item ID to delete: "))
    except ValueError:
        print("Invalid ID.")
        return

    confirm = (
        input(f"Are you sure you want to delete item {item_id}? (y/n): ")
        .strip()
        .lower()
    )
    if confirm != "y":
        print("Cancelled.")
        return

    response = requests.delete(f"{BASE_URL}/inventory/{item_id}")
    if response.status_code == 204:
        print(f"\nItem {item_id} deleted successfully.")
    elif response.status_code == 404:
        print(f"\nItem with id {item_id} not found.")
    else:
        print(f"\nError: {response.status_code}")


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------


def main():
    """Run the CLI application."""
    print("\nWelcome to the Inventory Management System!")
    print("Make sure the Flask server is running before proceeding.")

    actions = {
        "1": view_all,
        "2": view_single,
        "3": add_item_manually,
        "4": add_item_by_barcode,
        "5": search_by_name,
        "6": update_item,
        "7": delete_item,
    }

    while True:
        print_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "8":
            print("\nGoodbye!")
            break
        elif choice in actions:
            try:
                actions[choice]()
            except requests.exceptions.ConnectionError:
                print("\nError: Could not connect to the Flask server.")
                print("Make sure it is running with: flask run")
        else:
            print("\nInvalid choice. Please enter a number between 1 and 8.")


if __name__ == "__main__":
    main()
