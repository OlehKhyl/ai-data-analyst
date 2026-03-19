DATABASE_SCHEMA = {
    "users": {
        "description": "Table to store user information",
        "columns": {
            "id": {"type": "Integer",
                   "primary_key": True},
            "name": {"type": "String"},
            "email": {"type": "String"},
        }
    },

    "products": {
        "description": "Table to store product information",
        "columns": {
            "id": {"type": "Integer"},
            "name": {"type": "String"},
            "category": {"type": "String"},
            "price": {"type": "Float"}
        }
    },

    "orders": {
        "description": "Table to store order information",
        "columns": {
            "id": {"type": "Integer",
                   "primary_key": True},
            "user_id": {"type": "Integer",
                    "foreign_key": "users.id"},
        "product_id": {"type": "Integer",
                       "foreign_key": "products.id"},
        "quantity": {"type": "Integer"},
        "total_price": {"type": "Float"},
        "order_date": {"type": "Date"}
        
        }
    }
}

def get_schema_prompt():

    prompt = "The database schema:\n"

    for table_name, table_info in DATABASE_SCHEMA.items():

        table_description = table_info["description"]
        prompt += f"\nTable: {table_name}\nDescription: {table_description}"

        for column_name in table_info["columns"]:
            
            column_info = table_info["columns"][column_name]
            column_type = column_info["type"]
            primary_key = column_info.get("primary_key")
            foreign_key = column_info.get("foreign_key")
            prompt += f"\n  - {column_name} ({column_type})"
            if primary_key:
                prompt += " (Primary Key)"
            if foreign_key:
                prompt += f" (Foreign Key: {foreign_key})"
        
        prompt += "\n"

    return prompt


def get_all_tables_names():
    return list(DATABASE_SCHEMA.keys())

def get_all_columns_names():
    columns = []
    for table_name, table_info in DATABASE_SCHEMA.items():
        columns.extend(list(table_info["columns"].keys()))
    return columns