import xml.etree.ElementTree as ET
import requests
import os
import math

# Evaluate our setup with nDCG marker
class Evaluator:

    # Init with reference data
    def __init__(self):
        dir = os.path.dirname(os.path.realpath(__file__))
        with open(f'{dir}/relevance_judgements.qrels') as reference:
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




