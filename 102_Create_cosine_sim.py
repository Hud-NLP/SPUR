import NeoQuery
from Functions import msg, cosine_sim

node_1_type  = "sub_activity"
node_2_type  = "goal"
node_1_field = "sa_clean"
node_2_field = "detail_clean"

msg(f"Program to create cosine similarity relationships in Neo4j, comparing {node_1_type}.{node_2_field} <with> {node_2_type}.{node_2_field}")

msg("Creating Neo4j queries")
query1  = NeoQuery.NeoQuery("bolt://localhost", "neo4j", "neo4jj")

msg("Getting data for first array")
query1.set(f"match(x:{node_1_type}) return x.id, x.{node_1_field}")
query1.runQuery()
first_array = query1.getResultsArray()

msg("Getting data for second array")
query1.set(f"match(x:{node_2_type}) return x.id, x.{node_2_field}")
query1.runQuery()
second_array = query1.getResultsArray()

msg("Started cross-matching")
for item_1 in first_array:
    for item_2 in second_array:
        id_1   = item_1[0]
        text_1 = item_1[1]
        id_2   = item_2[0]
        text_2 = item_2[1]
        if (not node_1_type == node_2_type) or (not id_1 == id_2):              # Don't create a relationship between a node and itself
            cosine_similarity = cosine_sim(text_1, text_2)
            if cosine_similarity > 0:
                query1.set(f"match (x1:{node_1_type}) where x1.id = {id_1}")
                query1.add(f"match (x2:{node_2_type}) where x2.id = {id_2}")
                query1.add(f"merge (x1)-[c:cosine]->(x2) set c.cosine = {cosine_similarity}")
                print(query1.get())
                query1.runQuery()

msg("Closing Neo4j query")
query1.close()
msg("Finished")

# Cypher to delete cosine relationships:
# match(sa:sub_activity)-[:sub_activity]->(ra:research_activity)-[c:cosine]-(sa) delete c
