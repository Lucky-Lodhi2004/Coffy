# NoSQL Examples using Coffy
This document provides examples of how to use Coffy's NoSQL engine for various database operations, including querying, and mutating data.

## Example 1: Planets and Stars

### Code:
```python

"""
nosql_demo_space.py
=========================

Demonstration of *coffy.nosql* features using an **Astro‑Catalog**
with **Galaxies → Stars → Planets**.

Covered API surface
-------------------
* Collection creation & bulk insertion
* Nested fields, dot‑notation queries
* Logical helpers: ``match_any``, ``match_all``, ``not_any``
* Comparison operators & aggregations
* Projection & pagination
* Mutation: ``update``, ``delete`` & ``remove_field``
* One‑to‑one and one‑to‑many ``lookup`` joins with ``merge``
* DocList utilities
* Persistence/export

No visualization is used.

Run with::

    pip install coffy
    python nosql_demo_space.py

Two files will be created in the working directory::

    habitable_planets.json   # query result example
    galaxies_export.json     # full collection export
"""

from coffy.nosql import db
import random

# ----------------------------- Pretty helpers --------------------------- #

def _print_header(title: str) -> None:
    bar = "=" * 72
    print(f"\n{bar}\n{title}\n{bar}")


def _print_table(rows, headers):
    if not rows:
        print("<no data>")
        return
    widths = [max(len(str(x)) for x in col) for col in zip(headers, *rows)]
    h_line = " | ".join(str(h).ljust(w) for h, w in zip(headers, widths))
    sep = "-+-".join("-" * w for w in widths)
    print(h_line)
    print(sep)
    for row in rows:
        print(" | ".join(str(c).ljust(w) for c, w in zip(row, widths)))

# ------------------------------- Constants ------------------------------ #

random.seed(11)

GALAXIES = [
    {"name": "Milky Way",     "type": "Spiral",      "distance_Mly": 0.0},
    {"name": "Andromeda",     "type": "Spiral",      "distance_Mly": 2.54},
    {"name": "Triangulum",    "type": "Spiral",      "distance_Mly": 2.73},
    {"name": "Whirlpool",     "type": "Spiral",      "distance_Mly": 23},
    {"name": "Sombrero",      "type": "Spiral",      "distance_Mly": 31},
]

SPECTRAL_TYPES = ["O", "B", "A", "F", "G", "K", "M"]
PLANET_TYPES = ["Terrestrial", "Gas Giant", "Ice Giant", "Dwarf"]

# ---------------------------- Data Generation --------------------------- #

def generate_galaxies(col):
    col.clear()
    for g in GALAXIES:
        doc = {
            "name": g["name"],
            "type": g["type"],
            "distance_Mly": g["distance_Mly"],
            "coords": {
                "ra": round(random.uniform(0, 360), 2),
                "dec": round(random.uniform(-90, 90), 2)
            }
        }
        col.add(doc)


def generate_stars(col, galaxies):
    col.clear()
    star_id = 1
    for gal in galaxies.all_docs():
        for _ in range(random.randint(8, 12)):  # stars per galaxy
            doc = {
                "id": star_id,
                "name": f"Star_{star_id}",
                "galaxy": gal["name"],
                "spectral": random.choice(SPECTRAL_TYPES),
                "magnitude": round(random.uniform(-1.5, 15.0), 2),
                "mass_solar": round(random.uniform(0.1, 50), 2),
                "position": {
                    "ra": round(random.uniform(0, 360), 3),
                    "dec": round(random.uniform(-90, 90), 3)
                }
            }
            col.add(doc)
            star_id += 1


def generate_planets(col, stars):
    col.clear()
    planet_id = 1
    for st in stars.all_docs():
        for _ in range(random.randint(3, 6)):  # planets per star
            p_type = random.choice(PLANET_TYPES)
            hab = p_type == "Terrestrial" and random.random() < 0.2
            doc = {
                "id": planet_id,
                "name": f"Planet_{planet_id}",
                "star_id": st["id"],
                "type": p_type,
                "orbital_period_days": round(random.uniform(50, 10000), 1),
                "habitable": hab,
                "composition": {
                    "atmosphere": random.choice(["N2/O2", "CO2", "H2/He", "CH4", None])
                }
            }
            col.add(doc)
            planet_id += 1

# ---------------------------- Demonstration ----------------------------- #

def demo():
    galaxies = db("galaxies", path=":memory:")
    stars    = db("stars",    path=":memory:")
    planets  = db("planets",  path=":memory:")

    # Populate collections
    generate_galaxies(galaxies)
    generate_stars(stars, galaxies)
    generate_planets(planets, stars)

    # ------------------- Collection‑level aggregates -------------------- #
    _print_header("Collection Sizes")
    rows = [
        ("Galaxies", galaxies.count()),
        ("Stars",    stars.count()),
        ("Planets",  planets.count())
    ]
    _print_table(rows, ["Collection", "Documents"])

    # --------------------- Query: Habitable planets --------------------- #
    _print_header("Habitable Planets (top 10)")
    habitable = planets.where("habitable").eq(True).limit(10)
    rows = [(d["id"], d["name"], d["type"]) for d in habitable.run().as_list()]
    _print_table(rows, ["ID", "Name", "Type"])
    habitable = planets.where("habitable").eq(True)
    print(f"Total habitable planets: {habitable.count()} / {planets.count()}")
    habitable = habitable.run()
    habitable.to_json("habitable_planets.json")

    # ---------------- Average orbital periods by planet type ------------ #
    _print_header("Avg Orbital Period by Type")
    rows = []
    for ptype in PLANET_TYPES:
        q = planets.where("type").eq(ptype)
        rows.append((ptype, round(q.avg("orbital_period_days"), 1)))
    _print_table(rows, ["Planet Type", "Avg Period (days)"])

    # ---------------- Mutation: classify dwarf planets ------------------ #
    dwarfs_updated = planets.where("type").eq("Dwarf").update({"classification": "dwarf"})["updated"]
    print(f"\nAdded classification to {dwarfs_updated} dwarf planets")

    # ---------------- Delete example: remove uninhabitable dwarfs ------- #
    deleted = planets.match_all(
        lambda q: q.where("type").eq("Dwarf"),
        lambda q: q.where("habitable").eq(False)
    ).delete()["deleted"]
    print(f"Deleted {deleted} non‑habitable dwarf planets")

    # ---------------- Export galaxy collection ------------------------- #
    galaxies.export("galaxies_export.json")
    print("\nExported galaxies_export.json")

# ------------------------------ Main ----------------------------------- #

if __name__ == "__main__":
    demo()

```

### Output
```

========================================================================
Collection Sizes
========================================================================
Collection | Documents
-----------+----------
Galaxies   | 5
Stars      | 51
Planets    | 238

========================================================================
Habitable Planets (top 10)
========================================================================
ID  | Name       | Type
----+------------+------------
18  | Planet_18  | Terrestrial
59  | Planet_59  | Terrestrial
78  | Planet_78  | Terrestrial
49  | Planet_49  | Terrestrial
56  | Planet_56  | Terrestrial
97  | Planet_97  | Terrestrial
191 | Planet_191 | Terrestrial
193 | Planet_193 | Terrestrial
219 | Planet_219 | Terrestrial
Total habitable planets: 9 / 238

========================================================================
Avg Orbital Period by Type
========================================================================
Planet Type | Avg Period (days)
------------+------------------
Terrestrial | 4532.9
Gas Giant   | 5211.4
Ice Giant   | 5415.0
Dwarf       | 5790.6

Added classification to 51 dwarf planets
Deleted 51 non‑habitable dwarf planets

Exported galaxies_export.json
```