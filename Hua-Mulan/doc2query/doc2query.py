import torch
from transformers import T5Config, T5Tokenizer, T5ForConditionalGeneration


device = torch.device('cpu')
tokenizer = T5Tokenizer.from_pretrained('t5-base')
config = T5Config.from_pretrained('t5-base')
model = T5ForConditionalGeneration.from_pretrained(
    'doc2query/model.ckpt-1004000', from_tf=True, config=config)

model.to(device)

doc_text = 'The presence of communication amid scientific minds was equally important to the success of the Manhattan Project as scientific intellect was. The only cloud hanging over the impressive achievement of the atomic researchers and engineers is what their success truly meant; hundreds of thousands of innocent lives obliterated. </s>'

input_ids = tokenizer.encode(doc_text, return_tensors='pt').to(device)
outputs = model.generate(
    input_ids=input_ids,
    max_length=64,
    do_sample=True,
    top_k=10,
    num_return_sequences=3)

for i in range(3):
    print(f'sample {i + 1}: {tokenizer.decode(outputs[i], skip_special_tokens=True)}')
