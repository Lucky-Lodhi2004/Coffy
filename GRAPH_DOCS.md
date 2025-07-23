# 📘 Coffy Graph Engine (`coffy.graph`)

Coffy’s graph engine wraps `networkx` to provide a clean, queryable, and minimalistic in-memory graph database with nodes, relationships, filtering, and logic operations.

Author: nsarathy

---

## 🧠 Overview

- Graph data structure with nodes and directed/undirected relationships
- Node and relationship attributes are first-class
- Query interface supports exact match, comparison (`gt`, `lt`, `eq`, etc.), and logical operators (`and`, `or`, `not`)
- No persistence (yet) — all in-memory

---

## 🔧 Usage

```python
from coffy.graph import GraphDB

db = GraphDB(directed=True)
```

---

## 📌 Methods

### Node Operations

| Method                         | Description                          |
|--------------------------------|--------------------------------------|
| `add_node(id, **attrs)`       | Add a single node                    |
| `add_nodes([{...}, ...])`     | Add multiple nodes                   |
| `get_node(id)`                | Get attributes for a node            |
| `remove_node(id)`             | Remove a node                        |
| `has_node(id)`                | Check if node exists                 |
| `degree(id)`                  | Get degree of node                   |
| `neighbors(id)`               | List neighbor node IDs               |
| `nodes()`                     | Get all nodes as list of dicts       |
| `find_nodes(**conditions)`    | Search nodes using attribute filters |

---

### Relationship (Edge) Operations

| Method                                | Description                             |
|---------------------------------------|-----------------------------------------|
| `add_relationship(u, v, **attrs)`     | Add a relationship (edge)               |
| `add_relationships([{...}, ...])`     | Add multiple relationships              |
| `get_relationship(u, v)`              | Get edge data                           |
| `remove_relationship(u, v)`           | Delete an edge                          |
| `has_relationship(u, v)`              | Check if edge exists                    |
| `relationships()`                     | Get all relationships as list of dicts  |
| `find_relationships(**conditions)`    | Filter relationships by attributes      |

---

## 🔍 Query Filters

### Supported Comparison Operators

You can use the following inside `find_nodes()` or `find_relationships()`:

- `eq` – equals
- `ne` – not equals
- `gt` – greater than
- `lt` – less than
- `gte` – greater than or equal
- `lte` – less than or equal

Example:

```python
db.find_nodes(age={"gt": 25})
db.find_relationships(type="friend")
```

---

### Logical Operators

Use `_logic` to combine multiple filters:

- `_logic="and"` (default)
- `_logic="or"`
- `_logic="not"` (negates all)

Example:

```python
# OR logic
db.find_nodes(age={"gt": 30}, name="Tanaya", _logic="or")

# NOT logic
db.find_nodes(age={"lt": 25}, _logic="not")
```

---

## 📤 Export

| Method         | Description                          |
|----------------|--------------------------------------|
| `to_dict()`    | Returns all nodes and relationships as dict |
| `nodes()`      | Returns node list                    |
| `relationships()` | Returns relationship list         |

---

## 🧪 Example

```python
from coffy.graph import GraphDB

db = GraphDB(directed=True)

db.add_nodes([
    {"id": 1, "name": "Neel", "age": 30},
    {"id": 2, "name": "Tanaya", "age": 28},
    {"id": 3, "name": "Mrittika", "age": 35},
])

db.add_relationships([
    {"source": 1, "target": 2, "type": "friend", "strength": 7},
    {"source": 2, "target": 3, "type": "colleague", "strength": 5},
    {"source": 1, "target": 3, "type": "friend", "strength": 9}
])

print(db.find_nodes(age={"gt": 29}))
print(db.find_relationships(type="friend"))
print(db.to_dict())
```

---

## 📄 License

MIT © 2025 nsarathy