# Hua-Mulan


## Data

Download data from https://zenodo.org/record/3734893#.X5BreS337OQ and unzip in `data/`

For data analysis run following commands in `exploration/data/`
```
$ docker-compose build
$ docker-compose up
``` 

For starting and indexing with elasticsearch run following commands in  `.`

```
$ docker-compose build
$ docker-compose up
``` 

Than create pipenv using pipfile and run main.py. Elasticsearch index will be running on `localhost:9200` and save data to `indexing/elasticsearch_data/`.