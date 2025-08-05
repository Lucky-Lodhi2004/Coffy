# ☕ Coffy Feature Matrix

| Feature                                  | `coffy.nosql`      | `coffy.sql`           | `coffy.graph`           | Notes / Gaps                                          |
| ---------------------------------------- | ------------------ | --------------------- | ----------------------- | ----------------------------------------------------- |
| **Local Persistence**                    | ✅                  | ✅                     | ✅                       | All support persistence on provided path              |
| **In-Memory Mode**                       | ✅                  | ✅                     | ✅                       | All support `:memory:` or `None` fallback             |
| **Typed Schema Enforcement**             | ❌                  | ✅ (via SQL DDL)       | ❌                       | Only SQLite supports explicit schemas                 |
| **Logical Operators (AND/OR/NOT)**       | ✅ (chainable)      | ✅ (`WHERE ...`)       | ✅                       | SQL uses standard SQL WHERE logic                     |
| **Comparison Operators (gt/lt/eq/ne)**   | ✅                  | ✅                     | ✅                       | Uniformly supported across all                        |
| **Joins / Lookups**                      | ✅ (1:1 and 1:N)     | ✅ (JOINs)             | ❌                       | One-to-many now supported in `nosql`                  |
| **Projections** (select specific fields) | ✅ (`fields=[...]`) | ✅ (`SELECT cols`)     | ✅                       | All support limited projections                       |
| **Full-Text Search / Regex**             | ✅ (`matches()`)    | ⚠️ (LIKE only)         | ❌                       | Only `nosql` supports regex matching                  |
| **Aggregations (sum, avg, min, max)**    | ✅                  | ✅                     | ✅                       | GraphDB supports field + graph-level aggregations     |
| **Indexing**                             | ✅                  | ✅ (SQLite)            | ❌                       | Indexes not implemented for graphs                |
| **Transactions / Rollback**              | ❌                  | ✅                     | ❌                       | Only `sql` has ACID semantics via SQLite              |
| **Custom Relationships / Edge Types**    | ❌                  | ❌                     | ✅                       | `graph` has `_type` and attributes on edges           |
| **Directional Traversals**               | ❌                  | ❌                     | ✅                       | Supports directed + undirected graphs                 |
| **Path Matching (Cypher-style)**         | ❌                  | ❌                     | ✅                       | `match_full_path`, `match_node_path`, etc.            |
| **Node Labels / Categories**             | ❌                  | ❌                     | ✅ (`_labels`)           | Labeled nodes are unique to GraphDB                   |
| **Export / Save Query Results**          | ✅ (`to_json()`)    | ✅ (`to_json()`)       | ✅ (`save_query_result`) | All can save JSON output                              |
| **Import / Load from JSON**              | ✅ (`import_()`)    | ❌                     | ✅ (`load(path)`)        | SQL must load via SQL                                 |
| **CLI Tooling**                          | ❌                  | ❌                     | ❌                       | Would be a useful enhancement                         |
| **GUI / Visualization**                  | ✅                  | ✅                     | ✅                       | `view()`         |
| **One-to-Many Lookups**                  | ✅                  | ✅                     | ❌                       | Now fully supported in `nosql`                        |
| **Custom Field Indexing**                | ❌                  | ✅                     | ❌                       | Needed for performance scaling in `nosql` and `graph` |
| **Schema Validation**                    | ❌                  | ✅                     | ❌                       | SQLite enforces schema; `nosql` is fully dynamic      |
| **Pagination**                           | ✅ (`limit`, `offset`) | ⚠️ (manual via LIMIT) | ✅ (`limit`, `offset`) | Fully supported in `nosql` and `graph`                |
| **Multi-collection Queries**             | ✅ (via lookup)     | ✅                     | ❌                       | Graph queries are limited to one graph instance       |
| **Visualization-friendly Output**        | ⚠️ (tabular)        | ✅ (tabular)           | ⚠️ (structured paths)   | Could standardize better for frontend integration     |

## ✅ Legend
- ✅ Fully supported
- ⚠️ Partially supported or requires manual effort
- ❌ Not supported
