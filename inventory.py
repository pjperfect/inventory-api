"""
In-memory inventory storage.

Simulates a database using a list of dictionaries.
Each item resembles the structure of an OpenFoodFacts product,
with an additional 'price' and 'stock' field for inventory purposes.
"""

# Simulated inventory database array
inventory = [
    {
        "id": 1,
        "product_name": "Organic Almond Milk",
        "brands": "Silk",
        "ingredients_text": "Filtered water, almonds, cane sugar, sea salt, sunflower lecithin",
        "quantity": "64 fl oz",
        "categories": "Plant-based milks, Beverages",
        "price": 4.99,
        "stock": 120
    },
    {
        "id": 2,
        "product_name": "Greek Yogurt",
        "brands": "Chobani",
        "ingredients_text": "Cultured nonfat milk, evaporated cane juice, fruit pectin",
        "quantity": "32 oz",
        "categories": "Dairy, Yogurts",
        "price": 6.49,
        "stock": 85
    },
    {
        "id": 3,
        "product_name": "Whole Grain Bread",
        "brands": "Dave's Killer Bread",
        "ingredients_text": "Whole wheat flour, water, cane sugar, oats, sunflower seeds",
        "quantity": "27 oz",
        "categories": "Breads, Bakery",
        "price": 5.99,
        "stock": 60
    },
    {
        "id": 4,
        "product_name": "Orange Juice",
        "brands": "Tropicana",
        "ingredients_text": "100% pure squeezed pasteurized orange juice",
        "quantity": "52 fl oz",
        "categories": "Juices, Beverages",
        "price": 3.99,
        "stock": 200
    },
    {
        "id": 5,
        "product_name": "Dark Chocolate Bar",
        "brands": "Lindt",
        "ingredients_text": "Chocolate, cocoa butter, vanilla extract, sugar",
        "quantity": "3.5 oz",
        "categories": "Chocolates, Snacks",
        "price": 2.99,
        "stock": 150
    },
]


def get_next_id():
    """Return the next available ID based on the current inventory."""
    if not inventory:
        return 1
    return max(item["id"] for item in inventory) + 1


def find_item(item_id):
    """Return the item with the given ID, or None if not found."""
    return next((item for item in inventory if item["id"] == item_id), None)