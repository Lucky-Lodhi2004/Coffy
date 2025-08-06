# coffy.sql

A tiny, zero‑dependency wrapper around `sqlite3` that gives you:
* one‑liner database **initialise/query/close** calls  
* a **`SQLDict`** result object with pretty `print`, HTML viewing, and CSV / JSON export  
* sensible defaults (in‑memory DB if you don’t specify a path)

---

## Table of Contents
- [Quick‑start](#quick-start)
- [Public API](#public-api)
    - [`init(path: str | None = None)`](#initpath-str--none--none-)
    - [`query(sql: str)`](#querysql-str)
    - [`close()`](#close)
- [`SQLDict`](#sqldict--result-wrapper)
    - [`__repr__()`](#__repr__)
    - [`as_list()`](#as_list)
    - [`to_csv(path)`](#to_csvpath)
    - [`to_json(path)`](#to_jsonpath)
    - [`view(title: str = "SQL Query Results")`](#viewtitle-str---sql-query-results-)
- [Usage Examples](#usage-examples)

---

## Quick‑start

```python
from coffy.sql import init, query

init("users.sqlite")                      # create / open DB
query("CREATE TABLE users (id INT, name TEXT)")
query("INSERT INTO users VALUES (1, 'Neel')")
result = query("SELECT * FROM users")
print(result)                             # pretty table in your terminal
result.to_json("users.json")              # export
```
> You can run any valid SQLite statement with `query(...)`.
---

## Public API

### `init(path: str | None = None)`
Open (or create) an SQLite database.  
*If `path` is `None`, an in‑memory DB is used.*

### `query(sql: str)`
Run any SQL statement.  
*Returns*  
- **`SQLDict`** for `SELECT` queries  
- `{"status": "success", "rows_affected": n}` for mutating queries  

### `close()`
Closes the current connection & cursor. Safe to call multiple times.

---

## `SQLDict` – Result Wrapper

### `__repr__()`
Pretty‑prints the result set as an ASCII table when you `print(result)` or inspect it in a REPL.

### `as_list()`
Returns the raw data as `List[Dict[str, Any]]`.

### `to_csv(path)`
Writes the result to a CSV file at *path*.

### `to_json(path)`
Writes the result to a JSON file at *path* (pretty‑printed).

### `view(title: str = "SQL Query Results")`
Launches your default browser with an HTML table for interactive viewing.

![Example](https://github.com/nsarathy/Coffy/blob/main/assets/sqlviz.png)

---

## Usage Examples

**Example 1**

```python
# Initialize database
init("users.sqlite")

# Create & populate
query("CREATE TABLE users (id INTEGER, name TEXT)")
query("INSERT INTO users VALUES (1, 'Neel')")
query("INSERT INTO users VALUES (2, 'Tanaya')")

# Filter
result = query("SELECT * FROM users WHERE id > 1")
print(result)              # tabular view
result.to_json("filtered_users.json")
```

**Example 2**

```python
from coffy.sql import init, query, close

init(r"C:\Users\neel3\Everything\Coffy\test_data\sql.db")

query("DELETE FROM users")  # clear
query("""CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER,
    occupation TEXT,
    city TEXT
)""")
query("INSERT INTO users (name, age, occupation, city) VALUES ('Alice', 30, 'Wonderland', 'Wonderland')")
query("INSERT INTO users (name, age, occupation) VALUES ('Bob', 25, 'Engineer')")
query("INSERT INTO users (name, age, occupation, city) VALUES ('Charlie', 35, 'Electrician', 'New York')")

print(query("SELECT * FROM users"))
close()
```
