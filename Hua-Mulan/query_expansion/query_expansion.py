from indexing.index_connector import IndexConnector
from sklearn.feature_extraction.text import CountVectorizer
import pickle
import requests
import json
import math

class Expander:
    def __init__(self, query, relevant):
        self.query = query
        self.relevant = relevant
        self.relevant = [entry['_source'] for entry in self.relevant]
        self.relevant = [" ".join(entry.values()) for entry in self.relevant]
        self.load_pickle()
        self.rank_searchterms()

    def load_pickle(self):
        with open('query_expansion/idf.pickle', 'rb') as idf:
            self.idf = pickle.load(idf)
        with open('query_expansion/vocabulary.pickle', 'rb') as vocab:
            self.vocab = pickle.load(vocab)

    def rank_searchterms(self):
        k = 10
        vectorizer = CountVectorizer(strip_accents='ascii', vocabulary=self.vocab)
        res = vectorizer.fit_transform([" ".join(self.relevant[:k])])
        self.res = res
        res = res.toarray()
        res = res[0]
        print(sorted(res))
        res = map(lambda x: x+0.01, res)
        res = list(map(math.log, res))
        #self.scores = res*self.idf
        self.scores = res

        #while k<=80:
            #pass

    def additional_terms(self, count):
        return self.best_terms[:count]

    def output(self):
        return json.dumps([str(type(self.res)),
                           self.res.shape,
                           str(type(self.idf)),
                           self.idf.shape
                          ], indent = 2)

