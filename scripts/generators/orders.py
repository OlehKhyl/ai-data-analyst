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

def random_date(start_date, end_date):

    start_timestamp = int(datetime.strptime(start_date, '%Y-%m-%d').timestamp())
    end_timestamp = int(datetime.strptime(end_date, '%Y-%m-%d').timestamp())
    rand_date = None

    for _ in range(100):
        rand_date = datetime.fromtimestamp(random.randint(start_timestamp, end_timestamp))
        if random.random() < MONTH_WEIGHTS.get(rand_date.month) / MAX_MONTH_WEIGHT:
            break

    return rand_date

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

def random_product_weighted(products):
    
    random_product = None

    for _ in range(100):
        random_product = random.choice(products)
        if random.random() < PRODUCT_CATEGORIES_WEIGHTS.get(random_product[2]) / MAX_PRODUCT_CATEGORY_WEIGHT:
            break

    return random_product
    


def generate_order(user_ids, products):
    min_date = '2023-01-01'
    max_date = '2024-12-31'

    user_id = random.choice(user_ids)[0]
    order_date = random_date(min_date, max_date)
    product_id, product_price, product_category = random_product_weighted(products)
    quantity = round(random.randint(1, 5) * get_seasonal_multiplier(product_category, order_date))
    total_price = round(quantity * product_price, 2)
    return {"user_id": user_id, "product_id": product_id, "quantity": quantity, "total_price": total_price, "order_date": order_date}


def generate_orders(db):
    users_select = select(User.id)
    user_ids = list(db.execute(users_select))

    products_select = select(Product.id, Product.price, Product.category)
    products = list(db.execute(products_select))

    orders = [generate_order(user_ids, products) for _ in range(5000)]
    db.execute(insert(Order), orders)
    db.commit()
    return len(orders)
