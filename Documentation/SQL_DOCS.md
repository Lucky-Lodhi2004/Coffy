# 📘 Coffy SQL Database

A lightweight SQL database wrapper around SQLite with zero dependencies. Load, query, and persist relational data using standard SQL syntax via a minimal Python API.

Author: nsarathy

---

## 🛠️ Getting Started

### Initialization

You can use an **in-memory database** (default) or **load/save from disk** by specifying a path:

```python
from coffy.sql import init, query

# In-memory database (default)
init()

# OR persistent database file
init("my_database.sqlite")
```

---

## 🔍 Executing Queries

Once initialized, you can use standard SQL queries to interact with the database:

```python
# Create a table
query("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)")

# Insert data
query("INSERT INTO users (id, name, email) VALUES (1, 'Neel', 'neel@a.com')")

# Query data
result = query("SELECT * FROM users")
print(result)
```

> 💡 You can run **any valid SQLite query** — DDL, DML, joins, aggregates, etc.  
> No need to learn a custom query language.

---

## 📄 SQLDict Result Object

Queries that return rows (e.g. `SELECT`) return a `SQLDict` object — a list-like, enhanced wrapper.

### Key Features

#### `__repr__()`
Pretty tabular output in console.

#### `.as_list()`
Returns raw list of dictionaries:
```python
rows = result.as_list()
```

#### `.to_csv(path: str)`
Save result as CSV:
```python
result.to_csv("output.csv")
```

#### `.to_json(path: str)`
Save result as JSON:
```python
result.to_json("output.json")
```

---

## 🧪 Example Workflow

```python
from coffy.sql import init, query

# Initialize database
init("users.sqlite")

# Create and populate
query("CREATE TABLE users (id INTEGER, name TEXT)")
query("INSERT INTO users VALUES (1, 'Neel')")
query("INSERT INTO users VALUES (2, 'Tanaya')")

# Run SQL query
result = query("SELECT * FROM users WHERE id > 1")

# Display as table
print(result)

# Export to JSON
result.to_json("filtered_users.json")
```

---

## 🗃️ Persistence

- If you call `init()` with a path, the database is persisted to disk.
- If no path is passed, a temporary in-memory SQLite database is used.
- You can copy the `.sqlite` file manually or reuse it by re-initializing with the same path.

---

## 🧼 Design Principles

- Full power of SQLite via simple wrapper
- No ORMs, no boilerplate, just raw SQL
- Tabular result formatting for easy reading
- Minimal API surface

---