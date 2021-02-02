import flask
from doc2query import predictqueryfromdoc
from flask import request, jsonify



app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "Welcome to the API of Hua-Mulan"


@app.route('/api/doc2query', methods=['GET'])
def api_arg():
    #takes something like /api/doc2query?arg=[DOCSTRING]
    if 'arg' in request.args:
        query = predictqueryfromdoc(request.args['arg'])
        return jsonify(query)
    else:
        return "Error, invalid request"

app.run(host="0.0.0.0", port=5000, debug = True, use_reloader=True)
