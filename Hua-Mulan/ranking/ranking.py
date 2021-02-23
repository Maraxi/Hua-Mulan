import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import time

tokenizer = AutoTokenizer.from_pretrained("amberoad/bert-multilingual-passage-reranking-msmarco")
model = AutoModelForSequenceClassification.from_pretrained("amberoad/bert-multilingual-passage-reranking-msmarco")

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
    )
    output = model(**pt_batch)
    consensus = F.softmax(output[0], dim=-1)
    outputscore = [consensus[i][0].item() for i in range(len(consensus))]


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

