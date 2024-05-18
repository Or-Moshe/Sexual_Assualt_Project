from transformers import pipeline, BertForSequenceClassification, BertTokenizerFast
import pandas as pd
from nlp.scripts.preprocessing import Preprocessing
from nlp.scripts.translate import Translate
'''
csv_path = "../data/withoutClassification.csv"
tanslated_path = "../data/withoutClassificationTranslated.csv"
model_path = "../models/torch-bert-base-uncased-model-all-data"
result_path = "../data/withoutClassificationTranslatedResults.csv"
'''
csv_path = "../data/withoutClassification.csv"
tanslated_path = "../data/withDummyTranslated_Consumer.csv"
model_path = "../models/torch-bert-base-uncased-model-all-data-consumer"
result_path = "../data/withoutClassificationTranslatedConsumerResults.csv"
def classify_file():
    '''
    df = pd.read_csv(csv_path)
    preprocessing = Preprocessing(df)
    preprocessing.process_dataframe()
    print(preprocessing.df.head())
    translate = Translate(preprocessing.df)
    df = translate.translate_dataframe(tanslated_path)
    '''
    df = pd.read_csv(tanslated_path)

    df[['label', 'score']] = df['transcriptConsumer_en'].apply(lambda text: do_nlp(text, model_path)).apply(pd.Series)
    df.to_csv(result_path, index=False)

def do_nlp(text, model_path):
    try:
        model = BertForSequenceClassification.from_pretrained(model_path)
        tokenizer = BertTokenizerFast.from_pretrained(model_path)
        nlp = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
        result = nlp(text)
        print(result)
        return result[0]['label'], result[0]['score']
    except Exception as e:
        print(e)
        return None



#print(do_nlp(text))
classify_file()