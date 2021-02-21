import pandas
import pickle

print('opening args_expanded.tsv')
data = pandas.read_csv("args_expanded.tsv", sep="\t")
with open("args_expanded.pickle", "wb") as output:
    print('writing to args_expanded.pickle')
    pickle.dump(data,output)
print('done')
