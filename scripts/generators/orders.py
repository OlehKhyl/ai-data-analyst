from sqlalchemy import select, insert
import random
from datetime import datetime
from database.models import User, Product, Order

MONTH_WEIGHTS = {
    1: 0.6,
    2: 0.7,
    3: 0.9,
    4: 1.0,
    5: 1.1,
    6: 1.2,
    7: 1.25,
    8: 1.15,
    9: 1.0,
    10: 1.1,
    11: 1.8,
    12: 2.0
    }

MAX_MONTH_WEIGHT = max(MONTH_WEIGHTS.values())

PRODUCT_CATEGORIES_WEIGHTS = {
        "Electronics": 0.3,
        "Books": 0.25,
        "Clothing": 0.2,
        "Home & Kitchen": 0.15,
        "Sports": 0.1
    }

MAX_PRODUCT_CATEGORY_WEIGHT = max(PRODUCT_CATEGORIES_WEIGHTS.values())

MIN_DATE = datetime(2023,1,1)
MAX_DATE = datetime(2024,12,31)

def random_date(start_date, end_date):

    start_timestamp = int(start_date.timestamp())
    end_timestamp = int(end_date.timestamp())
    rand_date = None

    for _ in range(10):
        rand_date = datetime.fromtimestamp(random.randint(start_timestamp, end_timestamp))
        if random.random() < MONTH_WEIGHTS.get(rand_date.month) / MAX_MONTH_WEIGHT:
            break

    return rand_date


def random_product_weighted(products):
    
    random_product = None

    for _ in range(100):
        random_product = random.choice(products)
        if random.random() < PRODUCT_CATEGORIES_WEIGHTS.get(random_product["category"]) / MAX_PRODUCT_CATEGORY_WEIGHT:
            break

    return random_product

    
def get_seasonal_multiplier(category, order_date):
    month = order_date.month
    if category == "Electronics":
        return 1.5 if month in [11, 12] else 1.0
    elif category == "Books":
        return 1.2 if month in [6, 7, 8] else 1.0
    elif category == "Clothing":
        return 1.3 if month in [3, 4, 5] else 1.0
    elif category == "Home & Kitchen":
        return 1.4 if month in [9, 10] else 1.0
    elif category == "Sports":
        return 1.2 if month in [4, 5, 6] else 1.0
    return 1.0


def generate_order(user_ids, products):

    user_id = random.choice(user_ids)
    order_date = random_date(MIN_DATE, MAX_DATE)
    product = random_product_weighted(products)
    product_id = product["id"]
    product_price = product["price"]
    product_category = product["category"]
    quantity = max(1, round(random.randint(1, 5) * get_seasonal_multiplier(product_category, order_date)))
    total_price = round(quantity * product_price, 2)
    return {"user_id": user_id, "product_id": product_id, "quantity": quantity, "total_price": total_price, "order_date": order_date}


def generate_orders(db):
    users_select = select(User.id)
    user_ids = [row[0] for row in db.execute(users_select)]

    products_select = select(Product.id, Product.price, Product.category)
    products = [
                {"id": row[0], "price": row[1], "category": row[2]}
                for row in db.execute(products_select)
                ]

    orders = [generate_order(user_ids, products) for _ in range(5000)]
    db.execute(insert(Order), orders)
    db.commit()
    return len(orders)
