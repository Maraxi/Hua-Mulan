import flask
from flask import request, jsonify
from indexing.index_connector import IndexConnector
from retrieval.ranker import rank

dataConn = IndexConnector("localhost", "9200", "args")

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "Welcome to the API of Hua-Mulan"


@app.route('/api/query', methods=['GET'])
def api_arg():
    if 'arg' in request.args:
        result = dataConn.query_index(request.args['arg'], 10)
        return jsonify(result["hits"]["hits"])
    else:
        return "Error, invalid request"


app.run()
