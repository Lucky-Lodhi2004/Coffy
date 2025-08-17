# Coffy SQL CLI

`coffy-sql` is a simple, file-backed command-line interface for working with **Coffy’s SQL wrapper** around `sqlite3`.
It allows you to initialize databases, run SQL statements, export results, and view tables in your browser.

⚠️ **Note**: In-memory databases (`:memory:`) are not allowed in this CLI. You must provide a file path.

---

## Installation

After installing Coffy, the CLI is available as:

```bash
coffy-sql
```

This is provided via the `console_scripts` entry point.

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
