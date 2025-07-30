## 📘 Graph Examples Using Coffy

These examples demonstrate how to build and traverse graph structures using Coffy’s GraphDB module. They illustrate node creation, relationship mapping, and structured querying.

## 🏢 Example 1: Manager and Engineers in a Company
This example models a simple organizational structure where a Manager manages multiple Engineers. It showcases adding nodes, relationships, and querying by role.

## CODE
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
## OUTPUT
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
## 👩‍🏫 Example 2: Mentor-Mentee Graph Traversal
This example illustrates a mentorship relationship between two individuals. You’ll see how to create nodes, define one-directional relationships, and fetch structured paths.

## 🧾 Code
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

 
