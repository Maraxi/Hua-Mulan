import json
from indexing.IndexConnector import IndexConnector
from elasticsearch import Elasticsearch
import os
import ijson

es = Elasticsearch()
indexing = False

conn = IndexConnector("localhost", "9200", "args")
dir = "data/"



result = conn.query_index("nuclear power or solar energy", 100)
for arg in result["hits"]["hits"]:
    print(arg)


if indexing:
    #iterate over each file in directory
    for file in os.listdir(dir):
        # generate auxiliary structures
        doc = {}
        prem = []
        arg = {}
        # read json as stream and catch each relevant key and create argument
        for prefix, type_of_object, value in ijson.parse(open(dir + file)):

            if prefix == "arguments.item.id":
                doc.update({"id": value})
            if prefix == "arguments.item.conclusion":
                doc.update({"conclusion": value})
            if prefix == "arguments.item.premises.item.text":
                arg.update({"text": value})
            if prefix == "arguments.item.premises.item.stance":
                arg.update({"stance": value})
                prem.append(arg)
                arg = {}
            if prefix == "arguments.item.context.discussionTitle":
                doc.update({"premises": prem})
                doc.update({"discussionTitle": value})
            # last relevant key is sourceURL, afterwards reset auxiliary structures and send doc to es
            if prefix == "arguments.item.context.sourceUrl":
                doc.update({"souceURL": value})
                conn.add_document(doc)
                doc = {}
                prem = []
