from sqlalchemy import delete
from database.models import User, Product, Order
from database.db import SessionLocal
from scripts.generators.users import generate_user, generate_users
from scripts.generators.products import generate_product, generate_products
from scripts.generators.orders import generate_order, generate_orders

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