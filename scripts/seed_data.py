from sqlalchemy import select, insert, delete
import random
from datetime import datetime
from database.models import User, Product, Order
from database.db import SessionLocal

first_names_list = [
    "James", "Mary", "Robert", "Patricia", "John", "Jennifer", "Michael", "Linda", "David", "Elizabeth",
    "William", "Barbara", "Richard", "Susan", "Joseph", "Jessica", "Thomas", "Sarah", "Christopher", "Karen",
    "Charles", "Nancy", "Daniel", "Lisa", "Matthew", "Betty", "Anthony", "Margaret", "Mark", "Sandra",
    "Donald", "Ashley", "Steven", "Kimberly", "Paul", "Emily", "Andrew", "Donna", "Joshua", "Michelle",
    "Kenneth", "Dorothy", "Kevin", "Carol", "Brian", "Amanda", "George", "Melissa", "Edward", "Deborah",
    "Ronald", "Stephanie", "Timothy", "Rebecca", "Jason", "Sharon", "Jeffrey", "Laura", "Ryan", "Cynthia",
    "Jacob", "Kathleen", "Gary", "Amy", "Nicholas", "Shirley", "Eric", "Angela", "Jonathan", "Helen",
    "Stephen", "Anna", "Larry", "Brenda", "Justin", "Pamela", "Scott", "Nicole", "Brandon", "Emma",
    "Benjamin", "Samantha", "Samuel", "Katherine", "Gregory", "Christine", "Alexander", "Debra", "Frank", "Rachel",
    "Patrick", "Catherine", "Raymond", "Carolyn", "Jack", "Janet", "Dennis", "Virginia", "Jerry", "Heather"
]

second_names_list = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
    "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
    "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson",
    "Walker", "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores",
    "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell", "Carter", "Roberts",
    "Gomez", "Phillips", "Evans", "Turner", "Diaz", "Parker", "Cruz", "Edwards", "Collins", "Reyes",
    "Stewart", "Morris", "Morales", "Murphy", "Cook", "Rogers", "Gutierrez", "Ortiz", "Morgan", "Cooper",
    "Peterson", "Bailey", "Reed", "Kelly", "Howard", "Ramos", "Kim", "Cox", "Ward", "Richardson",
    "Watson", "Brooks", "Chavez", "Wood", "James", "Bennett", "Gray", "Mendoza", "Ruiz", "Hughes",
    "Price", "Alvarez", "Castillo", "Sanders", "Patel", "Myers", "Long", "Ross", "Foster", "Jimenez"
]

email_domains_list = [
    "gmail.com", "outlook.com", "icloud.com", "yahoo.com", "hotmail.com",
    "aol.com", "msn.com", "proton.me", "zoho.com", "mail.com"
]

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


def random_date(start_date, end_date):
    start_timestamp = int(datetime.strptime(start_date, '%Y-%m-%d').timestamp())
    end_timestamp = int(datetime.strptime(end_date, '%Y-%m-%d').timestamp())
    random_timestamp = random.randint(start_timestamp, end_timestamp)
    return datetime.fromtimestamp(random_timestamp)


def generate_user():
    first_name = random.choice(first_names_list)
    second_name = random.choice(second_names_list)
    email_domain = random.choice(email_domains_list)
    return {"name": f"{first_name} {second_name}", "email": f"{first_name.lower()}.{second_name.lower()}{random.randint(1, 999)}@{email_domain}"}

def generate_users(db):
    users = [generate_user() for _ in range(100)]
    db.execute(insert(User), users)
    db.commit()
    return len(users)


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


def generate_order(user_ids, products):
    min_date = '2023-01-01'
    max_date = '2024-12-31'

    user_id = random.choice(user_ids)[0]
    product_id, product_price = random.choice(products)
    quantity = random.randint(1, 5)
    total_price = round(quantity * product_price, 2)
    order_date = random_date(min_date, max_date)
    return {"user_id": user_id, "product_id": product_id, "quantity": quantity, "total_price": total_price, "order_date": order_date}


def generate_orders(db):
    users_select = select(User.id)
    user_ids = list(db.execute(users_select))

    products_select = select(Product.id, Product.price)
    products = list(db.execute(products_select))

    orders = [generate_order(user_ids, products) for _ in range(5000)]
    db.execute(insert(Order), orders)
    db.commit()
    return len(orders)


def clear_data(db):
    db.execute(delete(Order))
    db.execute(delete(Product))
    db.execute(delete(User))
    db.commit()

def main():
    with SessionLocal() as db:

        clear_data(db)

        user_cnt = generate_users(db)
        print(f"Users created: {user_cnt}")
        
        product_cnt = generate_products(db)
        print(f"Products created: {product_cnt}")
        
        order_cnt = generate_orders(db)
        print(f"Orders created: {order_cnt}")


if __name__ == "__main__":
    main()