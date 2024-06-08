from transformers import pipeline, BertForSequenceClassification, BertTokenizerFast, BertTokenizer
import torch
import numpy as np
import pandas as pd

#from app:
#model_to_vector_path = "./nlp/models/text-to-vector/customer-en-encoded"
#model_to_vector_path = "../models/text-to-vector/customer-en-encoded"

cols = ['despair_0', 'despair_1', 'loneliness_0',
        'loneliness_1', 'emotional overflow_0', 'emotional overflow_1',
        'self blame_0', 'self blame_1', 'anxiety_0', 'anxiety_1',
        'distrust / confusion_0', 'distrust / confusion_1',
        'new assault / new exposure_0', 'new assault / new exposure_1',
        'level of suicide/ level of risk_0',
        'level of suicide/ level of risk_1',
        'level of suicide/ level of risk_2',
        'level of suicide/ level of risk_3',
        'obligation to report occording law_0',
        'obligation to report occording law_1', 'support for support circuls_0',
        'support for support circuls_1']

def prepare_input(text, tokenizer):
    encoding = tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=512)
    return encoding

def predict_sentiments(text, model_path):
    model = BertForSequenceClassification.from_pretrained(model_path)
    tokenizer = BertTokenizerFast.from_pretrained(model_path)
    model.eval()
    inputs = prepare_input(text, tokenizer)
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
    return logits

def get_binary_vector(logits, threshold=0.5):
    probs = torch.sigmoid(logits)
    binary_vector = (probs > threshold).int()
    return binary_vector

def get_sentiment_vector(text, model_path, threshold=0.5):
    logits = predict_sentiments(text, model_path)
    binary_vector = get_binary_vector(logits, threshold)
    return binary_vector.numpy().flatten()

def store_sentiment_vector(text, vector):
    #data = {'transcriptConsumer_en': text}
    data = {}
    print(vector)
    for i, col in enumerate(cols):
        data[col] = vector[i]
    data['vector'] = np.array(vector)
    return data

def vectorized_df(df):
    results = []
    df['transcriptConsumer_en'] = df['transcriptConsumer_en'].astype(str)
    for text in df['transcriptConsumer_en']:
        binary_vector = get_sentiment_vector(text)
        print(binary_vector)
        result = store_sentiment_vector(text, binary_vector)
        results.append(result)

    # Convert results to a DataFrame
    sentiment_results_df = pd.DataFrame(results, columns=['transcriptConsumer_en'] + cols)

    # Concatenate the original DataFrame with the sentiment results
    final_df = pd.concat([df, sentiment_results_df.drop(columns=['transcriptConsumer_en'])], axis=1)
    print(final_df.head())
    return final_df


def vectorized_single_text(text, lang):
    #from app:
    model_path = "./nlp/models/text-to-vector/en/customer-en-encoded" if lang == 'en' else "./nlp/models/text-to-vector/en/customer-en-encoded"
    #model_path = "../models/text-to-vector/en/customer-en-encoded" if lang == 'en' else "../models/text-to-vector/en/customer-en-encoded"
    binary_vector = get_sentiment_vector(text, model_path)
    print('binary_vector', binary_vector)
    result = store_sentiment_vector(text, binary_vector)
    print('result',result)
    return result

text = """
Hey I don't know what's happening to me what is happening to my body I always make mistakes and don't learn Me and my big mouth my mother's cup My biggest mistake in this life that I exist I have to keep my mouth shut and do and deal with things without telling True, but now I do it like a grown-up Aaaaaaaaa There is no one I don't want anyone either, I don't have faith in anyone It's best to be alone, lonely like a bitch, the best and the truest I'm sorry I'm taking it all out on you It's best to keep the right to remain silent and that's it Obviously Do not want you are right no matter everything is fine All is well
"""
#print(vectorized_single_text(text))
#binary_vector = get_sentiment_vector(text)
#print(binary_vector)
