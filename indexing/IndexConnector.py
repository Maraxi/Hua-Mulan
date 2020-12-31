from elasticsearch import Elasticsearch, helpers


class IndexConnector:

    def __init__(self, host, port, index):
        self.es = Elasticsearch([{'host': host, 'port': port, 'index': index}])
        self.index = index

    def count(self):
        return self.es.count()

    def add_document(self, doc):
        res = self.es.index(index=self.index, body=doc)
        print(res)

    def add_bulk(self, bulk):
        helpers.bulk(self.es, bulk)

    def get_document(self, id):
        res = self.es.get(index=self.index, id=id)
        print(res['_source'])

    def query_index(self, querystring, size):
        res = self.es.search(index="args",
                             body={"size": size,
                                   "query":
                                       {"query_string":
                                            {"query": querystring
                                             }}})
        return res