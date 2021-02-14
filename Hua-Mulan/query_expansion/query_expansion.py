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

    def load_pickle(self):
        with open('query_expansion/idf.pickle', 'rb') as idf:
            self.idf = pickle.load(idf)
        with open('query_expansion/vocabulary.pickle', 'rb') as vocab:
            self.vocab = pickle.load(vocab)

    def rank_searchterms(self, count=5):
        ks = [5,10,20,40]
        results = []
        for k in ks:
            vectorizer = CountVectorizer(strip_accents='ascii', vocabulary=self.vocab)
            res = vectorizer.fit_transform([" ".join(self.relevant[:k])])
            res = res.toarray()[0]
            res = map(lambda x: x+0.001, res)
            res = list(map(math.log, res))
            results.append(res)
        results = zip(*results)
        results = list(map(sum, results))
        scores = results * self.idf
        scored_words = [(scores[index], word) for word, index in self.vocab.items()]
        scored_words.sort(reverse=True)
        print(scored_words[:count], flush=True)
        return [word for _,word in scored_words[:count]]

