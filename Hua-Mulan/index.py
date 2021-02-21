from indexing.index_connector import IndexConnector
import pickle
import os
import pandas as pd
import time

indices = ["args_original","args_t5expansion", "args_gpt2expansion", "args_naiveexpansion", "args_original_bm25","args_t5expansion_bm25", "args_gpt2expansion_bm25", "args_naiveexpansion_bm25"]
file = "pred/indexing/args_expanded.tsv"
pickle_file = "pred/indexing/args_expanded.pickle"

data = None
if "args_expanded.pickle" in os.listdir("pred/indexing"):
    print('reading from pickle', flush=True)
    with open(pickle_file, "rb") as datafile:
        data = pickle.load(datafile)
else:
    print('reading from tsv', flush=True)
    data = pd.read_csv(file, sep="\t")

print("Waiting for elastic", flush=True)
time.sleep(30)

conn = IndexConnector()
for index in indices:
    print(f"Checking {index}", flush=True)

    sim = "bm25" if "bm25" in index else "lmdirichlet"
    # check if index already exists, if not, create
    if not conn.exists(index):
        conn.create_index(index, sim)

    # check if index is empty, if yes: bulk load data
    if conn.count(index) == 0:
        df = data[["id", "conclusion", "stance", index.replace("_bm25", "")]]
        df.columns = ["id", "conclusion", "stance", "premises"]
        df = df.fillna("NEU")
        conn.index_bulk(df, index)


print("Finish indexing...", flush=True)
