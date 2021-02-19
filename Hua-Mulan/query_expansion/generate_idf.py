from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import os

datafile = 'indexing/args_expanded.tsv'
with open(datafile) as data:
    header = data.readline()
    header = header[:-1].split("\t")
    indices = header[3:]

def gen(index):
    with open(datafile, 'r') as data:
        data.readline()
        for i, line in enumerate(data):
            line_arr = line[:-1].split('\t')
            while len(line_arr)<7:
                line = line + next(data)
                line_arr = line[:-1].split('\t')
            if (i+1)%500 == 0:
                print(f'yielded {i+1} documents from {indices[index]}', end='\r', flush=True)
            yield f'{line_arr[1]} {line_arr[3+index]}'
        print(f'yielded {i+1} documents from {indices[index]}', flush=True)

for i, index in enumerate(indices):
    print(f'Starting {index}')
    idfVectorizer = TfidfVectorizer(strip_accents='ascii', max_df=0.85, min_df=0.05, binary=True, use_idf=True)
    idfVectorizer.fit(gen(i))

    with open(f'query_expansion/{index}_idf.pickle', 'wb') as output:
        pickle.dump(idfVectorizer.idf_, output)
    with open(f'query_expansion/{index}_vocabulary.pickle', 'wb') as output:
        pickle.dump(idfVectorizer.vocabulary_, output)
