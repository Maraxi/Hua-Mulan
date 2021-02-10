from indexing.index_connector import IndexConnector
import pandas as pd
import time
time.sleep(30)
import requests
from urllib.request import urlopen

index = ["args_t5expansion", "args_baseline"]
file = ["exploration/data_expanded_t5.csv", "exploration/data_baseline.csv"]

conn = IndexConnector()

# index = "args_gpt2expansion"
# index = "args_naiveexpansion"
i = 1
while i==0:
    for i in range(1):

        if not conn.exists(index[i]):
            conn.create_index(index[i])

        if conn.count(index[i]) == 0:
            data = pd.read_csv(file[i], sep="\t")
            conn.index_bulk(data, index)



result = conn.query_index("Is Sexual Orientation Determined at Birth?", 10, index[0])

for hit in result["hits"]["hits"]:
    print(hit["_id"])
    print(hit["_source"]["conclusion"])