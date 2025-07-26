# 🗺️ Coffy Tentative Roadmap

This roadmap outlines short-, mid-, and long-term goals for the Coffy embedded database engine.  
It spans `NoSQL`, `SQL`, and `Graph` modules and aims to improve developer experience, performance, and extensibility.

---

## ✅ Current Status

- `NoSQL`: Nested queries, projections, joins (1:1), logic chaining, full test suite  
- `SQL`: Thin SQLite wrapper with raw query support, structured result object  
- `Graph`: NetworkX-based engine with labels, path matching, filtering, projections

---

## 🥇 Short-Term Goals (v0.2.x)

| Goal | Description |
|------|-------------|
| Pagination for NoSQL | Add `limit` and `offset` to `run()` |
| CLI tools | Inspect NoSQL and GraphDB from terminal |
| `maps/` docs | Add feature matrix, roadmap, and design overview |
| Code style CI | Add Ruff + Black lint checks on PR |
| Feature coverage tests | Add tests for missing Graph methods (`neighbors`, `degree`) |

---

## 🥈 Mid-Term Goals

| Goal | Description |
|------|-------------|
| One-to-many lookups | Extend NoSQL `lookup()` to support lists |
| Indexing (NoSQL) | Add internal field index for faster filtering |
| Graph aggregations | Add node/edge count, degree sum, etc. |
| Improved CLI | Unified CLI for loading/querying/exporting data |
| Plugin system | Optional extensions (e.g. validation, typing, formatters) |
| Richer docs | Examples for each feature in `docs/` or `examples/` folder |

---

## 🥉 Long-Term / Stretch Goals

| Goal | Description |
|------|-------------|
| GUI viewer | Interactive dashboard to explore databases |
| Real-time mode | Optional file watcher or in-memory sync with auto-refresh |
| Indexing in GraphDB | Optimize `find_nodes()` and traversal |
| NoSQL schema validation | Optional type hints, required fields, constraints |
| Graph visualizer | Export `GraphDB` to D3.js or Graphviz-compatible format |
| Hybrid query router | Allow pipelining across NoSQL/SQL/Graph using a unified interface |
| Public test dataset repo | JSONs and SQL to benchmark and test against |
| Pyodide/WebAssembly port | Run Coffy in-browser or embedded contexts |

---

## 🔄 Release Cadence

- Minor releases (v0.X): as features are added  
- Patch releases (v0.X.Y): bugfixes or doc updates  
- v1.0 target: stable CLI, indexing, docs, and cross-engine integration

---

## 🧠 Contributions Welcome!

Check out [CONTRIBUTING.md](../.github/CONTRIBUTING.md) and [Good First Issues](https://github.com/nsarathy/Coffy/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22) to get involved.
