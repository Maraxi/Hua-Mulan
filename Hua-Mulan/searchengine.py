import flask
from flask import request, jsonify
from indexing.index_connector import IndexConnector
import sys
import time


conn = IndexConnector()

app = flask.Flask(__name__)
app.config["DEBUG"] = True

print("Searchengine can be contacted on Port 5000")

@app.route('/', methods=['GET'])
def home():
    return "Welcome to the API of Hua-Mulan"


@app.route('/api/query', methods=['GET'])
def api_arg():
    if 'arg' in request.args and 'index' in request.args:
        print(request.args["index"], flush=True)
        result = conn.query_index(request.args["arg"], 10, request.args["index"])
        return jsonify(result["hits"]["hits"])
    else:
        return "Error, invalid request"


app.run(port=5000, debug=True, host='0.0.0.0')
