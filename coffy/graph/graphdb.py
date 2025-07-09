import json
import os
from typing import Dict, List, Optional

class Node:
    def __init__(self, id: int, labels: List[str], properties: Dict):
        self.id = id
        self.labels = set(labels)
        self.properties = properties

    def to_dict(self):
        return {"id": self.id, "labels": list(self.labels), "properties": self.properties}

class Relationship:
    def __init__(self, id: int, rel_type: str, start: int, end: int, properties: Dict):
        self.id = id
        self.type = rel_type
        self.start = start  # node id
        self.end = end      # node id
        self.properties = properties

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "start": self.start,
            "end": self.end,
            "properties": self.properties
        }

class GraphDB:
    def __init__(self, db_name: str = "default"):
        self._databases = {}
        self.current_db = db_name
        self.load_database(db_name)

    def load_database(self, db_name: str):
        node_file = f"{db_name}_nodes.json"
        rel_file = f"{db_name}_rels.json"
        self.current_db = db_name

        # Load nodes
        try:
            with open(node_file, "r") as f:
                node_data = json.load(f)
                nodes = {n["id"]: Node(n["id"], n["labels"], n["properties"]) for n in node_data}
        except FileNotFoundError:
            nodes = {}

        # Load relationships
        try:
            with open(rel_file, "r") as f:
                rel_data = json.load(f)
                rels = {r["id"]: Relationship(r["id"], r["type"], r["start"], r["end"], r["properties"]) for r in rel_data}
        except FileNotFoundError:
            rels = {}

        self._databases[db_name] = {
            "node_file": node_file,
            "rel_file": rel_file,
            "nodes": nodes,
            "rels": rels,
            "next_node_id": max(nodes.keys(), default=0) + 1,
            "next_rel_id": max(rels.keys(), default=0) + 1
        }

    def switch_database(self, db_name: str):
        if db_name not in self._databases:
            self.load_database(db_name)
        self.current_db = db_name

    def save(self):
        db = self._databases[self.current_db]
        with open(db["node_file"], "w") as f:
            json.dump([n.to_dict() for n in db["nodes"].values()], f, indent=2)
        with open(db["rel_file"], "w") as f:
            json.dump([r.to_dict() for r in db["rels"].values()], f, indent=2)

    # Core API for node/relationship manipulation

    def add_node(self, labels: List[str], properties: Dict) -> int:
        db = self._databases[self.current_db]
        node_id = db["next_node_id"]
        node = Node(node_id, labels, properties)
        db["nodes"][node_id] = node
        db["next_node_id"] += 1
        return node_id

    def add_relationship(self, rel_type: str, start: int, end: int, properties: Dict) -> int:
        db = self._databases[self.current_db]
        rel_id = db["next_rel_id"]
        rel = Relationship(rel_id, rel_type, start, end, properties)
        db["rels"][rel_id] = rel
        db["next_rel_id"] += 1
        return rel_id

    def get_node(self, node_id: int) -> Optional[Node]:
        return self._databases[self.current_db]["nodes"].get(node_id)

    def get_relationship(self, rel_id: int) -> Optional[Relationship]:
        return self._databases[self.current_db]["rels"].get(rel_id)

    def all_nodes(self):
        return list(self._databases[self.current_db]["nodes"].values())

    def all_relationships(self):
        return list(self._databases[self.current_db]["rels"].values())

    def delete_node(self, node_id: int):
        db = self._databases[self.current_db]
        db["nodes"].pop(node_id, None)
        # Also delete all relationships attached to this node
        rels_to_delete = [rid for rid, rel in db["rels"].items() if rel.start == node_id or rel.end == node_id]
        for rid in rels_to_delete:
            db["rels"].pop(rid)

    def delete_relationship(self, rel_id: int):
        self._databases[self.current_db]["rels"].pop(rel_id, None)

# Example usage
if __name__ == "__main__":
    db = GraphDB("testdb")
    db.add_node(["Person"], {"name": "Alice"})
    db.add_node(["Person"], {"name": "Bob"})
    db.add_relationship("FRIENDS_WITH", 1, 2, {})
    db.save()
