import random
from sqlalchemy import insert
from database.models import Product


products_data = [
    {
        "category": "Electronics",
        "products": [
            "Smartphone", "Laptop", "Wireless Headphones", "Smartwatch", "Tablet",
            "Bluetooth Speaker", "Digital Camera", "Gaming Console", "Monitor", "Power Bank"
        ],
        "min_price": 100.0,
        "max_price": 2000.0
    },
    {
        "category": "Books",
        "products": [
            "Mystery Novel", "Science Fiction Anthology", "Self-Help Guide", "Historical Biography", "Cookbook",
            "Fantasy Epic", "Financial Literacy Book", "Children's Picture Book", "Travel Memoir", "Poetry Collection"
        ],
        "min_price": 10.0,
        "max_price": 50.0
    },
    {
        "category": "Clothing",
        "products": [
            "Cotton T-Shirt", "Denim Jeans", "Hooded Sweatshirt", "Summer Dress", "Leather Jacket",
            "Running Shorts", "Formal Shirt", "Wool Sweater", "Cargo Pants", "Socks (6-pack)"
        ],
        "min_price": 20.0,
        "max_price": 200.0
    },
    {
        "category": "Home & Kitchen",
        "products": [
            "Air Fryer", "Coffee Maker", "Non-stick Frying Pan", "Blender", "Toaster Oven",
            "Electric Kettle", "Vacuum Cleaner", "Knife Set", "Storage Containers", "Bedding Set"
        ],
        "min_price": 30.0,
        "max_price": 500.0
    },
    {
        "category": "Sports",
        "products": [
            "Yoga Mat", "Dumbbell Set", "Basketball", "Running Shoes", "Tennis Racket",
            "Resistance Bands", "Water Bottle", "Bicycle Helmet", "Soccer Ball", "Hiking Backpack"
        ],
        "min_price": 20.0,
        "max_price": 300.0
    }
]

def generate_product():
    
    category_data = random.choice(products_data)
    product_name = random.choice(category_data["products"])
    price = round(random.uniform(category_data["min_price"], category_data["max_price"]), 2)
    return {"name": product_name, "category": category_data["category"], "price": price}


def generate_products(db):
    products = [generate_product() for _ in range(50)]
    db.execute(insert(Product), products)
    db.commit()
    return len(products)