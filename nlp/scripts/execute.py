from transformers import pipeline, BertForSequenceClassification, BertTokenizerFast

model_path = "./nlp/models/torch-bert-base-uncased-model"
#model_path = "../models/torch-bert-base-uncased-model"

model = BertForSequenceClassification.from_pretrained(model_path)
tokenizer= BertTokenizerFast.from_pretrained(model_path)
nlp= pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

text = "Recently, I've been feeling very anxious and overwhelmed at work. It's started to affect my sleep and my relationships. I don't feel like it's an emergency, but I could really use some advice on how to manage this stress."

print(nlp(text))

def do_nlp(text):
    nlp = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
    return nlp

print(do_nlp(text))