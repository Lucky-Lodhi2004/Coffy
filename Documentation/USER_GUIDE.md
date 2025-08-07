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
from coffy.sql import init, query

init(":memory:")                              # default = in‑memory
query("CREATE TABLE nums (n INT)")
query("INSERT INTO nums VALUES (42)")
result = query("SELECT * FROM nums")
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
4. **Export everywhere.** Any result → `.to_json()`, `.to_csv()`, or `save_query_result()`.

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

---

## 7. Limitations (Know Before You Go)

* Single‑process only — no concurrent writers.
* Not ACID; prefer snapshot saves over long transactions.
* No explicit indexing beyond in‑memory structures; keep datasets small (<~1e6 rows/nodes) or move to a server‑grade DB.
---

MIT license © 2025 Neel Sarathy • Happy hacking!
