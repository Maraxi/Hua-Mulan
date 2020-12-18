import json
from indexing.IndexConnector import IndexConnector
from elasticsearch import Elasticsearch
import os

es = Elasticsearch()

conn = IndexConnector("localhost", "9200", "args")
dir = "data/"


for file in os.listdir(dir):

    with open(dir+file) as file:
        data = json.load(file)

        for arg in data["arguments"]:
            conn.add_document(arg)
