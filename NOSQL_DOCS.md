# 📘 Coffy NoSQL Database

A lightweight, embedded NoSQL database for Python. JSON-backed storage, fluent querying, and powerful filtering—all without a server.

Author: nsarathy

---

## 🛠️ Getting Started

```python
from coffy.nosql import db

users = db("users", path="users_data.json")
orders = db("orders", path="orders_data.json")
```

---

## 📦 Collection Methods

### `add(document: dict)`
Add a single document.
```python
users.add({"id": 1, "name": "Neel"})
```

---

### `add_many(docs: list[dict])`
Add multiple documents at once.
```python
users.add_many([{...}, {...}])
```

---

### `where(field: str)`
Start a query by targeting a field.
```python
users.where("email").eq("user@example.com").first()
```

---

### `match_any(*conditions)`
Match if **any** of the given conditions are true.
```python
orders.match_any(
    lambda q: q.where("status").eq("pending"),
    lambda q: q.where("total").gt(100)
)
```

---

### `match_all(*conditions)`
Match if **all** of the given conditions are true.
```python
orders.match_all(
    lambda q: q.where("status").ne("cancelled"),
    lambda q: q.where("total").gte(60)
)
```

---

### `not_any(*conditions)`
Negated OR condition — exclude if **any** condition is true.
```python
orders.not_any(
    lambda q: q.where("status").eq("cancelled"),
    lambda q: q.where("status").eq("pending")
)
```

---

### `lookup(foreign_collection_name, local_key, foreign_key, as_field)`
Join another collection on a key, similar to SQL `JOIN`.
```python
orders.lookup("users", local_key="user_id", foreign_key="id", as_field="user")
```

---

### `merge(fn)`
Enrich documents by merging additional fields computed from the joined data.
```python
.merge(lambda doc: {"customer": doc["user"]["name"]})
```

---

### `sum(field)`, `avg(field)`, `min(field)`, `max(field)`
Run aggregation functions on numeric fields.
```python
orders.sum("total")
orders.avg("total")
```

---

### `first()`
Return the first matched document or `None`.

---

### `count()`
Return count of matched documents.

---

### `all_docs()`, `all()`
Return all documents in the collection as a list.

---

### `clear()`
Deletes all documents in the collection.

---

### `export(path: str)`
Export current documents to a JSON file.

---

### `import_(path: str)`
Import documents from a JSON file, replacing current contents.

---

### `save(path: str)`
Save current state of documents to specified file (manual override).

---

## 🔎 Query Filters & Operators

After `.where(field)`, chain any of the following:

### Comparison

| Operator       | Description                           |
|----------------|---------------------------------------|
| `.eq(value)`   | Equals                                |
| `.ne(value)`   | Not equals                            |
| `.gt(value)`   | Greater than                          |
| `.gte(value)`  | Greater than or equal                 |
| `.lt(value)`   | Less than                             |
| `.lte(value)`  | Less than or equal                    |
| `.in_([...])`  | Value in list                         |
| `.nin([...])`  | Value not in list                     |
| `.matches(rx)` | Regex match on field as string        |
| `.exists()`    | Field exists in document              |

Example:
```python
orders.where("total").gt(100).count()
```

---

### Execution Methods

| Method          | Description                                 |
|------------------|---------------------------------------------|
| `.run()`         | Run query and return a `DocList`            |
| `.update({...})` | Update matched documents                    |
| `.delete()`      | Delete matched documents                    |
| `.replace({...})`| Replace matched documents entirely          |

---

### Aggregates on filtered results

```python
orders.where("status").eq("delivered").sum("total")
```

---

## 📄 DocList Object

Returned by `.run()`, it's an enhanced list of documents.

### `.as_list()`
Returns raw list of dicts.

---

### `.to_json(path: str)`
Save results as JSON.

---

### `__repr__()`
Pretty tabular printout of documents.

---

## 🔄 Example Workflow

```python
users = db("users", path="users_data.json")
orders = db("orders", path="orders_data.json")

# Clear all data
users.clear()
orders.clear()

# Add documents
users.add_many([
    {"id": 1, "name": "Neel"},
    {"id": 2, "name": "Tanaya"}
])

orders.add_many([
    {"order_id": 101, "user_id": 1, "total": 100},
    {"order_id": 102, "user_id": 2, "total": 200}
])

# Filter and join
result = (
    orders
    .lookup("users", local_key="user_id", foreign_key="id", as_field="user")
    .merge(lambda o: {"customer": o["user"]["name"]})
    .run()
)

print(result)
```

---

## 🧪 Testing Queries

```python
orders.where("total").gt(100).count()
users.where("email").matches(r".*@b.com").first()
orders.match_all(
    lambda q: q.where("total").gte(100),
    lambda q: q.where("status").ne("cancelled")
)
```

---

## 📂 File Storage

Each collection uses a separate `.json` file specified in `db(name, path="...")`. You can export, import, or inspect these directly.

---

## 🧼 Clean Design Principles

- Pure Python, no external dependencies.
- In-memory with optional disk persistence.
- Chainable DSL, optimized for readability.
- Suitable for CLI tools, prototyping, desktop apps.

---

## 🧱 Roadmap Ideas

- Indexing support
- Pagination `.limit()`, `.skip()`
- Schema validation
- TTL / expiring docs
- Built-in encryption (optional)