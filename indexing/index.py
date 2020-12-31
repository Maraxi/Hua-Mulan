from IndexConnector import IndexConnector
import os
import ijson

conn = IndexConnector("localhost", "9200", "args")
dir = "../data/"

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
