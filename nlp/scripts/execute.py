import joblib
from transformers import pipeline, BertForSequenceClassification, BertTokenizerFast, BertTokenizer
import pandas as pd
import numpy as np
import pickle
import sklearn
import openpyxl
from nlp.scripts.preprocessing import Preprocessing
import torch
from nlp.scripts.translate import Translate
from nlp.scripts.text_to_vector import vectorized_single_text, vectorized_df, decode_one_hot
from nlp.scripts.vector_to_classification_v2 import predict_single_text
from nlp.scripts.classfiy_no_vectors import predict_single_text_by_text

'''
tanslated_path = "../data/withoutClassificationTranslated.csv"
model_path = "../models/torch-bert-base-uncased-model-all-data"
result_path = "../data/withoutClassificationTranslatedResults.csv"
'''
'''
tanslated_path = "../data/withDummyTranslated_Consumer.csv"
model_path = "../models/torch-bert-base-uncased-model-all-data-consumer"
result_path = "../data/withoutClassificationTranslatedConsumerResults.csv"
'''

'''
model_path = "../models/torch-bert-base-uncased-model-all-data-consumer-he"
result_path = "../data/withoutClassificationConsumerResults-he.xlsx"
'''

csv_path = "../data/inputs/withoutClassificationTranslated.csv"
tanslated_path = "../data/inputs/withoutClassificationTranslated.csv"

result_path = "../data/results/hebrew/predictionsConsumerResults-en.csv"
column_to_predict = 'transcriptConsumer_en'

def classify_file_by_vectors():
    '''
    csv_path = "../data/inputs/withoutClassification.csv"
    df = pd.read_csv(csv_path, usecols=['firstConversation', 'transcriptAll', 'transcriptConsumer'])
    preprocessing = Preprocessing(df)
    df = preprocessing.process_dataframe(column_to_predict)
    print(df.columns)

    translate = Translate(preprocessing.df)
    df = translate.translate_dataframe(tanslated_path)
    df = pd.read_csv(tanslated_path)
'''
    '''
    df = pd.read_csv(tanslated_path)
    file_to_vector(df)
'''

    '''
    df = pd.read_csv("../data/inputs/withoutClassificationTranslated.csv")
    # Vectorize the text and update the DataFrame
    sentiment_results_df = vectorized_df(df)
    result_path = "../data/results/english/text-to-vector-results.csv"
    sentiment_results_df.to_csv(result_path, index=False)
    '''
    # Check the DataFrame structure
    df = pd.read_csv("../data/results/english/text-to-vector-results.csv")
    final_df = classify_file(df)

def classify_single_text_by_vectors_en(text):
    res = {}
    result = vectorized_single_text(text, 'en')
    res['prediction'] = predict_single_text(result['vector'])
    res['sentiments'] = decode_one_hot(result)
    print('res',res)
    return res

def classify_single_text_by_vectors_he(text):
    res = {}
    result = vectorized_single_text(text, 'he')
    res['prediction'] = predict_single_text(result['vector'])
    res['sentiments'] = decode_one_hot(result)
    print('res',res)
    return res

def classify_single_text_en(text):
    res = {}
    # from app:
    #model_path = "./nlp/models/classify-without-vector/en/classify-no-vectors-en"
    model_path = "./nlp/models/classify-without-vector/en/bert-base-multilingual-cased-0-77"
    res['prediction'] = predict_single_text_by_text(text, model_path)
    return res
"""
    tokenizer = BertTokenizer.from_pretrained(model_path, max_length=512)
    nlp = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
    result = nlp(text)
    print(result)
    return result[0]['label'], result[0]['score']
"""
def classify_single_text_he(text):
    res = {}
    # from app:
    # model_path = "./nlp/models/classify-without-vector/en/classify-no-vectors-en"
    model_path = "./nlp/models/classify-without-vector/he/bert-base-multilingual-cased-0-74"
    vector = vectorized_single_text(text, 'he')
    res['prediction'] = predict_single_text_by_text(text, model_path)
    res['sentiments'] = decode_one_hot(vector)
    return res


"""
    tokenizer = BertTokenizer.from_pretrained(model_path, max_length=512)
    nlp = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
    result = nlp(text)
    print(result)
    return result[0]['label'], result[0]['score']
"""
"""
def classify_single_text_by_vectors2(text):
    model_to_vector_path = "../models/text-to-vector/predict_flags-model-all-data-consumer-en"
    vector = text_to_vector(text, model_to_vector_path)
    print(f'Vector: {vector}')
    classifier_model_path = '../models/vector-to-classification/random_forest_model.pkl'
    # Load your classifier model
    with open(classifier_model_path, 'rb') as file:
        classifier_model = pickle.load(file)

    # Make a prediction
    predicted_classification = classifier_model.predict(vector)
    print(f'Predicted Classification: {predicted_classification}')

"""
def translate_file():
    df = pd.read_csv(csv_path, usecols=['transcriptAll', 'transcriptConsumer'])
    preprocessing = Preprocessing(df)
    df = preprocessing.process_dataframe(column_to_predict)
    translate = Translate(preprocessing.df)
    df = translate.translate_dataframe(tanslated_path)
    return df
def classify_file_without_vectors_he():

    df = pd.read_excel(csv_path, usecols=['transcriptAll', 'transcriptConsumer_en'])
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
        tokenizer = BertTokenizer.from_pretrained("bert-base-uncased", max_length=512)
        #tokenizer = BertTokenizerFast.from_pretrained(model_path)
        nlp = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
        result = nlp(text)
        print(result)
        return result[0]['label'], result[0]['score']
    except Exception as e:
        print(e)
        return None


# Convert numpy.int32 to Python int
def convert_numpyInt_to_int(result):
    for key, value in result.items():
        if isinstance(value, (np.int32, np.int64)):
            result[key] = int(value)

    return result

#print(do_nlp(text))
#classify_file()
#translate_file()
#single_example_reshaped = text_to_vector()
#text_to_vector()
text = """
Hey ?? please help me I fell for a twin and I'm screaming out loud Do not know No mistake But God is not with me All is well I'm lonely, I'll be lonely I was a bitch, I'll stay a bitch of what exactly what I'm a piece of shit Because from the day I know myself I am guilty Your testimony that you don't know me is the best Because if you knew me, you would regret it like everyone else what a mother you have an angel I'm on fire for her What would I do without her? A bitch can't stand her A mistake she brought me into this world Ruined my life Every day and every day I drink and lose myself I don't care about my dick
"""
#classify_single_text_by_vectors(text)
#print(f'classify_text_by_vectors results: {classify_text_by_vectors(text)}')
#print(f'do_nlp results: {do_nlp(text, model_path)}')
#classify_single_text_by_vectors_en(text)
#classify_single_text_en(text)