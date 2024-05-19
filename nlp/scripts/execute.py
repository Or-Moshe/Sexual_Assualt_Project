from transformers import pipeline, BertForSequenceClassification, BertTokenizerFast, BertTokenizer
import pandas as pd
import openpyxl
from nlp.scripts.preprocessing import Preprocessing
from nlp.scripts.translate import Translate
'''
csv_path = "../data/withoutClassification.csv"
tanslated_path = "../data/withoutClassificationTranslated.csv"
model_path = "../models/torch-bert-base-uncased-model-all-data"
result_path = "../data/withoutClassificationTranslatedResults.csv"
'''
'''
csv_path = "../data/withoutClassification.csv"
tanslated_path = "../data/withDummyTranslated_Consumer.csv"
model_path = "../models/torch-bert-base-uncased-model-all-data-consumer"
result_path = "../data/withoutClassificationTranslatedConsumerResults.csv"
'''
csv_path = "../data/withoutClassification.xlsx"
model_path = "../models/torch-bert-base-uncased-model-all-data-consumer-he"
result_path = "../data/withoutClassificationConsumerResults-he.xlsx"

column_to_predict = 'transcriptConsumer'

def classify_file():

    df = pd.read_excel(csv_path)
    preprocessing = Preprocessing(df)
    df = preprocessing.process_dataframe(column_to_predict)
    print(df.columns)
    '''
    translate = Translate(preprocessing.df)
    df = translate.translate_dataframe(tanslated_path)
    df = pd.read_csv(tanslated_path)
    df[['label', 'score']] = df['transcriptConsumer_en'].apply(lambda text: do_nlp(text, model_path)).apply(pd.Series)
    '''
    columns_to_copy = ['count', 'transcriptConsumer']
    df = df[columns_to_copy].copy()
    df[['label', 'score']] = df['transcriptConsumer'].apply(lambda text: do_nlp(text, model_path)).apply(pd.Series)
    df.to_excel(result_path, index=False)

def do_nlp(text, model_path):
    try:
        model = BertForSequenceClassification.from_pretrained(model_path)
        tokenizer = BertTokenizerFast.from_pretrained("bert-base-uncased", max_length=512)
        #tokenizer = BertTokenizerFast.from_pretrained(model_path)
        nlp = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
        result = nlp(text)
        print(result)
        return result[0]['label'], result[0]['score']
    except Exception as e:
        print(e)
        return None



#print(do_nlp(text))
classify_file()