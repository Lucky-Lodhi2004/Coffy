# Graph Examples Using Coffy

These examples demonstrate how to build and traverse graph structures using Coffy’s GraphDB module. They illustrate node creation, relationship mapping, and structured querying.

## Table of Contents
- [Example 1: Manager and Engineers in a Company](#example-1-manager-and-engineers-in-a-company)
- [Example 2: Mentor-Mentee Graph Traversal](#example-2-mentor-mentee-graph-traversal)
- [Example 3: Animal Kingdom Graph](#example-3-animal-kingdom-graph)

## Example 1: Manager and Engineers in a Company
This example models a simple organizational structure where a Manager manages multiple Engineers. It showcases adding nodes, relationships, and querying by role.

## Code
```python
from coffy.graph import GraphDB

# Create a file-backed graph
db = GraphDB(path="graph_data/company.json")

# Add nodes representing employees
db.add_node("N1", labels="Person", name="Arun", role="Manager")
db.add_node("P1", labels="Person", name="Neel", role="Engineer")
db.add_node("L2", labels="Person", name="Zara", role="Engineer")

# Define "MANAGES" relationships from manager to engineers
db.add_relationship("N1", "P1", rel_type="MANAGES")
db.add_relationship("N1", "L2", rel_type="MANAGES")

# Query: Find all engineers
db.find_nodes(label="Person", role="Engineer")
# Output:
# [
#   {'id': 'P1', 'labels': ['Person'], 'name': 'Neel', 'role': 'Engineer'},
#   {'id': 'L2', 'labels': ['Person'], 'name': 'Zara', 'role': 'Engineer'}
# ]

# Traverse: Who does Arun manage?
pattern = [{"rel_type": "MANAGES", "node": {"role": "Engineer"}}]
db.match_path_structured(start={"name": "Arun"}, pattern=pattern)
```
## Output
```bash
 [
   {
     'start': {'id': 'N1', 'name': 'Arun', 'labels': ['Person'], 'role': 'Manager'},
     'path': [
      {'type': 'MANAGES', 'to': {'id': 'P1', 'name': 'Neel', 'labels': ['Person'], 'role': 'Engineer'}},
       {'type': 'MANAGES', 'to': {'id': 'L2', 'name': 'Zara', 'labels': ['Person'], 'role': 'Engineer'}}
     ]
   }
 ]
```

---

## Example 2: Mentor-Mentee Graph Traversal
This example illustrates a mentorship relationship between two individuals. You’ll see how to create nodes, define one-directional relationships, and fetch structured paths.

## Code
```python
from coffy.graph import GraphDB

# File-backed graph database
db = GraphDB(path="graph_data/mentorship.json")

# Add people
db.add_node("M1", labels="Person", name="Sara", age=40)
db.add_node("M2", labels="Person", name="Tina", age=28)

# Define mentorship relationship
db.add_relationship("M1", "M2", rel_type="MENTORS", since=2022)

# Find Sara
db.find_nodes(label="Person", name="Sara")
# Output:
# [{'id': 'M1', 'labels': ['Person'], 'name': 'Sara', 'age': 40}]

# Traverse: Who does Sara mentor?
pattern = [{"rel_type": "MENTORS", "node": {"name": "Tina"}}]
db.match_path_structured(start={"name": "Sara"}, pattern=pattern)
```
## Output:
```bash
 [
   {
     'start': {'id': 'M1', 'name': 'Sara', 'labels': ['Person'], 'age': 40},
     'path': [
       {'type': 'MENTORS', 'to': {'id': 'M2', 'name': 'Tina', 'labels': ['Person'], 'age': 28}}
     ]
   }
 ]
 ```

---

# Example 3 (End-to-end): Animal Kingdom Graph

This example provides a richer demonstration of Coffy’s graph capabilities by modeling an Animal Kingdom. It includes various animal species, their classifications, and relationships.

## Code
```python

"""
graph_demo_animals.py
============================

A richer demonstration of *coffy.graph* using an **Animal‑Kingdom**
knowledge graph with extended entity types and relationships.

Highlights
----------
* Multiple node labels: Animal, Habitat, Biome, Continent, DietType,
  ConservationStatus.
* Relationship types: LIVES_IN, LOCATED_IN, HAS_BIOME, HAS_DIET,
  STATUS, EATS.
* Pretty‑formatted console output (tabular summaries).
* Extensive use of filtering, aggregation, projection, and pattern
  matching utilities.
* JSON persistence of the full graph and of specific query results.

Usage
-----
``pip install coffy networkx``

``python graph_demo_animals.py``

Two files will be written to the working directory::

    animal_graph.json       # complete graph snapshot
    carnivore_paths.json    # example path query output
"""

from coffy.graph import GraphDB
import random
import json
import os

# ---------------------------------------------------------------------------
# Pretty‑printing helpers
# ---------------------------------------------------------------------------

def _print_header(title: str) -> None:
    bar = "=" * 70
    print(f"\n{bar}\n{title}\n{bar}")


def _print_table(rows, headers):
    if not rows:
        print("<no data>")
        return
    widths = [max(len(str(x)) for x in col) for col in zip(headers, *rows)]
    header_line = " | ".join(str(h).ljust(w) for h, w in zip(headers, widths))
    sep_line = "-+-".join("-" * w for w in widths)
    print(header_line)
    print(sep_line)
    for row in rows:
        print(" | ".join(str(c).ljust(w) for c, w in zip(row, widths)))


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

NUM_SPECIES = 60
RANDOM_SEED = 23
GRAPH_PATH = ":memory:"        # change to 'animal_graph.json' for file‑backed

random.seed(RANDOM_SEED)

# ---------------------------------------------------------------------------
# Reference data
# ---------------------------------------------------------------------------

CLASSES = ["Mammal", "Bird", "Reptile", "Fish", "Amphibian", "Insect"]
DIETS = ["Herbivore", "Carnivore", "Omnivore"]
STATUSES = ["Least Concern", "Vulnerable", "Endangered", "Critically Endangered"]
CONTINENTS = ["Africa", "Asia", "Europe", "North America", "South America", "Oceania", "Antarctica"]
BIOMES = ["Tropical Rainforest", "Savanna", "Desert", "Temperate Forest", "Taiga",
          "Tundra", "Freshwater", "Marine"]
HABITATS = [
    "Amazon Basin", "Serengeti", "Sahara", "Great Barrier Reef", "Ganges Delta",
    "Rocky Mountains", "Patagonian Steppe", "Congo Rainforest", "Great Plains",
    "Himalayan Foothills", "Madagascar Forest", "Siberian Taiga", "Mojave Desert",
    "Danube Wetlands", "Galápagos Islands", "Scottish Highlands", "Yellowstone",
    "Okavango Delta", "Borneo Jungle", "Andes Cloud Forest"
]

# Map each habitat to a random continent & biome upfront
HABITAT_META = {
    name: {
        "continent": random.choice(CONTINENTS),
        "biome": random.choice(BIOMES)
    } for name in HABITATS
}

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def generate_species(idx: int) -> dict:
    animal_class = random.choice(CLASSES)
    diet = random.choices(DIETS, weights=[0.55, 0.25, 0.2])[0]
    status = random.choices(STATUSES, weights=[0.6, 0.25, 0.1, 0.05])[0]
    return {
        "id": f"S{idx}",
        "labels": ["Animal", animal_class],
        "name": f"Species_{idx}",
        "class": animal_class,
        "diet": diet,
        "status": status,
        "lifespan_years": random.randint(3, 70),
        "avg_weight_kg": round(random.uniform(0.02, 400), 2)
    }


def build_graph() -> GraphDB:
    db = GraphDB(path=GRAPH_PATH, directed=True)

    # -- Static entity nodes ------------------------------------------------
    db.add_nodes([{"id": f"D{i}", "labels": "DietType", "name": d}
                  for i, d in enumerate(DIETS, 1)])
    db.add_nodes([{"id": f"C{i}", "labels": "Continent", "name": c}
                  for i, c in enumerate(CONTINENTS, 1)])
    db.add_nodes([{"id": f"B{i}", "labels": "Biome", "name": b}
                  for i, b in enumerate(BIOMES, 1)])
    db.add_nodes([{"id": f"ST{i}", "labels": "ConservationStatus", "name": s}
                  for i, s in enumerate(STATUSES, 1)])

    # -- Habitat nodes ------------------------------------------------------
    habitat_nodes = []
    for i, name in enumerate(HABITATS, 1):
        meta = HABITAT_META[name]
        node = {"id": f"H{i}", "labels": "Habitat", "name": name,
                "continent": meta["continent"], "biome": meta["biome"]}
        habitat_nodes.append(node)
    db.add_nodes(habitat_nodes)

    # Link habitats to continents & biomes
    for hab in habitat_nodes:
        # continent node
        cont = next(n for n in db.find_nodes(label="Continent", name=hab["continent"]))
        biome = next(n for n in db.find_nodes(label="Biome", name=hab["biome"]))
        db.add_relationship(hab["id"], cont["id"], rel_type="LOCATED_IN")
        db.add_relationship(hab["id"], biome["id"], rel_type="HAS_BIOME")

    # -- Species nodes ------------------------------------------------------
    species_nodes = [generate_species(i) for i in range(1, NUM_SPECIES + 1)]
    db.add_nodes(species_nodes)

    # Link species to diet & status
    for sp in species_nodes:
        diet_node = next(n for n in db.find_nodes(label="DietType", name=sp["diet"]))
        status_node = next(n for n in db.find_nodes(label="ConservationStatus", name=sp["status"]))
        db.add_relationship(sp["id"], diet_node["id"], rel_type="HAS_DIET")
        db.add_relationship(sp["id"], status_node["id"], rel_type="STATUS")

    # Link species to habitats (1‑3 habitats each)
    for sp in species_nodes:
        hs = random.sample(habitat_nodes, k=random.randint(1, 3))
        for hab in hs:
            db.add_relationship(sp["id"], hab["id"], rel_type="LIVES_IN")

    # Predator/prey (EATS) relationships
    carnivores = [n for n in species_nodes if n["diet"] != "Herbivore"]
    possible_prey = [n for n in species_nodes if n["diet"] == "Herbivore"]
    for predator in carnivores:
        prey_sample = random.sample(possible_prey, k=min(2, len(possible_prey)))
        for prey in prey_sample:
            db.add_relationship(predator["id"], prey["id"], rel_type="EATS",
                                weight=round(random.uniform(0.1, 1.0), 2))

    # Upsert mythical creature to show set_node / update
    db.set_node("S999", labels=["Animal", "Mythical"], name="Dragon", diet="Carnivore")
    db.update_node("S999", status="Legendary", avg_weight_kg=5000)

    return db


# ---------------------------------------------------------------------------
# Demonstration logic
# ---------------------------------------------------------------------------

def demonstrate(db: GraphDB):
    _print_header("Graph Overview")
    print(f"Total nodes:          {db.count_nodes()}")
    print(f"Total relationships:  {db.count_relationships()}")
    print(f"Average degree:       {round(db.avg_degree(), 2)}")

    # Species count per class
    _print_header("Species Count by Class")
    rows = []
    for cl in CLASSES:
        cnt = db.find_nodes(label=cl).count()
        rows.append((cl, cnt))
    _print_table(rows, ["Class", "# Species"])

    # Conservation status distribution
    _print_header("Conservation Status Distribution")
    rows = []
    for st in STATUSES:
        cnt = db.find_nodes(label="Animal", status=st).count()
        rows.append((st, cnt))
    _print_table(rows, ["Status", "# Species"])

    # Example aggregation
    avg_life = db.find_nodes(label="Animal").avg("lifespan_years")
    print(f"\nAverage lifespan (all animals): {round(avg_life, 1)} years")

    # Strong predation links
    strong_eats = db.find_relationships(rel_type="EATS", weight={"gte": 0.8})
    print(f"Strong EATS relationships (weight ≥ 0.8): {strong_eats.count()}")

    # Pattern matching: carnivore → herbivore
    pattern = [{"rel_type": "EATS", "node": {"diet": "Herbivore"}}]
    carnivore_paths = db.match_path_structured(
        start={"diet": "Carnivore"},
        pattern=pattern,
        node_fields=["id", "name", "diet"],
        rel_fields=["type", "weight"]
    )
    print(f"Carnivore → Herbivore paths found: {len(carnivore_paths)}")

    # Save path results
    db.save_query_result(carnivore_paths, "carnivore_paths.json")
    print("Saved carnivore_paths.json")

    # Projection + pagination
    _print_header("First 8 Species (projected)")
    sample = db.find_nodes(label="Animal", fields=["id", "name", "diet"], limit=8)
    _print_table([tuple(n.values()) for n in sample.as_list()], ["ID", "Name", "Diet"])

    # Persist full graph
    db.save("animal_graph.json")
    print("Graph snapshot saved to animal_graph.json")

    # Optional visualization
    try:
        db.view()
    except Exception as exc:
        print("Visualization skipped:", exc)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    db = build_graph()
    demonstrate(db)


if __name__ == "__main__":
    main()
```

## Output
```bash

======================================================================
Graph Overview
======================================================================
Total nodes:          103
Total relationships:  338
Average degree:       6.56

======================================================================
Species Count by Class
======================================================================
Class     | # Species
----------+----------
Mammal    | 6
Bird      | 12
Reptile   | 13
Fish      | 10
Amphibian | 11
Insect    | 8

======================================================================
Conservation Status Distribution
======================================================================
Status                | # Species
----------------------+----------
Least Concern         | 33
Vulnerable            | 13
Endangered            | 6
Critically Endangered | 8

Average lifespan (all animals): 40.0 years
Strong EATS relationships (weight ≥ 0.8): 15
Carnivore → Herbivore paths found: 36
Saved carnivore_paths.json

======================================================================
First 8 Species (projected)
======================================================================
ID | Name      | Diet
---+-----------+----------
S1 | Species_1 | Herbivore
S2 | Species_2 | Carnivore
S3 | Species_3 | Herbivore
S4 | Species_4 | Herbivore
S5 | Species_5 | Herbivore
S6 | Species_6 | Herbivore
S7 | Species_7 | Herbivore
S8 | Species_8 | Herbivore
Graph snapshot saved to animal_graph.json
```

In browser window:

![graph visualization](https://github.com/nsarathy/Coffy/blob/main/Documentation/Examples/graphvizeg.png)