import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForSequenceClassification

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