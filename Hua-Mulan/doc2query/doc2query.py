import torch
from transformers import T5Config, T5Tokenizer, T5ForConditionalGeneration

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

tokenizer = T5Tokenizer.from_pretrained('t5-base')
config = T5Config.from_pretrained('t5-base')
model = T5ForConditionalGeneration.from_pretrained(
    'doc2query/model.ckpt-1004000', from_tf=True, config=config)
model.to(device)



def predictqueryfromdoc(doc):
    input_ids = tokenizer.encode(doc, return_tensors='pt').to(device)
    outputs = model.generate(
        input_ids=input_ids,
        max_length=64,
        do_sample=True,
        top_k=10,
        num_return_sequences=3)
    return tokenizer.decode(outputs[1], skip_special_tokens=True)


