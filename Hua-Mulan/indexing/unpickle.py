import pickle
import pandas

print('open')
with open("args_expanded.pickle", "rb") as inp:
    data = pickle.load(inp)
    print(len(data))
