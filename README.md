# Coffy: Local-First Embedded Database Engine for Python

[![PyPI](https://img.shields.io/pypi/v/coffy)](https://pypi.org/project/coffy/)

**Coffy** is a lightweight, local-first embedded database engine supporting **NoSQL**, **SQL**, and **Graph** models — all in pure Python. Designed for fast prototyping, scripting, and local apps.

---

## Installation

```bash
pip install coffy
```

---
![preview](https://github.com/nsarathy/Coffy/blob/main/assets/Coffy%20preview%20image.png)
---
## Features

- Local persistence (JSON, SQLite)
- In-memory mode (`:memory:` or `None`)
- No server needed
- Logical and comparison operators
- Unified query interface

---

## Engines

| Engine | Description | Docs |
|--------|-------------|------|
| `coffy.graph` | Local graph database (NetworkX-based) | [Graph Docs](https://coffydb.org/graph) |
| `coffy.nosql` | Document store with chainable queries | [NoSQL Docs](https://coffydb.org/nosql) |
| `coffy.sql`   | Thin SQLite wrapper | [SQL Docs](https://coffydb.org/sql) |

---

## What sets Coffy apart?
Only embedded Python graph DB with:

- ✅ Declarative traversal syntax (match_node_path(...))
- ✅ Label/type filtering, limit/offset, result projection
- ✅ Unified API for both nodes and relationships

Only pure-Python embedded document store with:

- ✅ Auto-indexing on all top-level fields
- ✅ Chainable logical queries (.where(...).eq(...).or_().in_())
- ✅ Merge/lookups across collections (like mini $lookup)
- ✅ JSON persistence or in-memory fallback

---

## 🔗 Links

- PyPI: [coffy](https://pypi.org/project/coffy/)
- Source: [GitHub](https://github.com/nsarathy/Coffy)
- Graph Documentation: [GRAPH_DOCS.md](https://coffydb.org/graph)
- SQL Documentation: [SQL_DOCS.md](https://coffydb.org/sql)
- NoSQL Documentation: [NOSQL_DOCS.md](https://coffydb.org/nosql)

---

## License

MIT License © 2025 [Neel Sarathy](https://github.com/nsarathy)
