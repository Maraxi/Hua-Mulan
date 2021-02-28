# Hua-Mulan

## Preprocessing

`Hua-Mulan/preprocessing` contains all files needed to reproduce the document expansion. Note that the notebook for gpt2 and t5 expansion was executed in googlecolab on gpu. To reproduce, it is necessary to add the corresponding model files from the docT5query repository https://github.com/castorini/docTTTTTquery

## Data

Download data from https://wolke.reinlach.de/s/kfGH6m3mBEdoRWQ and unzip in `Hua-Mulan/indexing`


### Start searchengin

If you have not build the directory for the elasticsearch index, run the following comand in `Hua-Mulan/`

```
$ mkdir indexing/elasticsearch_data
```


To start the searchengine run the following commands in `Hua-Mulan/`

!! Note !! This will immediately trigger indexing, which can take up to a couple of hours. You can specify the indices you want to index in `Hua-Mulan/index.py` line 7, by removing the unwanted indices.


```
$ docker-compose build
$ docker-compose up
```


## Query Expansion

### Creating idf and vocabulary

Make sure that `args_expanded.tsv` is in `Hua-Mulan/indexing/`
Run `docker exec python python query_expansion/generate_idf.py`

## Simple querying

For simple querying create an instance of class `IndexConnector` and call method `query_index()` as seen in main.py

## Doc2Query
- doc2query base model from https://github.com/castorini/docTTTTTquery is running in a docker container in the tira network, needs to be extended with get api
- for running download https://git.uwaterloo.ca/jimmylin/doc2query-data/raw/master/T5-passage/t5-base.zip and unzip in  `Hua-Mulan/doc2query/`
- While the docker container is running. You can obtain a query corresponding to a string by sending it to localholst:5000/api/doc2query?arg=SOMESTRING



## Runing code queries against the index using docker
Check if the container is running and healthy by inspecting the output of
```
docker ps
```
We can connect to a container or run code inside by executing
```
docker exec (containername) (command with additional arguments)
```
For example inspect the python container with
```
docker exec python bash
```
Or run the the script which reads querys from topics.xml and writes output with
```
docker exec python python runTira.py -i /media -o /tmp -de args_original -qe 0 -r 0 
```
With the flags refering to the following parameters:     
qe: query expansion, integer indicating the number of words to add  
de: document expansion, refers to the name of the index  
r: whether or not ranking should be applied, integer. Please note that reranking can take up to a couple of hours when executed on cpu. A version of the system with the ranking componen running on gpu is on another branch. Documentation will be added soon.