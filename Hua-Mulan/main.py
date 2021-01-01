from indexing.index_connector import IndexConnector

conn = IndexConnector("localhost", "9200", "args")

result = conn.query_index("nuclear power or solar energy", 100)
for arg in result["hits"]["hits"]:
    print(arg)
