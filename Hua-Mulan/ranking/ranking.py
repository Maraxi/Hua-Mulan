import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import time
from flask import Flask, request
import torch

print(torch.cuda.is_available(), flush=True)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


app = Flask(__name__)
tokenizer = AutoTokenizer.from_pretrained("amberoad/bert-multilingual-passage-reranking-msmarco")
model = AutoModelForSequenceClassification.from_pretrained("amberoad/bert-multilingual-passage-reranking-msmarco").to(device)

def removequotes(input):
    output = input.replace("'", "")
    return output.replace('"', '')

def createQueryArgumentScore(argumentlist):
    pt_batch = tokenizer(
        argumentlist,
        padding=True,
        truncation=True,
        max_length=512,
        return_tensors="pt"
    ).to(device)

    output = model(**pt_batch)
    torch.cuda.empty_cache()
    consensus = F.softmax(output[0], dim=-1)
    outputscore = [consensus[0][1].item() for element in consensus]

    return outputscore

def new_arg(argument, query):
    start = time.time()
    arg = argument["_source"]["premises"] + argument["_source"]["conclusion"]
    argument["_score"] = createQueryArgumentScore(query, arg)
    stop = time.time()
    return argument

def concatargument(argument, score):
    argument["_score"] = score
    return argument

def rank(arguments, query, batchsize):
    print("applying Bert reranking")
    query = removequotes(query)
    argumentlist = []
    results = []
    for arg in arguments:
        element = []
        element.append(query)
        element.append(removequotes(arg["_source"]["premises"] + arg["_source"]["conclusion"]))
        argumentlist.append(element)

    runs = int(len(argumentlist) / batchsize)
    if (len(argumentlist) % batchsize != 0):
        runs = runs +1
    for x in range(runs):
        results = results + createQueryArgumentScore(argumentlist[x * batchsize : (x+1) * batchsize])
    r = [concatargument(arguments[i], results[i]) for i in range(len(arguments))]


    return r




@app.route("/api/ranking", methods = ['POST'])
def hello():
    data = request.get_json()
    args = data["args"]
    query = data["query"]
    print(len(args), flush=True)
    start = time.time()
    dat = rank(args, query, 2)
    stop = time.time()
    print(stop-start, flush=True)
    return dat

app.run(port=5000, debug=True, host='0.0.0.0')