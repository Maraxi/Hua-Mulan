from index_connector import IndexConnector
import os
import ijson

conn = IndexConnector("localhost", "9200", "args")
if conn.count()['count']>0:
    print("The index is not empty")
    choice = input("Continue indexing? [y/N]")
    if choice not in 'yY':
        print("Canceled indexing")
        exit(1)

dir = __file__[:__file__.index('Hua-Mulan')]
dir = f"{dir}Hua-Mulan/data/"
files = os.listdir(dir)
files.remove(".gitkeep")

assert len(files)>0, f"Found no files to index in {dir}"

#iterate over each file in directory
for file in files:
    # generate auxiliary structures
    doc = {}
    prem = []
    arg = {}
    # read json as stream and catch each relevant key and create argument
    with open(dir+file) as jsonfile:
        for prefix, type_of_object, value in ijson.parse(jsonfile):
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
