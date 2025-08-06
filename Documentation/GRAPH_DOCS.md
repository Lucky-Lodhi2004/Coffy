# coffy.graph

A lightweight, Cypher-inspired graph engine built on top of `networkx`.  
Supports labeled nodes, typed relationships, projections, conditional filtering, directional traversals, and JSON persistence.

> Scope: single-process, developer-focused. Not ACID. Designed for simplicity and clarity.

## Table of Contents
- [Features](#features)
- [Quick Start](#quick-start)
- [Persistence](#persistence)
- [Data Model](#data-model)
- [Conditions](#conditions)
- [Start Here](#start-here)
  - [Constructor](#constructor)
  - [Node operations](#node-operations)
  - [Relationship operations](#relationship-operations)
  - [Introspection](#introspection)
  - [Update and upsert](#update-and-upsert)
  - [Projection](#projection)
  - [Find functions](#find-functions)
  - [GraphResult](#graphresult)
  - [Field Level Aggregations](#field-level-aggregations)
  - [Pattern matching](#pattern-matching)
  - [Export](#export)
  - [Saving query results](#saving-query-results)
  - [Visualization](#visualization)
- [Examples](#examples)
- [Limitations and notes](#limitations-and-notes)

## Features
- Nodes with **labels** and arbitrary properties
- Relationships with **types** and arbitrary properties
- **Directional** traversals for directed graphs, or undirected mode
- **Pattern matching** with typed edges and filtered nodes
- **Logical filtering**: `and` default, plus `_logic="or"` and `_logic="not"`
- **Comparisons**: `gt`, `gte`, `lt`, `lte`, `eq`, `ne`
- **Projection**: return only the fields you need
- **JSON persistence** with optional `:memory:` mode
- Structured **path** results similar to Cypher

## Quick Start

```python
from coffy.graph import GraphDB

db = GraphDB(path="graph_data/people.json")  # file-backed
db.add_node("A", labels="Person", name="Alice", age=30)
db.add_node("B", labels="Person", name="Bob", age=25)
db.add_relationship("A", "B", rel_type="KNOWS", since=2010)

# Find
db.find_nodes(label="Person", name="Alice")
# [{'id': 'A', 'labels': ['Person'], 'name': 'Alice', 'age': 30}]

# Traverse
pattern = [{"rel_type": "KNOWS", "node": {"name": "Bob"}}]
db.match_path_structured(start={"name": "Alice"}, pattern=pattern)
```

## Persistence

- `path="file.json"` → file-backed. Auto-loads if file exists. Writes after every mutation.
- `path=":memory:"` or `path=None` → in-memory only. No writes.
- Files are standard JSON with the shape:
  ```json
  {
    "nodes": [ { "id": "A", "labels": ["Person"], "name": "Alice" } ],
    "relationships": [ { "source": "A", "target": "B", "type": "KNOWS", "since": 2010 } ]
  }
  ```

## Data Model

- **Node**
  - Required: `id`
  - Optional: `_labels` stored internally, exported as `labels`
  - Arbitrary properties

- **Relationship**
  - Required: `source`, `target`
  - Optional: `_type` stored internally, exported as `type`
  - Arbitrary properties

## Conditions

Use keyword filters in `find_*` methods.

- Simple equality: `name="Alice"`
- Comparisons: `age={"gt": 30}`, `age={"lte": 40}`
- Logic:
  - Default is `and`
  - `_logic="or"` combines predicates with OR
  - `_logic="not"` negates the combined result

## Start Here

### Constructor

```python
GraphDB(directed: bool = False, path: str | None = None)
```

- `directed`: use `DiGraph` when `True`. If not set `False` by default.
- `path`: JSON file for persistence. Use `":memory:"` for in-memory mode

**Examples**
```python
db = GraphDB(directed=True, path="graph.json")
db_mem = GraphDB(path=":memory:")
```

---

### Node operations

#### `add_node(node_id, labels=None, **attrs)`
Add or update a node with labels and properties.

```python
db.add_node("U1", labels="Person", name="Alice", age=30)
db.add_node("U2", labels=["Person", "Employee"], name="Bob", age=25)
```

#### `add_nodes(nodes)`
Bulk add nodes with a list of dicts.

```python
db.add_nodes([
    {"id": "U3", "labels": "Company", "name": "Acme"},
    {"id": "U4", "labels": ["Person"], "name": "Carol", "age": 40}
])
```

#### `get_node(node_id)`
Return the node attribute dict.

```python
db.get_node("U1")["name"]  # 'Alice'
```

#### `remove_node(node_id)`
Remove a node.

```python
db.remove_node("U4")
```

#### `clear()`
Clear the graph, removing all nodes and relationships.
```python
db.clear()
```
---

### Relationship operations

#### `add_relationship(source, target, rel_type=None, **attrs)`
Create a relationship with optional type and properties.

```python
db.add_relationship("U1", "U2", rel_type="FRIEND_OF", since=2020)
db.add_relationship("U2", "U3", rel_type="WORKS_AT", title="Engineer")
```

#### `add_relationships(relationships)`
Bulk add edges.

```python
db.add_relationships([
    {"source": "U1", "target": "U3", "type": "LIKES", "weight": 0.9},
    {"source": "U2", "target": "U1", "type": "FOLLOWS"}
])
```

#### `get_relationship(source, target)`
Get edge attributes.

```python
db.get_relationship("U1", "U2")["_type"]  # 'FRIEND_OF'
```

#### `remove_relationship(source, target)`
Remove an edge.

```python
db.remove_relationship("U2", "U1")
```

---

### Introspection

#### `neighbors(node_id)`
List adjacent nodes.

```python
db.neighbors("U1")  # ['U2', 'U3']
```

#### `degree(node_id)`
Degree for the node, respecting graph direction model.

```python
db.degree("U1")
```

#### `has_node(node_id)` / `has_relationship(u, v)`
Presence checks.

```python
db.has_node("U1")
db.has_relationship("U1", "U2")
```

#### Graph-Level Aggregations
The following methods provide quick graph-wide statistics:

```python
db.count_nodes()          # → total number of nodes
db.count_relationships()  # → total number of relationships (edges)
db.avg_degree()           # → average node degree
db.min_degree()           # → minimum node degree
db.max_degree()           # → maximum node degree
db.total_degree()         # → sum of all node degrees

# Directed graphs only:
db.total_in_degree()      # → sum of in-degrees across all nodes
db.total_out_degree()     # → sum of out-degrees across all nodes
db.total_in_degree()      # → sum of in-degrees across all nodes
db.avg_in_degree()        # → average in-degree (only for directed graphs)
db.min_in_degree()        # → minimum in-degree (only for directed graphs)
db.max_in_degree()        # → maximum in-degree (only for directed graphs)
db.total_out_degree()     # → sum of out-degrees across all nodes
db.avg_out_degree()       # → average out-degree (only for directed graphs)
db.min_out_degree()       # → minimum out-degree (only for directed graphs)
db.max_out_degree()       # → maximum out-degree (only for directed graphs)
```

---

### Update and upsert

#### `update_node(node_id, **attrs)`
Update fields on an existing node.

```python
db.update_node("U1", age=31, city="Indy")
```

#### `update_relationship(source, target, **attrs)`
Update fields on an existing edge.

```python
db.update_relationship("U1", "U2", since=2021, strength="strong")
```

#### `set_node(node_id, labels=None, **attrs)`
Upsert node. Creates or updates.

```python
db.set_node("U5", labels="Person", name="Eve")
db.set_node("U5", mood="curious")  # updates existing
```

---

### Projection

#### `project_node(node_id, fields=None)`
Return a full node dict or just selected fields.

```python
db.project_node("U1")                    # full
db.project_node("U1", fields=["name"])   # {'name': 'Alice'}
```

#### `project_relationship(source, target, fields=None)`
Return full relationship dict or selected fields.

```python
db.project_relationship("U1", "U2")                    # full
db.project_relationship("U1", "U2", fields=["since"])  # {'since': 2020}
```

---

### Find functions

#### `find_nodes(label=None, fields=None, **conditions)`
Filter nodes by label and conditions. Supports `_logic` and comparison operators. Supports pagination with `limit` and `offset`.

```python
# 1) Exact match
db.find_nodes(label="Person", name="Alice")

# 2) OR
db.find_nodes(label="Person", _logic="or", name="Alice", age={"gt": 35})

# 3) NOT
db.find_nodes(label="Person", _logic="not", age={"lt": 35})

# 4) Range
db.find_nodes(label="Person", age={"gte": 25, "lt": 35}, fields=["id", "name"])

# 5) Pagination
db.find_nodes(label="Person", fields=["id", "name"], limit=10, offset=5)
db.find_nodes(label="Person", fields=["id", "name"], limit=5)
db.find_nodes(label="Person", _logic="or", name="Alice", age={"gt": 35}, offset=1)
```

#### `find_by_label(label, fields=None)`
Fast label filter.

```python
db.find_by_label("Person", fields=["id", "name"])

db.find_by_label("Company", fields=["id", "name"], limit=5, offset=2)
```

#### `find_relationships(rel_type=None, fields=None, **conditions)`
Filter edges by type and attribute conditions.

```python
# All FRIEND_OF since 2015 or later
db.find_relationships(rel_type="FRIEND_OF", since={"gte": 2015})

# Any relationships with weight less than 0.5
db.find_relationships(weight={"lt": 0.5})

db.find_relationships(rel_type="WORKS_AT", fields=["source", "target", "title"],
                       limit=10, offset=5)
```

#### `find_by_relationship_type(rel_type, fields=None)`
Fast relationship type filter.

```python
db.find_by_relationship_type("WORKS_AT", fields=["source", "target"])

db.find_by_relationship_type("FRIEND_OF", fields=["source", "target"], limit=5, offset=2)
```

---

### GraphResult
The methods `find_nodes(...)`, `find_by_label(...)`, `find_relationships(...)`, and `find_by_relationship_type(...)` return a `GraphResult` object. This object behaves like a list but also provides methods for aggregation and introspection.

```python
class GraphResult:
    def sum(self, field)
    def avg(self, field)
    def min(self, field)
    def max(self, field)
    def count()
    def first()
    def as_list()
```
---

### Field Level Aggregations
You can perform aggregation operations on the results of `find_nodes(...)`, `find_relationships(...)`, `find_by_label(...)`, and `find_by_relationship_type(...)`.

These results support:

- `.count()` — number of matched nodes/relationships
- `.sum(field)` — sum of a numeric field
- `.avg(field)` — average of a numeric field
- `.min(field)` — minimum value of a numeric field
- `.max(field)` — maximum value
- `.first()` — return the first matched item

Example:
```python
result = db.find_nodes(label="Person", age={"gte": 25}, fields=["name", "age"])

result.count()        # → 2
result.sum("age")     # → 55
result.avg("age")     # → 27.5
result.min("age")     # → 25
result.max("age")     # → 30
result.first()        # → {'name': 'Alice', 'age': 25}
```
---

### Pattern matching

Patterns are lists of steps. Each step has:
- `rel_type`: required relationship type filter, or omit for any
- `node`: a condition dict to filter the next node

#### `match_node_path(start, pattern, return_nodes=True, node_fields=None, direction="out")`
Return paths as lists of nodes or node IDs.

```python
pattern = [{"rel_type": "FRIEND_OF", "node": {"name": "Bob"}}]

# Return projected nodes
db.match_node_path(start={"name": "Alice"}, pattern=pattern, node_fields=["name"])

# Return node ID sequences
db.match_node_path(start={"name": "Alice"}, pattern=pattern, return_nodes=False)
```

#### `match_full_path(start, pattern, node_fields=None, rel_fields=None, direction="out")`
Return both nodes and relationships per match.

```python
pattern = [
    {"rel_type": "FRIEND_OF", "node": {"name": "Bob"}},
    {"rel_type": "WORKS_AT", "node": {"label": "Company"}}
]
db.match_full_path(start={"name": "Alice"}, pattern=pattern,
                   node_fields=["id", "name"], rel_fields=["type", "since"])
```

#### `match_path_structured(start, pattern, node_fields=None, rel_fields=None, direction="out")`
Return interleaved objects similar to a Cypher path.

```python
pattern = [{"rel_type": "KNOWS", "node": {"age": {"gte": 25}}}]
db.match_path_structured(start={"name": "Alice"}, pattern=pattern)
# [
#   {
#     "path": [
#       {"node": {...}},
#       {"relationship": {...}},
#       {"node": {...}},
#       ...
#     ]
#   }
# ]
```

- `direction`: `"out"` from current node, `"in"` for incoming, `"any"` for both on directed graphs. Ignored in undirected graphs.

---

### Export

#### `nodes()` / `relationships()`
Export all nodes or relationships as JSON-friendly lists.

```python
db.nodes()
db.relationships()
```

#### `to_dict()`
Export the whole graph as a dict.

```python
graph_dict = db.to_dict()
```

#### `save(path=None)` / `load(path=None)`
Persist or load the graph. `save()` writes pretty JSON.

```python
db.save()                 # to current path
db.save("backup.json")    # to a new file
db2 = GraphDB(path="backup.json")  # auto-loads
```

### Saving query results

#### `save_query_result(result, path)`
Write any JSON-serializable result to a file.

```python
people = db.find_nodes(label="Person", fields=["id", "name"])
db.save_query_result(people, "people.json")
```

---
### Visualization
```python
db.view()   # Opens an interactive graph visualization in a web browser
```
#### Example
![Graph Visualization](https://github.com/nsarathy/Coffy/blob/main/assets/graphviz.png)
## Examples

```python
from coffy.graph import GraphDB

db = GraphDB(path="graph_data/people.json")
db.add_node("A", labels="Person", name="Alice", age=30)
db.add_node("B", labels="Person", name="Bob", age=25)
db.add_node("C", labels="Company", name="Acme")
db.add_relationship("A", "B", rel_type="FRIEND_OF", since=2010)
db.add_relationship("B", "C", rel_type="WORKS_AT", title="Engineer")

# Find with OR
db.find_nodes(label="Person", _logic="or", name="Alice", age={"gt": 35})

# Traverse two hops
pattern = [
    {"rel_type": "FRIEND_OF", "node": {"name": "Bob"}},
    {"rel_type": "WORKS_AT", "node": {"labels": ["Company"]}}
]
db.match_full_path(start={"name": "Alice"}, pattern=pattern,
                   node_fields=["id", "name"], rel_fields=["type", "title"])
```