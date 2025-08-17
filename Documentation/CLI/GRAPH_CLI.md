# Graph CLI

A lightweight, file-backed command line interface for **Coffy GraphDB**.

---

## Table of Contents

- [Overview](#cli-overview)
- [General Usage](#general-usage)
- [Global Options](#global-options)
- [Commands](#commands)
- [Conditions Format](#conditions-format)
- [Examples](#cli-examples)

---

## CLI Overview

The CLI wraps `coffy.graph.GraphDB` into a developer-friendly tool for managing JSON-backed graphs without writing Python code.

* **File-backed** only (no in-memory mode allowed here)
* **Safe defaults**: auto-creates parent directories
* **JSON input** via inline strings, `@file.json`, or `-` (stdin)
* **Pretty printing** and `--out` file export



If `coffy` is installed in your environment. You’ll get the `coffy-graph` executable.

---

## General Usage

```bash
coffy-graph --path FILE.json <command> [options...]
```

Example:

```bash
coffy-graph --path ./graph.json add-node --id A --labels Person --props '{"name":"Alice","age":30}'
```

---

## Global Options

* `--path FILE.json` (required): Path to JSON file backing the graph
* `--directed` (flag): Use directed graph semantics (defaults to undirected)

---

## Commands

### init

Initialize a new graph file if not present.

```bash
coffy-graph --path graph.json init
```

---

### add-node

Add or update a single node.

```bash
coffy-graph --path graph.json add-node --id ID [--labels LABELS...] [--props JSON]
```

* `--id` (required): Node ID
* `--labels`: One or more labels
* `--props`: JSON object of properties

**Examples**

```bash
coffy-graph --path graph.json add-node --id A --labels Person --props '{"name":"Alice","age":30}'
```

---

### add-nodes

Bulk add nodes from a JSON array.

```bash
coffy-graph --path graph.json add-nodes '[{"id":"B","labels":["Person"],"name":"Bob"}]'
coffy-graph --path graph.json add-nodes @nodes.json
```

---

### add-rel

Add or update a single relationship.

```bash
coffy-graph --path graph.json add-rel --source A --target B --type KNOWS [--props JSON]
```

---

### add-rels

Bulk add relationships from JSON array.

```bash
coffy-graph --path graph.json add-rels @rels.json
```

---

### find-nodes

Find nodes by label and conditions.

```bash
coffy-graph --path graph.json find-nodes [--label LABEL] [--conds JSON] [--fields F1 F2 ...] [--count | --first] [--pretty] [--out FILE]
```

* `--label`: Restrict to one label
* `--conds`: JSON filter (see [Conditions Format](#conditions-format))
* `--fields`: Projection fields
* `--count`: Return count only
* `--first`: Return only the first match
* `--pretty`: Pretty-print JSON
* `--out FILE`: Write results to JSON file

---

### find-rels

Find relationships by type and conditions.

```bash
coffy-graph --path graph.json find-rels [--type TYPE] [--conds JSON] [--fields F1 F2 ...] [--count | --first] [--pretty] [--out FILE]
```

---

### agg

Run graph-level aggregations.

```bash
coffy-graph --path graph.json agg <function> [--field FIELD]
```

Functions:

* `count-nodes`
* `count-nodes-by-label` (requires `--field` = label)
* `count-rels`
* `count-rels-by-type` (requires `--field` = type)
* `avg-degree`, `min-degree`, `max-degree`, `total-degree`
* (Directed only) `total-in-degree`, `avg-in-degree`, `min-in-degree`, `max-in-degree`, `total-out-degree`, `avg-out-degree`, etc.

**Examples**

```bash
coffy-graph --path graph.json agg count-nodes
coffy-graph --path graph.json agg count-nodes-by-label --field Person
```

---

### clear

Clear the entire graph.

```bash
coffy-graph --path graph.json clear
```

---

## Conditions Format

Conditions are JSON dicts.

* Simple equality: `{"name":"Alice"}`
* Comparison: `{"age":{"gt":25,"lt":40}}`
* Logical OR: `{"_logic":"or","name":"Alice","age":{"gt":35}}`
* NOT: `{"_logic":"not","age":{"lt":20}}`

---

## CLI Examples

1. Initialize and add nodes:

```bash
coffy-graph --path ./graph.json init
coffy-graph --path ./graph.json add-node --id A --labels Person --props '{"name":"Alice","age":30}'
coffy-graph --path ./graph.json add-node --id B --labels Person --props '{"name":"Bob","age":25}'
```

2. Add relationship:

```bash
coffy-graph --path ./graph.json add-rel --source A --target B --type KNOWS --props '{"since":2010}'
```

3. Find with conditions:

```bash
coffy-graph --path ./graph.json find-nodes --label Person --conds '{"age":{"gte":25}}' --fields id name --pretty
```

4. Aggregations:

```bash
coffy-graph --path ./graph.json agg count-nodes
```

5. Save query result:

```bash
coffy-graph --path ./graph.json find-nodes --label Person --fields id name --out people.json
```

