# Coffy User Guide

**Local‑First Embedded Graph, NoSQL & SQL in Pure Python**

Coffy lets you prototype, script and ship data‑driven features without ever leaving Python—or spinning up a server. One `pip install` drops three tiny engines on disk:

| Engine | Back‑end | Primary Use‑Case |
|--------|----------|------------------|
| `coffy.graph` | NetworkX | Graph data & traversals |
| `coffy.nosql` | JSON | Document storage & analytics |
| `coffy.sql`   | SQLite | Tabular queries & exports |

---

## 1. Installation

```bash
pip install coffy
```

Coffy is pure‑Python; no C‑extensions, no build headaches. Python ≥3.7

---

## 2. Quick Start Cheatsheet

### 2.1 GraphDB

```python
from coffy.graph import GraphDB

g = GraphDB(path=":memory:")           # in‑memory, wipe on exit
g.add_node("A", labels="Person", name="Alice")
g.add_node("B", labels="Person", name="Bob")
g.add_relationship("A", "B", rel_type="KNOWS", since=2021)
```

### 2.2 NoSQL

```python
from coffy.nosql import db

users = db("users", path="data/users.json")   # JSON‑backed
users.add({"id": 1, "name": "Neel", "age": 30})
junior = users.where("age").lt(25).run()
```

### 2.3 SQL

```python
from coffy.sql import init, query, Model, Integer

init(":memory:")                              # default = in-memory

# Raw SQL
query("CREATE TABLE nums (n INT)")
query("INSERT INTO nums VALUES (42)")

# ORM (optional)
class User(Model):
    id = Integer(primary_key=True)
    name = Text()
User.objects.create_table()
User.objects.insert(id=1, name="Neel")
print(User.objects.get(id=1))
```

---

## 3. Persistence Modes

| Argument | Effect |
|----------|--------|
| `path=":memory:"` *or* `None` | Keep everything RAM‑only — fastest, volatile |
| `path="file.json"` / `file.sqlite` | Auto‑load & auto‑save; ideal for local apps |
| Swap paths at any time | Call `save(new_path)` to fork snapshots |

---

## 4. Day‑to‑Day Workflow

1. **Model locally.** Start in `:memory:` for speed.  
2. **Persist when it matters.** Flip to file‑backed once your schema stabilises.  
3. **Query fluently.** Chain filters (`where().eq().gt()`) or pattern‑match (`match_path_structured`) without mental context‑switching between engines.  
4. **Pick your style.** Use raw SQL for quick one-offs or the built-in ORM for clean, chainable Python queries.
5. **Export everywhere.** Any result → `.to_json()`, `.to_csv()`, or `save_query_result()`.

---

## 5. Advanced Playbook

### 5.1 Graph Pattern Matching

```python
pattern = [{"rel_type": "MANAGES", "node": {"role": "Engineer"}}]
managers = g.match_node_path(start={"role": "Manager"},
                             pattern=pattern,
                             node_fields=["name"])
```

### 5.2 NoSQL Look‑ups & Aggregates

```python
# one‑to‑many join: user → orders
enriched = (users.lookup("orders",
                         local_key="id",
                         foreign_key="user_id",
                         as_field="orders")
                  .merge(lambda u: {"spent": sum(o["total"] for o in u["orders"])})
                  .run())
```

### 5.3 SQL Export After Heavy Filtering

```python
big = query("SELECT * FROM logs WHERE ts >= '2025‑01‑01'")
big.to_csv("logs_2025.csv")
```
```
from coffy.sql import Model, Integer, Text
class Log(Model):
    id = Integer(primary_key=True)
    ts = Text()
    msg = Text()

recent = Log.objects.query().where(("ts", ">=", "2025-01-01")).all()
recent.to_csv("logs_2025.csv")
```

### 5.4 Mixing Engines (Example)

```python
# Dump graph nodes → NoSQL for ad‑hoc JSON analytics
people = g.find_nodes(label="Person").as_list()
ppl_col = db("people_tmp", path=":memory:")
ppl_col.add_many(people)
print(ppl_col.avg("age"))
```

---

## 6. Why Coffy Rocks

* **One import, three models.** Uniform mental model; no extra daemons.
* **Zero external deps.** Pure‑Python + SQLite — painless on CI, Windows, ARM.
* **Fluent APIs.** Chainable queries, declarative traversals, instant visualisation.
* **Local‑first philosophy.** Perfect for CLIs, notebooks, desktop apps, and edge devices.
* **JSON‑Readable Storage.** Debug or hand‑edit your data with any text editor.
* **Built-in ORM.** Define models in pure Python, bulk-insert, filter, join, group, and aggregate without leaving your editor.

---

## 7. Feature Matrix

