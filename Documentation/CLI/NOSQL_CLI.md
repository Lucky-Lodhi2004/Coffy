# NoSQL CLI

`coffy-nosql` is a file-backed command line interface for working with **`coffy.nosql`**, an embedded JSON document store.
It supports initializing collections, adding documents, running queries, performing aggregations, and clearing data, all through simple commands.

---

## CLI Table of Contents

- [Quick Start](#cli-quick-start)
- [Commands](#commands)
- [Options](#options)
- [Examples](#cli-examples)
- [Exit Codes](#exit-codes)

---

## CLI Quick Start

Initialize a new collection and add a few documents:

```bash
# initialize collection file
coffy-nosql --collection users --path ./users.json init

# add one document
coffy-nosql --collection users --path ./users.json add '{"id":1,"name":"Neel","age":30}'

# add many documents
coffy-nosql --collection users --path ./users.json add-many '[{"id":2,"name":"Bea","age":25},{"id":3,"name":"Carl","age":40}]'

# query users older than 29
coffy-nosql --collection users --path ./users.json query --field age --op gt --value 29
```

---

## Commands

### init

Initialize a JSON file to back a collection.

```bash
coffy-nosql --collection NAME --path FILE.json init
```

* Creates the file if it does not exist.
* Ensures the directory structure is created.

---

### add

Add a single document.

```bash
coffy-nosql --collection NAME --path FILE.json add DOC
```

**DOC** can be:

* JSON string: `{"id":1,"name":"Neel"}`
* File reference: `@doc.json`
* Read from stdin: `-`

---

### add-many

Add multiple documents in one call.

```bash
coffy-nosql --collection NAME --path FILE.json add-many DOCS
```

**DOCS** must be a JSON array:

* JSON string: `[{"id":1},{"id":2}]`
* File reference: `@docs.json`
* Read from stdin: `-`

---

### query

Run simple queries on one field.

```bash
coffy-nosql --collection NAME --path FILE.json query --field FIELD --op OP [--value VAL]
```

#### Operators

* `eq`, `ne`: equals, not equals
* `gt`, `gte`, `lt`, `lte`: numeric comparisons
* `in`, `nin`: membership in array
* `exists`: field presence
* `matches`: regex match (Python style)

#### Options

* `--value`: required for most operators, not allowed for `exists`
* `--fields`: projection fields to return
* `--count`: return only number of matches
* `--first`: return only the first match
* `--out FILE.json`: write results to file
* `--pretty`: pretty-print JSON results (adds indentation)

---

### agg

Run an aggregation across all documents.

```bash
coffy-nosql --collection NAME --path FILE.json agg {sum,avg,min,max,count} [--field FIELD]
```

* `sum`, `avg`, `min`, `max` require `--field`
* `count` counts all documents

---

### clear

Remove all documents from a collection.

```bash
coffy-nosql --collection NAME --path FILE.json clear
```

---

## Options

Global options (apply to all commands):

* `--collection NAME` (required): Collection name
* `--path FILE.json` (required): Path to JSON file backing the collection

---

## CLI Examples

**Initialize and add a document:**

```bash
coffy-nosql --collection users --path ./users.json init
coffy-nosql --collection users --path ./users.json add '{"id":1,"name":"Alice","age":22}'
```

**Add documents from a file:**

```bash
coffy-nosql --collection users --path ./users.json add-many @bulk_users.json
```

**Query for users aged ≥ 30:**

```bash
coffy-nosql --collection users --path ./users.json query --field age --op gte --value 30
```

**Get only the count:**

```bash
coffy-nosql --collection users --path ./users.json query --field age --op gte --value 30 --count
```

**Aggregate average age:**

```bash
coffy-nosql --collection users --path ./users.json agg avg --field age
```

**Clear all data:**

```bash
coffy-nosql --collection users --path ./users.json clear
```

---

## Exit Codes

* `0` Success
* `1` Failure (invalid arguments, parse errors, runtime errors)


