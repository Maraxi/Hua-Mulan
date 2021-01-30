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


## Simple querying

For simple querying create an instance of class `IndexConnector` and call method `query_index()` as seen in main.py

## Doc2Query
- doc2query base model from https://github.com/castorini/docTTTTTquery is running in a docker container in the tira network, needs to be extended with get api
- for running download https://git.uwaterloo.ca/jimmylin/doc2query-data/raw/master/T5-passage/t5-base.zip and unzip in  `Hua-Mulan/doc2query/`

