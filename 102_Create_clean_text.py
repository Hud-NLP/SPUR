import NeoQuery, nltk
from   datetime import datetime
from Functions import msg, clean_text

'''def msg(*text_items):
    text_to_show = ""
    for each_item in text_items:
        text_to_show += str(each_item) + " "
    time_now = str(datetime.now().strftime("%H:%M:%S"))
    print("=== %s %s" %(time_now, text_to_show))

def clean_text(sentence):
    sentence  = sentence.lower()
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    new_words = tokenizer.tokenize(sentence)
    result    = ""
    for each_word in new_words:
        result += (each_word  + " ")
    result = result[:-1]
    return result'''

node_type = "goal"
existing_text_label = "detail"
clean_text_label = existing_text_label + "_clean"

msg("Creating queries")
query1  = NeoQuery.NeoQuery("bolt://localhost", "neo4j", "neo4jj")
query2  = NeoQuery.NeoQuery("bolt://localhost", "neo4j", "neo4jj")

query1.set(f"match(x:{node_type}) return x.id, x.{existing_text_label}")
query1.runQuery()

msg("Running first query")
results = query1.getResultsArray()
print(f"Number of results found {len(results)}")

for each_result in enumerate(results):
    id = each_result[1][0]
    text = each_result[1][1]
    print(f"{id}\t{text}")
    query_to_run = f"match(x:{node_type}) where x.id = {id} set x.{clean_text_label} = '{clean_text(text)}'"
    query2.set(query_to_run)
    query2.runQuery()
    print(query_to_run)

query1.close()
query2.close()

