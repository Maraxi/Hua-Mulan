import json
from indexing.IndexConnector import IndexConnector
from elasticsearch import Elasticsearch
import os

es = Elasticsearch()
indexing = False



conn = IndexConnector("localhost", "9200", "args")
dir = "data/"


#result = conn.query_index("nuclear power or solar energy")
# for arg in result["hits"]["hits"]:
#     print(arg)

if indexing:
    for file in os.listdir(dir):

        with open(dir+file) as file:
            data = json.load(file)

            for arg in data["arguments"]:
                conn.add_document(arg)
