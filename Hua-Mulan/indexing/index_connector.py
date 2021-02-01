from elasticsearch import Elasticsearch, helpers


class IndexConnector:

    def __init__(self, index):
        self.es = Elasticsearch([{'host': "localhost", 'port': "9200", 'index': index}])
        self.index = index

    def count(self):
        return int(self.es.cat.count(self.index, params={"format": "json"})[0].get("count"))

    @classmethod
    def update(cls, index):
        cls.es = Elasticsearch([{'host': "localhost", 'port': "9200", 'index': index}])

    def create_index(self, index, similarity):
        request_body = {
            "settings": {
                "index": {
                    "similarity": {
                        "lm-dirichlet": {
                            "type": similarity
                        }
                    }
                }
            }
        }
        print("creating 'example_index' index...")
        self.es.indices.create(index=index, body=request_body)
        self.update(index)


    def add_document(self, doc):
        res = self.es.index(index=self.index, body=doc)
        print("created")

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
