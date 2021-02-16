from indexing.index_connector import IndexConnector
import pandas as pd
import time

time.sleep(30)

indices = ["args_t5expansion", "args_gpt2expansion", "args_original", "args_naiveexpansion"]
file = "pred/indexing/args_expanded.tsv"

conn = IndexConnector()
data = pd.read_csv(file, sep="\t")

for index in indices:

    # check if index already exists, if not, create
    if not conn.exists(index):
        conn.create_index(index)

    # check if index is empty, if yes: bulk load data
    if conn.count(index) == 0:
        df = data[["id", "conclusion", "stance", index]]
        df.columns = ["id", "conclusion", "stance", "premises"]
        df = df.fillna("NEU")
        print(f"Now indexing {index}...")
        conn.index_bulk(df, index)

print("Finish indexing...")
