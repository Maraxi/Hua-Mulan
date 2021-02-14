from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import os
import ijson

dir = os.path.dirname(os.path.realpath(__file__))
dir = dir[:dir.index('Hua')] + "Hua-Mulan/data/"
data = ['debateorg.json',
        'debatepedia.json',
        'debatewise.json',
        'idebate.json',
        'parliamentary.json']

def gen():
    for json_file in data:
        with open(dir+json_file, 'r') as dat:
            for index, argument in enumerate(ijson.items(dat, 'arguments.item')):
                #if index > 80:
                #    break
                if (index+1) % 1000 == 0:
                    print(f'served {index+1} documents from {json_file}', end='\r')
                text = [argument['conclusion'],
                        argument['premises'][0]['text'],
                        argument['context']['sourceText']
                       ]
                if 'discussionTitle' in argument['context'].keys():
                    text.append(argument['context']['discussionTitle'])
                yield " ".join(text)
            print('')

idfVectorizer = TfidfVectorizer(strip_accents='ascii', max_df=0.85, min_df=0.05, binary=True, use_idf=True)
idfVectorizer.fit(gen())

with open(f'{dir}idf.pickle', 'wb') as output:
    pickle.dump(idfVectorizer.idf_, output)
with open(f'{dir}vocabulary.pickle', 'wb') as output:
    pickle.dump(idfVectorizer.vocabulary_, output)