| Feature | coffy.graph | coffy.nosql | coffy.sql |
|---|---|---|---|
| File-backed persistence | ✅ JSON | ✅ JSON | ✅ SQLite |
| In-memory mode | ✅ | ✅ | ✅ |
| Atomic writes on save | ✅ | ✅ | ❌ (SQLite handles durability) |
| Auto create dirs, auto load | ✅ | ✅ | ✅ (SQLite creates file) |
| Path validation | ✅ .json required | ✅ .json required | ✅ any .db or path |
| ACID guarantees | ❌ | ❌ | ✅ (SQLite) |
| Schema enforcement | ❌ | ❌ | ✅ (ORM) |
| Flexible schema | ✅ nodes, rels | ✅ documents | ⚠️ via nullable columns |
| Result wrapper | ✅ GraphResult | ✅ DocList | ✅ SQLDict |
| Pretty `__repr__` | ❌ | ✅ | ✅ |
| Export query to JSON | ✅ | ✅ | ✅ |
| HTML viewer | ✅ PyVis, tooltips | ✅ Card grid | ✅ Table view |
| Strict add duplicate guard | ✅ `add_node` raises | ❌ | ❌ |
| Remove by label or type | ✅ nodes, rels | ✅ `remove_field` only | ❌ (use WHERE) |
| Projection | ✅ node, rel | ✅ `run(fields=...)` | ✅ `select(...)` |
| Pagination | ✅ limit, offset | ✅ limit, offset | ✅ limit, offset |
| Logical filters | ✅ and, or, not | ✅ AND, OR, NOT | ✅ WHERE, HAVING |
| Comparisons | ✅ gt, gte, lt, lte, eq, ne | ✅ eq, ne, gt, gte, lt, lte, between | ✅ all SQL ops |
| Regex match | ❌ | ✅ `matches()` | ✅ `LIKE` or `REGEXP` (pragma) |
| Field existence | ❌ | ✅ `exists()` | ✅ `IS NULL` checks |
| Nested field access | ❌ | ✅ dotted paths | ❌ |
| Indexing | ❌ | ✅ equality and `in_` | ✅ SQLite indexes (user defined) |
| Aggregations (collection/graph) | ✅ degree stats, counts | ✅ sum, avg, min, max, count | ✅ SQL aggregates |
| Aggregations on filtered result | ✅ GraphResult methods | ✅ QueryBuilder methods | ✅ `.aggregate()` or SQL |
| Distinct values | ❌ | ✅ coerces to str | ✅ `SELECT DISTINCT` |
| Bulk insert/add | ✅ nodes, rels | ✅ `add_many` | ✅ `bulk_insert` |
| Update | ✅ node, rel | ✅ `update({...})` | ✅ `UPDATE` via Manager |
| Replace | ❌ | ✅ `replace(new_doc)` | ✅ `REPLACE` or upsert pattern |
| Upsert | ✅ `set_node` | ❌ | ⚠️ use `INSERT OR REPLACE` manually |
| Delete | ✅ node, rel | ✅ `delete()` | ✅ `DELETE` via Manager |
| Joins | ⚠️ via traversal | ✅ `lookup` one-to-one, many | ✅ `JOIN` in Query |
| Join types | N/A | N/A | ⚠️ INNER, LEFT ok, RIGHT/FULL not in SQLite |
| Cross-collection enrich | ❌ | ✅ `lookup(..., many=\|False)` | ✅ JOINs or CTEs |
| Query builder | ❌ | ✅ chainable | ✅ fluent `Query` API |
| Raw queries | ❌ | ❌ | ✅ `raw(sql, params)` |
| CTEs | ❌ | ❌ | ✅ `.with_cte(..., recursive=...)` |
| Identifier validation | ❌ | ❌ | ✅ `_quote_ident` guards names |
| Param binding | ❌ | ❌ | ✅ `?` parameters everywhere |
| Default values in DDL | ❌ | ❌ | ✅ safely inlined via `quote(?)` |
| Error surface | Exceptions | Exceptions | ⚠️ `engine.query` returns error dicts |
| Directed graphs | ✅ flag | N/A | N/A |
| Path matching, traversal | ✅ node, full, structured | ❌ | ⚠️ emulate via JOINs/CTEs |
| Cycle avoidance in match | ✅ | N/A | N/A |
| Degree metrics | ✅ avg, min, max, totals | ❌ | ❌ |
| Count by label/type | ✅ | ❌ | ✅ via SQL WHERE |
| Save whole dataset | ✅ `save()` | ✅ `save()` | ❌ (dump via SQL) |
| Import/export dataset | ✅ JSON | ✅ JSON | ⚠️ CSV/JSON export of results only |

## Legend
- ✅ fully supported
- ⚠️ partially supported or has caveats
- ❌ not supported

---

## 8. Limitations (Know Before You Go)

* Single‑process only — no concurrent writers.
* Not ACID (nosql and graph); prefer snapshot saves over long transactions.
* No explicit indexing beyond in‑memory structures (graph).
---

MIT license © 2025 Neel Sarathy
