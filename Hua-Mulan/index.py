from indexing.index_connector import IndexConnector
import pandas as pd
import time

time.sleep(30)

indices = ["args_original","args_t5expansion", "args_gpt2expansion", "args_naiveexpansion", "args_original_bm25","args_t5expansion_bm25", "args_gpt2expansion_bm25", "args_naiveexpansion_bm25"]
file = "pred/indexing/args_expanded.tsv"


conn = IndexConnector()
data = pd.read_csv(file, sep="\t")

for index in indices:

    sim = "bm25" if "bm25" in index else "lmdirichlet"
    # check if index already exists, if not, create
    if not conn.exists(index):
        conn.create_index(index, sim)

    # check if index is empty, if yes: bulk load data
    if conn.count(index) == 0:
        df = data[["id", "conclusion", "stance", index.replace("_bm25", "")]]
        df.columns = ["id", "conclusion", "stance", "premises"]
        df = df.fillna("NEU")
        print(f"Now indexing {index}...")
        conn.index_bulk(df, index)


print("Finish indexing...")
