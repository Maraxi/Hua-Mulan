# Hua-Mulan

## Python virtual environment

To run the python scripts with the correct dependencies installed go to `Hua-Mulan/` and execute
```
$ pipenv sync
$ pipenv shell
```
This installes needed modules specified in the `Piplock` file and starts a shell with the correct environment.

## Data

Download data from https://zenodo.org/record/3734893#.X5BreS337OQ and unzip in `data/`

### Data analysis

Run the following commands in `Hua-Mulan/exploration/`
```
$ docker-compose build
$ docker-compose up
```
Open one of the links given in the output and edit the Jupyter Notebook in a browser.

## Indexing

For starting and indexing with elasticsearch run following commands in `Hua-Mulan/`

```
$ docker-compose build
$ docker-compose up
```
Elasticsearch index will be running on `localhost:9200` and save data to `elasticsearch_data/`.

Index the data with:
```
$ python indexing/index.py
```

NEW: 
For Indexing with DirichletLM, please create corresponding index with following shell put

```
curl -X PUT "localhost:9200/args-lm-dirichlet?pretty" -H 'Content-Type: application/json' -d'
{
            "settings": {
                "index": {
                    "similarity": {
                        "lm-dirichlet": {
                            "type": "LMDirichlet"
                        }
                    }
                }
            }
        }
'
```


## Simple querying

For simple querying create an instance of class `IndexConnector` and call method `query_index()` as seen in main.py

## Doc2Query
- doc2query base model from https://github.com/castorini/docTTTTTquery is running in a docker container in the tira network, needs to be extended with get api
- for running download https://git.uwaterloo.ca/jimmylin/doc2query-data/raw/master/T5-passage/t5-base.zip and unzip in  `Hua-Mulan/doc2query/`
- While the docker container is running. You can obtain a query corresponding to a string by sending it to localholst:5000/api/doc2query?arg=SOMESTRING

## Runing code inside docker
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
docker exec python python runTira.py -i /media -o /tmp
```
