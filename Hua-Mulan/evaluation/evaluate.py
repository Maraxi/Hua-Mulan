import xml.etree.ElementTree as ET
import requests
import json
from ndcg import Evaluator

dir = __file__[:__file__.index('Hua-Mulan')]
tree = ET.parse(f'{dir}/Hua-Mulan/Hua-Mulan/evaluation/topics.xml')
root = tree.getroot()

result = []
for elem in root:
        r = requests.get('http://127.0.0.1:5000/api/query?arg=' + elem[1].text)
        json_data = json.loads(r.text)
        for arg in json_data:
            result.append({"query": elem[1].text,
                           "nr": elem[0].text,
                           "arg_id": arg["_source"]["id"],
                           "score": arg["_score"]})

evaluator = Evaluator()
for doc in result.values():
    print(doc[0]['nr'], evaluator.ndcg(doc))