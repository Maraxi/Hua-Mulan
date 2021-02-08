from indexing.index_connector import IndexConnector
from retrieval.ranker import rank

conn = IndexConnector("args")

result = conn.query_index("nuclear power or solar energy", 100)
for arg in rank(result["hits"]["hits"]):
    print(arg)
