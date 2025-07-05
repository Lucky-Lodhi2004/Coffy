from coffy.nosql import doc

print("=== TEST: clear() ===")
doc("users").clear()
doc("orders").clear()

print("=== TEST: add(), add_many() ===")
doc("users").add({"id": 1, "name": "Neel", "email": "neel@a.com"})  # {'inserted': 1}
doc("users").add_many([
    {"id": 2, "name": "Tanaya", "email": "tanaya@b.com"},
    {"id": 3, "name": "Mrittika", "email": "mrittika@c.com"}
])
print(doc("users").count())  # 3

print("=== TEST: where() + eq(), ne(), gt(), gte(), lt(), lte(), in_(), nin(), matches(), exists() ===")
doc("orders").add_many([
    {"order_id": 101, "user_id": 1, "total": 100, "status": "delivered"},
    {"order_id": 102, "user_id": 2, "total": 50, "status": "pending"},
    {"order_id": 103, "user_id": 3, "total": 150, "status": "delivered"},
    {"order_id": 104, "user_id": 2, "total": 70, "status": "cancelled"}
])

print("eq:", doc("orders").where("status").eq("delivered").count())     # 2
print("ne:", doc("orders").where("status").ne("cancelled").count())     # 3
print("gt:", doc("orders").where("total").gt(100).count())              # 1
print("gte:", doc("orders").where("total").gte(100).count())            # 2
print("lt:", doc("orders").where("total").lt(70).count())               # 1
print("lte:", doc("orders").where("total").lte(70).count())             # 2
print("in_:", doc("orders").where("status").in_(["pending", "cancelled"]).count())  # 2
print("nin:", doc("orders").where("status").nin(["cancelled"]).count())             # 3
print("matches:", doc("users").where("email").matches(".*@b.com").first())          # {'id': 2, ...}
print("exists:", doc("orders").where("total").exists().count())         # 4

print("=== TEST: match_any(), match_all(), not_any() ===")
q1 = doc("orders").match_any(
    lambda q: q.where("status").eq("pending"),
    lambda q: q.where("total").gt(120)
)
print("match_any:", q1.count())  # 2

q2 = doc("orders").match_all(
    lambda q: q.where("status").ne("cancelled"),
    lambda q: q.where("total").gt(60)
)
print("match_all:", q2.count())  # 2

q3 = doc("orders").not_any(
    lambda q: q.where("status").eq("cancelled"),
    lambda q: q.where("status").eq("pending")
)
print("not_any:", q3.count())  # 2 (delivered only)

print("=== TEST: lookup() + merge() ===")
result = (
    doc("orders")
    .lookup("users", local_key="user_id", foreign_key="id", as_field="user")
    .merge(lambda o: {"customer": o["user"]["name"]})
    .run()
)
print(result)  # Expected: Each order has 'customer' field added

print("=== TEST: update(), delete(), replace() ===")
doc("orders").where("status").eq("pending").update({"status": "shipped"})
print(doc("orders").where("status").eq("shipped").count())  # 1

doc("orders").where("status").eq("cancelled").delete()
print(doc("orders").count())  # 3 (one cancelled removed)

doc("orders").where("order_id").eq(103).replace({"order_id": 103, "user_id": 3, "total": 175, "status": "delivered"})
print(doc("orders").where("order_id").eq(103).first())  # total: 175

print("=== TEST: Aggregates (sum, avg, min, max) ===")
print("sum:", doc("orders").sum("total"))   # 100 + 175 + 70 = 345
print("avg:", doc("orders").avg("total"))   # 345 / 3 = 115.0
print("min:", doc("orders").min("total"))   # 70
print("max:", doc("orders").max("total"))   # 175

print("=== TEST: first(), count(), all(), all_docs(), export(), import_() ===")
print("first user:", doc("users").where("name").matches(".*i.*").first())  # Match Mrittika
print("user count:", doc("users").count())  # 3
print("all users:", doc("users").all_docs())  # All users
doc("users").export("users_test.json")
doc("users").clear()
doc("users").import_("users_test.json")
print("imported user count:", doc("users").count())  # 3 again

print("=== TEST: DocList .to_json(), .as_list(), __repr__() ===")
users_result = doc("users").where("id").gt(1).run()
print(users_result)               # Formatted table output
users_result.to_json("filtered_users.json")
print("Raw list:", users_result.as_list())  # [{'id': 2, ...}, ...]
