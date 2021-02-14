from elasticsearch import Elasticsearch, helpers
import requests

host = "elastic"


class IndexConnector:

    def __init__(self, host_name="elastic"):
        host = host_name
        connection = False
        while not connection:
            try:
                connection = True
                response = requests.request("GET", "http://" + host +":9200")
            except Exception:
                connection = False

        self.es = Elasticsearch([{'host': host, 'port': "9200"}])
        print(self.es.ping())
        print("connection established!")

    def ping(self):
        if self.es.ping():
            return True
        return False

    def count(self, index):
        return int(self.es.cat.count(index, params={"format": "json"})[0].get("count"))

    @classmethod
    def update(cls, index):
        cls.es = Elasticsearch([{'host': host, 'port': "9200", 'index': index}])

    def create_index(self, index):
        request_body = {
            'settings': {
                'similarity': {
                    'lmdirichlet': {'type': 'LMDirichlet'}
                },
                'analysis': {
                    'normalizer': {
                        'norm': {'type': 'custom', 'filter': ['lowercase', 'asciifolding']}
                    }
                }
            },
            'mappings': {
                'properties': {
                    'premises': {'type': 'text', 'similarity': 'lmdirichlet',
                                 'fields': {'kw': {'type': 'keyword', 'normalizer': 'norm', 'ignore_above': 32766}}},
                    'stance': {'type': 'keyword'},
                    'conclusion': {'type': 'text'},
                    'context.sourceUrl': {'type': 'keyword'}
                }
            }
        }
        print("creating " + index + " index...")
        self.es.indices.create(index=index, body=request_body)
        self.update(index)

    def exists(self, index):
        if self.es.indices.exists(index=index):
            return True
        return False

    def add_document(self, doc, index):
        res = self.es.index(index=index, body=doc)
        print("created")

    def index_data_generator(self, data, index):
        for i, row in data.iterrows():
            yield {
                "_index": index,
                "_id": row["id"],
                "_source": {
                    'premises': row["premises"],
                    'stance': row["stance"],
                    'conclusion': row["conclusion"],
                    'context.sourceUrl': row["context.sourceUrl"]

                }
            }

    def index_bulk(self, data, index):
        helpers.bulk(self.es, self.index_data_generator(data, index))

    def get_document(self, id, index):
        res = self.es.get(index=index, id=id)
        print(res['_source'])

    def query_index(self, querystring, size, indexname):
        res = self.es.search(index=indexname,
                             body={"size": size,
                                   "query":
                                       {"query_string":
                                            {"query": querystring
                                             }}})
        return res
