# coffy
Local Embedded DBMS (python)
---

## 📦 `coffy.sql` – Embedded SQL Engine (SQLite)

### Overview

The `coffy.sql` module is a lightweight, embedded SQL execution engine powered by SQLite. It is designed for local development environments and supports standard SQL queries, table creation, insertion, selection, and data export.

It features a custom result wrapper `SQLDict` for easy access, pretty-printing, and file export.

---

### 🔧 Initialization

```python
import coffy.sql as sql

sql.init()               # Uses in-memory DB
sql.init("mydb.sqlite")  # Optional: specify path for persistent DB
```

If no path is given, it defaults to an in-memory SQLite database.

---

### ▶️ Executing Queries

```python
sql.query("CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT);")
sql.query("INSERT INTO test (name) VALUES ('Alice'), ('Bob');")
result = sql.query("SELECT * FROM test;")
```

* Queries are automatically committed if they modify data.
* If the query is a `SELECT`, a `SQLDict` object is returned.

---

### 📄 `SQLDict` – Query Result Wrapper

When a `SELECT` query is executed, the result is returned as a `SQLDict` object:

```python
print(result)
print(result.as_list())     # Access as list of dicts
result.to_csv("out.csv")    # Export to CSV
result.to_json("out.json")  # Export to JSON
```

Pretty-printed table output is shown when printed directly.

---

### 💡 Example

```python
import coffy.sql as sql

sql.query("""
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        price REAL
    );
""")

sql.query("""
    INSERT INTO products (name, price) VALUES
    ('Coffee Mug', 12.99),
    ('Wireless Mouse', 24.50),
    ('Notebook', 3.25),
    ('Bluetooth Speaker', 45.00),
    ('Mechanical Keyboard', 85.75);
""")

result = sql.query("SELECT * FROM products WHERE price > 20;")
print(result)
result.to_csv("products.csv")
result.to_json("products.json")
```

---

### 🔍 Internals

* Uses `sqlite3` under the hood.
* Connection is initialized once via `init()` or automatically on first query.
* Error handling is included; non-`SELECT` queries return status and affected row count.

---
