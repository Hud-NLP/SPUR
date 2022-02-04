import NeoQuery

node_type = "sub_activity"
unique_label = "sa"

query1  = NeoQuery.NeoQuery("bolt://localhost", "neo4j", "neo4jj")
query2  = NeoQuery.NeoQuery("bolt://localhost", "neo4j", "neo4jj")

query1.set(f"match(x:{node_type}) return x.{unique_label}")
query1.runQuery()

results = query1.getResultsArray()

print(f"Createing index based on {node_type}.{unique_label}")
for counter, each_result in enumerate(results):
    query2.set(f"match(x:{node_type} {{{unique_label}:'{each_result[0]}'}}) set x.id = {counter + 1};")
    query2.runQuery()

query1.close()
query2.close()