import coffy.sql as sql

query1 = """
    CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    price REAL
    );
"""
query2 = """
    INSERT INTO products (name, price) VALUES
    ('Coffee Mug', 12.99),
    ('Wireless Mouse', 24.50),
    ('Notebook', 3.25),
    ('Bluetooth Speaker', 45.00),
    ('Mechanical Keyboard', 85.75);
"""
query3 = "SELECT * FROM products WHERE price > 20;"

sql.query(query1)  # Create table
sql.query(query2)  # Insert data
result = sql.query(query3)  # Select data
print(result)
print(result.as_list())  # Convert to list
result.to_csv("products.csv")  # Export to CSV
result.to_json("products.json")  # Export to JSON