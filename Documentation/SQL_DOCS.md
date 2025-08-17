# coffy.sql

A tiny, zero‑dependency wrapper around `sqlite3` that gives you:
* one‑liner database **initialise/query/close** calls  
* a **`SQLDict`** result object with pretty `print`, HTML viewing, and CSV / JSON export  
* sensible defaults (in‑memory DB if you don’t specify a path)
* a minimal **ORM** with declarative models, query building, bulk insert, and SQL injection protections

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
- [ORM Documentation](#coffy-sql-orm-documentation)
    - [Overview](#overview)
    - [Key Components](#key-components)
        - [Fields](#fields)
        - [Model](#model)
        - [Manager](#manager)
        - [Query Builder](#query-builder)
        - [Raw Queries](#raw-queries)
    - [Protections Against SQL Injection](#protections-against-sql-injection)
    - [Example End-to-End](#example-end-to-end)
    - [Summary](#summary)

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

---

## `coffy.sql` ORM Documentation

### Overview

Coffy’s SQL ORM is a lightweight object-relational mapper built on top of SQLite.  
It offers a clean, Pythonic interface for defining models, creating tables, performing CRUD operations, building queries, and running raw SQL.

The ORM is minimal but expressive, with built-in protections against SQL injection via identifier validation and value parameterization.

---

### Key Components

#### Fields

Field classes define table columns and constraints.  
They are declared as class attributes inside `Model` subclasses.

Available field types:
- `Integer`
- `Real`
- `Text`
- `Blob`

Each accepts optional arguments:
- `primary_key` (bool)
- `nullable` (bool)
- `default` (any)

Example:
```python
class User(Model):
    id = Integer(primary_key=True, nullable=False)
    name = Text(nullable=False)
    age = Integer(default=18)
```

---

#### Model

A `Model` represents a database table.  
Its metaclass (`ModelMeta`) automatically collects `Field` definitions and metadata.

Special attributes:
- `__tablename__` (optional) – override the table name
- `objects` – a `Manager` instance for CRUD and queries

Example:
```python
class Product(Model):
    __tablename__ = "products"
    id = Integer(primary_key=True, nullable=False)
    name = Text(nullable=False, default="unknown")
    price = Real(nullable=False)
```

---

#### Manager

`Manager` provides table-level operations:

- `create_table(if_not_exists=True)` – create table with fields
- `drop_table(if_exists=True)` – drop table
- `insert(**values)` – insert one row
- `bulk_insert(rows)` – insert many rows, respecting defaults for omitted fields
- `update(where, **values)` – update matching rows
- `delete(where)` – delete matching rows
- `get(**eq_filters)` – retrieve a single row by equality filters
- `query()` – create a `Query` object

Example:
```python
User.objects.insert(id=1, name="Alice")
User.objects.update([("id", "=", 1)], name="Alicia")
User.objects.delete([("id", "=", 1)])
```

---

#### Query Builder

The `Query` class allows constructing SELECT queries fluently.

Methods:
- `select(*cols)` – columns to retrieve
- `where(cond)` – WHERE conditions (supports nested AND/OR)
- `order_by(*cols)` – ORDER BY clause
- `limit(n, offset=None)` – LIMIT/OFFSET
- `join(other_table, on, kind="INNER")` – JOINs with validation
- `group_by(*cols)` – GROUP BY
- `having(cond)` – HAVING
- `with_cte(name, sql, params=None, recursive=False)` – Common Table Expressions
- `all()` – execute and return results as `SQLDict`
- `first()` – return first result or `None`
- `aggregate(**agg)` – shortcut for aggregates

Condition format:
```python
[("age", ">", 21), ("city", "IS NOT", None)]
(("name", "=", "Alice"), "OR", ("name", "=", "Bob"))
```

Example:
```python
q = User.objects.query()     .select("id", "name")     .where([("age", ">", 21), ("city", "IS NOT", None)])     .order_by("id ASC")     .limit(5)

rows = q.all().as_list()
```

---

#### Raw Queries

For advanced use cases, execute raw SQL:
```python
from coffy.sql import raw
res = raw("SELECT COUNT(*) AS c FROM users WHERE age > ?", [25])
print(res[0]["c"])
```

`raw()` returns an `SQLDict`, which supports:
- index access (`res[0]`)
- iteration
- `.as_list()` – list of dicts

---

### Protections Against SQL Injection

- **Identifier validation** – `_quote_ident()` ensures identifiers contain only alphanumerics and underscores, optionally qualified with a dot (`table.column`).
- **Parameterized queries** – all values are bound via `?` placeholders.
- **Join ON validation** – token parsing ensures join conditions do not contain unsafe syntax.

---

### Example End-to-End

```python
from coffy.sql import init, close, Model, Integer, Text, raw

init(":memory:")

class User(Model):
    id = Integer(primary_key=True, nullable=False)
    name = Text(nullable=False)
    age = Integer()

User.objects.create_table()
User.objects.bulk_insert([
    {"id": 1, "name": "Alice", "age": 30},
    {"id": 2, "name": "Bob", "age": 25}
])

res = User.objects.query()     .select("name")     .where(("age", ">", 26))     .all()

print(res.as_list())  # [{'name': 'Alice'}]

close()
```

---

### Summary

Coffy SQL ORM is a lightweight, explicit, and secure ORM for SQLite.  
It offers:
- Declarative model definitions
- Clean query building
- Bulk insert with defaults
- Aggregations and grouping
- Safe raw SQL execution

This makes it ideal for small to medium-sized projects, educational purposes, and embedded database applications.


# SQL CLI

## CLI Table of Contents
- [CLI Availability](#cli-availability)
- [Usage](#usage)
    - [Commands](#commands)
- [Examples](#examples)

`coffy-sql` is a simple, file-backed command-line interface for working with **Coffy’s SQL wrapper** around `sqlite3`.
It allows you to initialize databases, run SQL statements, export results, and view tables in your browser.

⚠️ **Note**: In-memory databases (`:memory:`) are not allowed in this CLI. You must provide a file path.

---

## CLI Availability

After installing Coffy, the CLI is available as:

```bash
coffy-sql
```

---

## Usage

```bash
coffy-sql --db PATH COMMAND [options...]
```

* `--db PATH` (required): Path to SQLite database file. Will be created if missing.
  *Must be a file, not `:memory:`.*

### Commands

#### `init`

Create or open a database file.

```bash
coffy-sql --db ./users.sqlite init
```

---

#### `run`

Execute one or more SQL statements.

```bash
coffy-sql --db ./users.sqlite run "SQL"
```

Options:

* `SQL`: A SQL string or `@path/to/file.sql` to load statements from a file.
* `--json`: Output SELECT results as JSON to stdout.
* `--pretty`: Pretty-print JSON output.
* `--out PATH`: If the last statement is a SELECT, export to `.json` or `.csv`.

Examples:

```bash
# Single statement
coffy-sql --db ./users.sqlite run "SELECT * FROM users"

# Multiple statements
coffy-sql --db ./users.sqlite run "CREATE TABLE u(id INT); INSERT INTO u VALUES(1); SELECT * FROM u" --out u.csv

# Run from file
coffy-sql --db ./users.sqlite run @init.sql --json --pretty
```

---

#### `export`

Run a single SELECT query and export results.

```bash
coffy-sql --db ./users.sqlite export "SELECT * FROM users" --out users.json
```

Options:

* `--out PATH`: Must end with `.json` or `.csv`.

---

#### `view`

Run a SELECT query and open the result in your default browser.

```bash
coffy-sql --db ./users.sqlite view "SELECT * FROM users"
```

Options:

* `--title TITLE`: Browser tab title (default: *SQL Query Results*).

---

## Examples

### Initialize and insert data

```bash
coffy-sql --db ./users.sqlite init
coffy-sql --db ./users.sqlite run "CREATE TABLE users(id INT, name TEXT)"
coffy-sql --db ./users.sqlite run "INSERT INTO users VALUES (1,'Neel'); INSERT INTO users VALUES (2,'Tanaya')"
```

### Query as table

```bash
coffy-sql --db ./users.sqlite run "SELECT * FROM users"
```

Output:

```
+----+--------+
| id | name   |
+----+--------+
| 1  | Neel   |
| 2  | Tanaya |
+----+--------+
```

### Export as JSON

```bash
coffy-sql --db ./users.sqlite export "SELECT * FROM users" --out users.json
```

### Export as CSV

```bash
coffy-sql --db ./users.sqlite export "SELECT * FROM users" --out users.csv
```

### View in browser

```bash
coffy-sql --db ./users.sqlite view "SELECT * FROM users"
```

