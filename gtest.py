import json
from coffy.graph.executor import CypherExecutor
from coffy.graph.graphdb import GraphDB

if __name__ == "__main__":
    db = GraphDB("mytestdb2")
    exec = CypherExecutor(db)

    # CREATE test
    exec.execute(
        'CREATE (a:Person {name: "Alice"})-[:KNOWS]->(b:Person {name: "Bob"}), (a)-[:WORKS_AT]->(c:Company {name: "Initech"})'
    )

    # MATCH + RETURN test
    results = exec.execute(
        'MATCH (a:Person)-[:KNOWS]->(b:Person), (a)-[:WORKS_AT]->(c:Company) WHERE a.name="Alice" RETURN DISTINCT c'
    )
    
    print("\n\n----------------------------------------------------------------")

    # Pretty print only the 'return' results
    for item in results:
        if 'return' in item:
            print(json.dumps(item['return'], indent=2))

    # DELETE test (leave as is)
    exec.execute(
        'MATCH (a:Person)-[r:KNOWS]->(b:Person) WHERE b.name="Bob" DELETE r, b'
    )
    
    print("\n\n----------------------------------------------------------------")

    print(
        "All nodes after deletion:",
        json.dumps([n.to_dict() for n in db.all_nodes()], indent=2)
    )


# todo: duplicate ids are printed, need to fix that