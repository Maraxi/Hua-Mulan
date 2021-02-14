import xml.etree.ElementTree as ET
import requests
import json
from ndcg import Evaluator
import os
import time

dir = os.path.dirname(os.path.realpath(__file__))
print(dir)
tree = ET.parse(f'{dir}/topics.xml')
root = tree.getroot()

index = "args_t5expansion"
host = "http://searchengine"

index = ["args_t5expansion"]

def connect():
    connected = False
    while not connected:
        try:
            for ind in index:
                count = requests.request("GET", f"http://elastic:9200/{ind}/_count?")
                if json.loads(count.text)["count"] != 382545:
                    raise Exception

            print("Evaluation starting...", flush=True)
            connected = True
        except Exception:
            connected = False
            print("Evaluation is waiting for searchengine ...", flush=True)
            time.sleep(20)

def evaluate():
    result = {}
    for elem in root:
        r = requests.get(host + ":5000/api/query?arg=" + elem[1].text + "&index=" + index[0])
        json_data = json.loads(r.text)
        result[elem[0].text] = []
        for arg in json_data:
            result[elem[0].text].append({"query": elem[1].text,
                                         "nr": elem[0].text,
                                         "arg_id": arg["_id"],
                                         "score": arg["_score"]})

    evaluator = Evaluator()
    for doc in result.values():
        print(doc[0]['nr'], evaluator.ndcg(doc))

def expand_query():
    for elem in root:
        print(f"{elem[1].text}")
        r = requests.get(f"{host}:5000/api/expand?arg={elem[1].text}&index={index[0]}&terms=10")
        print(r.text)

connect()
evaluate()
expand_query()
