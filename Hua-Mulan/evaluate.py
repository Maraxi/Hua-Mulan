import pandas as pd
from elasticsearch import Elasticsearch
import os
import argparse
import xml.etree.ElementTree as ET
import numpy as np
import json
import requests
from indexing.index_connector import IndexConnector
from time import sleep, time
#import ranking.ranking as ranking

if __name__ == "__main__":
    print('Starting Tira run script')

    # GET CONFIG
    config = []
    with open('run_config.json', 'r') as conf:
        config = json.load(conf)

    # PARSE ARGUMENTS
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input-dir")
    parser.add_argument("-o", "--output-dir")
    parser.add_argument("-qe", "--query-expansion")
    parser.add_argument("-de", "--doc-expansion")
    parser.add_argument("-r", "--ranking")
    parser.add_argument("-n", "--name")
    args = parser.parse_args()
    args = vars(args)

    # GIVE THE CONTAINERS TIME TO REACH A STEADY STATE
    sleep(2)

    # CONNECT TO ELASTICSEARCH NODE
    container_name = config['elastic_host_container_name']
    conn = IndexConnector(container_name)

    # SANITY CHECK
    print(conn.ping())

    # HANDLE I/O
    input_dir = args['input_dir']
    output_dir = args['output_dir']
    index = args['doc_expansion']
    ranking = args['ranking']
    name = args['name']
    queryexpansion = args['query_expansion']

    # MAKE SURE THE OUTPUT DIRECTORY EXISTS
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    print(index, flush=True)
    print(queryexpansion, flush=True)
    # LOAD THE TOPICS FROM THE INPUT DIRECTORY
    print("LOADING TOPICS")
    tree = ET.parse(os.path.join(input_dir, 'topics.xml'))
    root = tree.getroot()
    topics = []
    for child in root:
        d = {'topic_number': int(child[0].text), 'topic_query': child[1].text}
        topics.append(d)
    topics = pd.DataFrame(topics)

    # ITERATE THROUGH TOPICS AND EXECUTE SEARCH
    for _, row in topics.iterrows():
        number = row['topic_number']
        query = row['topic_query']

        print(f'Now working on query {number}: {query}')
        if queryexpansion != "None":
            # add expansion to query here
            print("no method implemented")
        # query
        response = conn.query_index(query, 1000, index)['hits']['hits']

        # apply bert reranking
        if ranking ==1:
            response = requests.post('http://localhost:5000/api/ranking', json=response)

        #response = ranking.rank(response, query, 15)
        # STORE RESULTS IN DICTIONARY
        results = dict()
        for hit in response:
            results[hit['_id']] = hit['_score']

        # CONVERT DICTIONARY TO TREC-STYLE DATAFRAME
        final_ranks = pd.DataFrame(list(results.items()), columns=['arg_ids', 'score'])
        final_ranks = final_ranks.sort_values(by='score', ascending=False)
        final_ranks['rank'] = np.arange(len(final_ranks)) + 1
        final_ranks['method'] = f"{index}_{queryexpansion}"
        final_ranks['Q0'] = "Q0"
        final_ranks['topic_number'] = number

        # APPEND CURRENT DATAFRAME TO OUTPUT FILE
        with open(f'{output_dir}/{name}.txt', 'a+') as f:
            final_ranks[['topic_number', 'Q0', 'arg_ids', 'rank', 'score', 'method']].to_csv(f, sep=' ', header=False,
                                                                                             index=False)

        # LOOK AT WHAT WAS ACTUALLY WRITTEN TO FILE
        print(final_ranks)
