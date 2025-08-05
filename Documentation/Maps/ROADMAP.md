# 🗺️ Coffy Tentative Roadmap

This roadmap outlines short-, mid-, and long-term goals for the Coffy embedded database engine.  
It spans NoSQL, SQL, and Graph modules and aims to improve developer experience, performance, and extensibility.
---

## 🥇 Short-Term Goals

| Goal | Description |
|------|-------------|
| CLI Tools | Terminal-based exploration and querying of NoSQL/GraphDB |
| Improved Error Messages | Raise consistent, readable errors for misused filters and joins |

---

## 🥈 Mid-Term Goals

| Goal | Description |
|------|-------------|
| Improved CLI | Unified CLI for loading, querying, exporting, and inspecting databases |
| Plugin System | Add-on hooks for validation, custom formats, or query transforms |
| Enhanced Docs | Auto-generated reference and rich examples in `docs/` or `examples/` |

---

## 🥉 Long-Term / Stretch Goals

| Goal | Description |
|------|-------------|
| Indexing in GraphDB | Field and structure-based indexing for graph queries |
| NoSQL Schema Validation | Optional schema system with type checks and constraints |
| Hybrid Query Router | Chain filters across NoSQL/SQL/Graph in unified syntax |
| Public Test Dataset Repo | Curated JSONs and SQL for benchmarking and testing |
| WebAssembly Build | Run Coffy in-browser (via Pyodide or WASM) for demos or tools |

---

## 🔄 Release Cadence

- **Minor releases (v0.X)**: As features are added  
- **Patch releases (v0.X.Y)**: Bugfixes or doc/test updates  
- **v1.0 target**: Stable CLI, indexing, docs, and engine interoperability

---

## 🧠 Contributions Welcome!

Check out [CONTRIBUTING.md](../.github/CONTRIBUTING.md) and [Good First Issues](https://github.com/nsarathy/Coffy/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22) to get involved.
