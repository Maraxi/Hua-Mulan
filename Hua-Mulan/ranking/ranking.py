import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import time

tokenizer = AutoTokenizer.from_pretrained("amberoad/bert-multilingual-passage-reranking-msmarco")
model = AutoModelForSequenceClassification.from_pretrained("amberoad/bert-multilingual-passage-reranking-msmarco")

def removequotes(input):
    output = input.replace("'", "")
    return output.replace('"', '')

def createQueryArgumentScore(query, argument):
    queryClean = removequotes(query)
    argumentClean = removequotes(argument)
    pt_batch = tokenizer(
        [[queryClean, argumentClean]],
        padding=True,
        truncation=True,
        max_length=512,
        return_tensors="pt"
    )
    output = model(**pt_batch)
    consensus = F.softmax(output[0], dim=-1)
    outputscore = consensus[0][1].item()

    return outputscore

def new_arg(argument, query):
    start = time.time()
    arg = argument["_source"]["premises"] + argument["_source"]["conclusion"]
    argument["_score"] = createQueryArgumentScore(query, arg)
    stop = time.time()
    return argument

def rank(arguments, query):
    print("applying Bert reranking")
    results = [new_arg(argument, query) for argument in arguments]

    return results


