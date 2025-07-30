# Coffy SQL CLI

A command-line interface (CLI) for interacting with the Coffy SQL engine.

## Installation
Ensure you have `coffy` installed and accessible in your environment.

```bash
pip install -e .
```

This will install the `coffy-sql` CLI (or `python -m coffy.cli.sql_cli` if running locally).

---

## Commands

### 1. `init`
Initialize the SQL engine.

#### Usage
```bash
coffy-sql init [--db <path>]
```

#### Options
| Option    | Description                          |
|-----------|--------------------------------------|
| `--db`    | Path to SQLite database file. If not provided, an in-memory database is used. |

#### Example
```bash
coffy-sql init --db my_database.db
```
Output:
```
Initialized SQL engine with db: my_database.db
```

---

### 2. `run`
Execute a SQL query.

#### Usage
```bash
coffy-sql run "<SQL QUERY>"
```

#### Description
- If the query is a `SELECT`, results will be displayed in the terminal.
- For non-SELECT queries (e.g., `CREATE`, `INSERT`), a success message is displayed.

#### Example
```bash
coffy-sql run "CREATE TABLE users (id INTEGER, name TEXT)"
coffy-sql run "INSERT INTO users VALUES (1, 'Alice')"
coffy-sql run "SELECT * FROM users"
```
Output:
```
id | name
---+-------
1  | Alice
```

---

### 3. `view`
Execute a SQL `SELECT` query and view the results in the browser.

#### Usage
```bash
coffy-sql view "<SELECT QUERY>"
```

#### Example
```bash
coffy-sql view "SELECT * FROM users"
```
This opens a browser window with an interactive HTML table.

If the query is not a `SELECT`, you will see:
```
Not a SELECT query.
```

---

### 4. `close`
Close the database connection.

#### Usage
```bash
coffy-sql close
```

#### Example
```bash
coffy-sql close
```
Output:
```
Closed SQL engine connection.
```

---

## Notes
- The CLI uses SQLite as the backend.
- If no database is initialized, `init` will create an in-memory database.
- Use `view` for visualizing large query results in a browser.

---

## Development
To run tests:
```bash
python -m unittest discover tests
```
