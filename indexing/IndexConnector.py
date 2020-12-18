from elasticsearch import Elasticsearch, helpers


class IndexConnector:

    def __init__(self, host, port, index):
        self.es = Elasticsearch([{'host': host, 'port': port, 'index':index}])
        self.index = index

    def add_document(self, doc):
        res = self.es.index(index=self.index, body=doc)
        print(res['result'])

    def add_bulk(self, bulk):
        helpers.bulk(self.es, bulk)

    def get_document(self, id):
        res = self.es.get(index=self.index, id=id)
        print(res['_source'])

    def search_query(self):
        res = self.es.search(index="args", body={"query": {"match_all": {}}})
        print("Got %d Hits:" % res['hits']['total']['value'])
        for hit in res['hits']['hits']:
            print(hit["_source"])
