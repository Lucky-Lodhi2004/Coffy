from coffy.graph import graph

g = graph("social")
g.add_node({"id": "1", "label": "Person", "name": "Alice"})
g.add_node({"id": "2", "label": "Person", "name": "Bob"})
g.add_node({"id": "3", "label": "Person", "name": "Charlie"})
g.add_edge({"source": "1", "target": "2", "label": "FRIEND"})
g.add_edge({"source": "1", "target": "3", "label": "FRIEND"})

friends_named_bob = (g >> "FRIEND" >> "Person").where("name").eq("Bob").run()
print(friends_named_bob)
