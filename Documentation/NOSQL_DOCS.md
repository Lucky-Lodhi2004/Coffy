# Coffy NoSQL Engine

- Embedded NoSQL document store with a fluent, chainable query API
- Supports nested fields, logical filters, aggregations, projections, and joins
- Built for local usage with optional persistence; minimal setup, fast iteration

> Scope: local, single-process, small datasets. No indexes, no transactions. Designed for clarity and fast iteration.

---
## Table of Contents

- [Quick Start](#quick-start)
- [Data Model & Persistence](#data-model--persistence)
- [Start Here](#start-here)
- [CollectionManager](#collectionmanager)
    - [Constructor](#constructor)
    - [Insertion](#insertion)
    - [Query entrypoints](#query-entrypoints)
    - [Aggregations (collection-level helpers)](#aggregations-collection-level-helpers)
    - [Maintenance & IO](#maintenance--io)
    - [Visualization](#visualization)
- [QueryBuilder](#querybuilder)
    - [Field selection](#field-selection)
    - [Comparison operators](#comparison-operators)
    - [Logic grouping](#logic-grouping)
    - [Execution](#execution)
    - [Mutation](#mutation)
    - [Aggregations (query-scoped)](#aggregations-query-scoped)
    - [Lookup (one-to-one join) and Merge](#lookup-one-to-one-join-and-merge)
    - [Pagination](#pagination)
- [DocList](#doclist)
- [Error Handling](#error-handling)
- [Performance & Limits](#performance--limits)
- [Example: end-to-end](#example-end-to-end)

---
## Quick Start

```python
from coffy.nosql import db

users = db("users", path="data/users.json")
users.clear()  # start clean for this demo

users.add_many([
    {"id": 1, "name": "Neel", "email": "neel@a.com", "age": 30, "address": {"city": "Indy"}},
    {"id": 2, "name": "Bea",  "email": "bea@b.com",  "age": 25, "address": {"city": "Austin"}},
    {"id": 3, "name": "Carl", "email": "carl@c.com", "age": 40},
])

# Basic equality
q = users.where("name").eq("Neel")
print(q.first())
# -> {'id': 1, 'name': 'Neel', ...}

# Nested field access
q = users.where("address.city").eq("Austin")
print(q.count())
# -> 1

# Projection
print(q.run(fields=["id", "address.city"]).as_list())
# -> [{'id': 2, 'address.city': 'Austin'}]
```

---

## Data Model & Persistence

- A **collection** stores a list of **documents** (plain `dict`s).
- Documents can have **different fields**.
- Use `path="file.json"` for durable persistence; omitted or invalid path means in-memory only.
- JSON on disk is pretty-printed and human-readable.

Example on disk:

```json
[
  {"id": 1, "name": "Neel", "age": 30},
  {"id": 2, "name": "Bea", "age": 25}
]
```

---

## Start Here

### CollectionManager

#### Constructor
```python
CollectionManager(name: str, path: str | None = None)
```

- name -- the collection name
- path -- optional path to a JSON file for persistence; if `None` or `:memory:`, in-memory only


#### Insertion

```python
add(document: dict) -> {"inserted": 1}
add_many(docs: list[dict]) -> {"inserted": N}
```

**Examples**
```python
users.add({"id": 4, "name": "Drew"})
users.add_many([{"id": 5}, {"id": 6, "active": True}])
```

#### Query entrypoints

```python
where(field: str) -> QueryBuilder
match_any(*builders) -> QueryBuilder   # OR across sub-queries
match_all(*builders) -> QueryBuilder   # AND across sub-queries
not_any(*builders)  -> QueryBuilder    # NOT( OR(sub-queries) )
```

**Examples**
```python
# where + eq
users.where("name").eq("Neel").first()

# match_any
users.match_any(
    lambda q: q.where("age").gt(35),
    lambda q: q.where("name").eq("Bea")
).run().as_list()

# match_all
users.match_all(
    lambda q: q.where("age").gte(25),
    lambda q: q.where("age").lt(40)
).count()

# not_any
users.not_any(
    lambda q: q.where("name").eq("Neel"),
    lambda q: q.where("age").eq(40)
).run().as_list()
```

#### Aggregations (collection-level helpers)

```python
sum(field: str) -> number
avg(field: str) -> float
min(field: str) -> number | None
max(field: str) -> number | None
count() -> int
first() -> dict | None
```

**Examples**
```python
users.sum("age")      # 95
users.avg("age")      # 31.66...
users.min("age")      # 25
users.max("age")      # 40
users.count()         # 3
users.first()         # first document in the collection
```

#### Maintenance & IO

```python
clear() -> {"cleared": N}
export(path: str) -> None
import_(path: str) -> None
save(path: str) -> None
all() -> list[dict]
all_docs() -> list[dict]
```

**Examples**
```python
users.export("backup/users_export.json")
users.clear()
users.import_("backup/users_export.json")
```

---

#### Visualization

You can visualize your collections using the built-in view function.
```python
view() -> None
```

**Example**
```python
users.view()
```

![NoSQL Visualization](https://github.com/nsarathy/Coffy/blob/main/assets/nosqlviz.png)

---

### QueryBuilder

You get a `QueryBuilder` from a collection via `where`, `match_any`, `match_all`, or `not_any`.

#### Field selection

```python
where(field: str) -> QueryBuilder
```

Supports **dot-notation** for nested fields.

**Examples**
```python
users.where("name").eq("Neel")
users.where("address.city").eq("Indy")
users.where("profile.stats.score").gte(9000)
```

#### Comparison operators

```python
eq(value)
ne(value)
gt(value)     # numeric
gte(value)
lt(value)
lte(value)
between(a, b)  # numeric range inclusive
in_(values: list)
nin(values: list)
matches(regex: str)   # regex on string value
exists()
```

**Examples**
```python
# equality
users.where("name").eq("Neel").count()

# numeric ranges
users.where("age").gte(25).where("age").lt(40).run()

# membership
users.where("name").in_(["Neel", "Bea"]).run()

# regex
users.where("email").matches(r"@a\.com$").run()

# existence (nested ok)
users.where("address.city").exists().run()
```

#### Logic grouping

```python
_and(*builders)   # all sub-queries must match
_or(*builders)    # any sub-query matches
_not(*builders)   # negates the AND of each sub-query
```

**Examples**
```python
# _and
q = users.where("age").gte(25)
q._and(lambda s: s.where("name").ne("Carl"))
q.run().as_list()

# _or with two branches
q = users._and(  # seed with no filters, then group
    lambda s: s.where("age").gt(35),
    lambda s: s.where("name").eq("Bea")
)

# Equivalent with collection helpers:
users.match_any(
    lambda s: s.where("age").gt(35),
    lambda s: s.where("name").eq("Bea")
).run().as_list()

# _not – exclude anyone under 30
users.where("age").lt(30)        # build the inner condition
# negate using collection helper
users.not_any(lambda s: s.where("age").lt(30)).run().as_list()
```

#### Execution

```python
run(fields: list[str] | None = None) -> DocList
count() -> int
first() -> dict | None
distinct(field: str) -> list[...]
```

`run(fields=[...])` performs **projection**. Fields can be nested (`"a.b.c"`). Returned keys are the field names you requested.

**Examples**
```python
users.where("age").gte(25).run(fields=["id", "name"]).as_list()
# -> [{'id': 1, 'name': 'Neel'}, {'id': 2, 'name': 'Bea'}, ...]

users.where("address.city").exists().run(fields=["id", "address.city"]).as_list()
# -> [{'id': 1, 'address.city': 'Indy'}, {'id': 2, 'address.city': 'Austin'}]

users.where("address.city").distinct("address.city")
# → ["Austin", "Indy", "Seattle"]
```

#### Mutation

```python
update(changes: dict) -> {"updated": N}
delete() -> {"deleted": N}
replace(new_doc: dict) -> {"replaced": N}
remove_field(field: str) -> {"removed": N}
```

**Examples**
```python
# mark all under 30 as junior
users.where("age").lt(30).update({"rank": "junior"})

# delete by name
users.where("name").eq("Carl").delete()

# replace exact matches
users.where("id").eq(2).replace({"id": 2, "name": "Bea Updated"})

# remove a field
users.where("name").eq("Neel").remove_field("rank")
```

#### Aggregations (query-scoped)

These work **after** filtering:
```python
sum(field)
avg(field)
min(field)
max(field)
```

**Examples**
```python
# average age for people with an email at a.com
users.where("email").matches("@a\\.com$").avg("age")
```

#### Lookup and Merge

```python
lookup(foreign_collection_name, local_key, foreign_key, as_field, many=True) -> QueryBuilder  
merge(fn: callable) -> QueryBuilder
```

- `lookup` runs the current query, matches each result to documents in another collection by key equality, and attaches the matched result(s) at `as_field`.
    - If `many=False`, attaches a single document or `None` (one-to-one).
    - If `many=True`, attaches a list of matching documents (one-to-many).
- `merge` transforms each (possibly looked-up) document by merging in fields returned from `fn(doc)`.

**Example - One-to-one join**

```python
users = db("users")
orders = db("orders")

users.clear(); orders.clear()
users.add_many([
    {"id": 1, "name": "Neel"},
    {"id": 2, "name": "Bea"},
])
orders.add_many([
    {"order_id": 10, "user_id": 1, "total": 50},
    {"order_id": 11, "user_id": 1, "total": 75},
    {"order_id": 12, "user_id": 2, "total": 20}
])

# Manually build a one-to-one map of latest order
latest_by_user = {}
for o in orders.all_docs():
    latest_by_user[o["user_id"]] = o  # override to get latest
orders_latest = db("orders_latest")
orders_latest.clear()
orders_latest.add_many(list(latest_by_user.values()))

out = (
    users.where("id").in_([1, 2])
         .lookup("orders_latest", local_key="id", foreign_key="user_id", as_field="latest_order", many=False)
         .merge(lambda d: {"latest_total": d.get("latest_order", {}).get("total", 0)})
         .run()
         .as_list()
)

# Result:
# [
#   {'id': 1, 'name': 'Neel', 'latest_order': {...}, 'latest_total': 75},
#   {'id': 2, 'name': 'Bea',  'latest_order': {...}, 'latest_total': 20}
# ]

```

**Example - One-to-many join**

```python
# Using full orders collection in a one-to-many join
out = (
    users.lookup("orders", local_key="id", foreign_key="user_id", as_field="orders", many=True)
         .merge(lambda u: {"total_spent": sum(o["total"] for o in u["orders"])})
         .run()
         .as_list()
)

# Result:
# [
#   {'id': 1, 'name': 'Neel', 'orders': [...], 'total_spent': 125},
#   {'id': 2, 'name': 'Bea',  'orders': [...], 'total_spent': 20}
# ]
```

> Note: `lookup` defaults to one-to-many (`many=True`). Use `many=False` for one-to-one joins.

---
#### Pagination

You can paginate query results using `.limit(n)` and `.offset(m)`:

```python
limit(n: int) -> QueryBuilder # Limits the number of results.
offset(m: int) -> QueryBuilder # Skips the first m results.
```

**Examples**
```python
col.where("score").gte(50).offset(10).limit(5).run()
# Returns 5 documents starting from the 11th result (zero-indexed).
```

### DocList

A lightweight wrapper around a list of documents.

```python
as_list() -> list[dict]
to_json(path: str) -> None
len(doclist) -> int
doclist[0]      # indexing
for d in doclist: ...
repr(doclist)   # pretty table-like output
```

**Examples**
```python
res = users.where("age").gte(25).run(fields=["id", "name"])
print(len(res))             # -> 3
print(res[0]["name"])       # -> 'Neel'
print(res.as_list())        # -> [{'id': 1, 'name': 'Neel'}, ...]
res.to_json("out.json")
print(res)                  # pretty-printed rows
```

---

## Error Handling

- This engine intentionally avoids raising on missing fields — comparisons on missing values simply **don’t match**.
- `exists()` checks presence, not truthiness.
- Numeric comparisons only apply to numeric values; non-numeric values fail the predicate.

---

## Example: end-to-end

```python
from coffy.nosql import db

users = db("users", path="data/users.json")
users.clear()
users.add_many([
    {"id": 1, "name": "Neel", "age": 30, "address": {"city": "Indy"}},
    {"id": 2, "name": "Bea",  "age": 25, "address": {"city": "Austin"}},
    {"id": 3, "name": "Carl", "age": 40}
])

# People with address, projected
print(users.where("address.city").exists().run(fields=["id", "address.city"]).as_list())

# Age 25-39
print(users.where("age").gte(25).where("age").lt(40).run().as_list())

# NOT (age < 30 OR name == 'Carl')
print(users.not_any(
    lambda q: q.where("age").lt(30),
    lambda q: q.where("name").eq("Carl"),
).run().as_list())

# Mutations
users.where("name").eq("Neel").update({"role": "admin"})
users.where("name").eq("Carl").delete()

# Aggregates
print(users.sum("age"), users.avg("age"))
```
