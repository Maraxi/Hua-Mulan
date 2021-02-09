import xml.etree.ElementTree as ET
import requests
import json
import math

# Evaluate our setup with nDCG marker
class Evaluator:

    # Init with reference data
    def __init__(self):
        dir = __file__[:__file__.index('Hua-Mulan')]
        with open(f'{dir}/Hua-Mulan/data/touche2020-task1-relevance-args-me-corpus-version-2020-04-01.qrels') as reference:
            data = reference.read()
            data = data.splitlines()
            self.data = [line.split() for line in data]

    # Find for respective topic within a document, which score does it have in our reference data
    def reference_score(self, topic, docid):
        score = [float(x[3]) for x in self.data if x[0]==topic and x[2]==docid]
        if len(score) > 0:
            return score[0]
        else:
            return -2.0

    # Get scores for respective topic
    def get_scores(self, query_results):
        return [self.reference_score(doc['nr'], doc['arg_id']) for doc in query_results]

    # DCG on respective topic
    def dcg(self, scores):
        return sum(map(lambda x: x[1]/math.log(x[0]+2,2), enumerate(scores)))

    # IDCG (optimum) on respective topic
    def idcg(self, topic, n):
        relevant = [float(doc[3]) for doc in self.data if doc[0] == topic]
        relevant.sort()
        relevant.reverse()
        relevant += [-2]*10
        return self.dcg(relevant[:n])

    # nDCG on respective topic
    def ndcg(self, query):
        scores = self.get_scores(query)
        return self.dcg(scores)/self.idcg(query[0]['nr'], len(scores))


dir = __file__[:__file__.index('Hua-Mulan')]

# This part is analogue to evaluate.py
tree = ET.parse(f'{dir}/Hua-Mulan/Hua-Mulan/evaluation/topics.xml')
root = tree.getroot()

result = {}
for elem in root:
    r = requests.get('http://127.0.0.1:5000/api/query?arg=' + elem[1].text)
    json_data = json.loads(r.text)
    result[elem[0].text] = []
    for arg in json_data:
        result[elem[0].text].append({"query": elem[1].text,
                                     "nr": elem[0].text,
                                     "arg_id": arg["_source"]["id"],
                                     "score": arg["_score"]})

evaluator = Evaluator()
for doc in result.values():
    print(doc[0]['nr'], evaluator.ndcg(doc))


