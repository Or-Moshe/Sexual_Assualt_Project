from transformers import pipeline, BertForSequenceClassification, BertTokenizerFast
import pandas as pd
from nlp.scripts.preprocessing import Preprocessing
from nlp.scripts.translate import Translate
#model_path = "./nlp/models/torch-bert-base-uncased-model"
#model_path = "../models/torch-bert-base-uncased-model"

csv_path = "C:/Users/Lenovo/studies/final project/withoutClassification.csv"

text = "Recently, I've been feeling very anxious and overwhelmed at work. It's started to affect my sleep and my relationships. I don't feel like it's an emergency, but I could really use some advice on how to manage this stress."


def classify_file():
    df = pd.read_csv(csv_path)
    preprocessing = Preprocessing(df)
    preprocessing.process_dataframe()
    print(preprocessing.df.head())
    translate = Translate(preprocessing.df)
    print(translate.translate_dataframe())

def do_nlp(text, model_path):
    try:
        model = BertForSequenceClassification.from_pretrained(model_path)
        tokenizer = BertTokenizerFast.from_pretrained(model_path)
        nlp = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
        result = nlp(text)
        return result
    except Exception as e:
        print(e)
        return None



#print(do_nlp(text))
#classify_file()