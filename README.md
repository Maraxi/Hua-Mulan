# Hua-Mulan


## Data

Download data from https://zenodo.org/record/3734893#.X5BreS337OQ and unzip in `data/`

For data analysis run following commands in `exploration/data/`
```
$ docker-compose build
$ docker-compose up
```

## Indexing

For starting and indexing with elasticsearch run following commands in  `.`

```
$ docker-compose build
$ docker-compose up
```

Then setup a python virtual environment with pipenv and activate it
```
$ pipenv sync
$ pipenv shell
```
Index the data with:
```
$ python indexing/index.py
```
Elasticsearch index will be running on `localhost:9200` and save data to `indexing/elasticsearch_data/`.

## Simple querying

For simple querying create an instance of class `IndexConnector` and call method `query_index()` as seen in main.py

