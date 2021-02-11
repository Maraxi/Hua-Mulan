from index_connector import IndexConnector
import pandas as pd
import time

time.sleep(30)

index = ["args_t5expansion", "args_baseline", "args_naiveexpansion"]
file = ["data/data_expanded_t5_3queries.csv", "data/data_baseline.csv", "data/data_naiveexpansion.csv"]

conn = IndexConnector()


if not conn.exists(index[0]):
    conn.create_index(index[0])

if conn.count(index[0]) == 0:
    data = pd.read_csv(file[0], sep="\t")
    conn.index_bulk(data, index)

print("Finish indexing...")
