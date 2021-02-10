from indexing.index_connector import IndexConnector
import pandas as pd
import time

time.sleep(30)

index = ["args_t5expansion", "args_baseline"]
file = ["exploration/data_expanded_t5.csv", "exploration/data_baseline.csv"]

conn = IndexConnector()

# index = "args_gpt2expansion"
# index = "args_naiveexpansion"
i = 1
while i == 0:
    for i in range(1):

        if not conn.exists(index[i]):
            conn.create_index(index[i])

        if conn.count(index[i]) == 0:
            data = pd.read_csv(file[i], sep="\t")
            conn.index_bulk(data, index)

print("Finish indexing...")
