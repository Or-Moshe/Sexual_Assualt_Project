from transformers import pipeline, BertForSequenceClassification, BertTokenizerFast, BertTokenizer
import torch
import numpy as np
import pandas as pd


def text_to_vector(text):
    # Ensure the input is a string
    if not isinstance(text, str):
        text = str(text)

    model_to_vector_path = "../models/text-to-vector/customer-en-encoded"
    model_to_vector = BertForSequenceClassification.from_pretrained(model_to_vector_path)
    tokenizer = BertTokenizerFast.from_pretrained(model_to_vector_path)

    # Tokenize the input text
    inputs = tokenizer(text, return_tensors='pt', max_length=512, truncation=True, padding='max_length')

    # Predict the vector from the model
    with torch.no_grad():
        outputs = model_to_vector(**inputs)

    # Extract the logits from the model output
    single_example_vector = outputs.logits.numpy().flatten().tolist()  # Convert numpy array to list

    return single_example_vector


def file_to_vector(df):
    # Ensure all entries in the 'transcriptConsumer_en' column are strings
    df['transcriptConsumer_en'] = df['transcriptConsumer_en'].astype(str)

    # Apply the text_to_vector function and handle any errors gracefully
    df['vector'] = df['transcriptConsumer_en'].apply(lambda text: text_to_vector(text))

    # Check the first few entries to ensure vectors are correct
    print(df['vector'].head())

    # Expand the vector column into multiple columns
    vectors = pd.DataFrame(df['vector'].tolist(), index=df.index)
    vectors.columns = [f'vector_{i}' for i in vectors.columns]

    # Drop the original vector column and concatenate the expanded vectors
    df = df.drop(['vector'], axis=1)
    df = pd.concat([df, vectors], axis=1)

    df.to_csv("../data/inputs/withoutClassificationVectorized.csv", index=False)

    return df

text = """
Hi, I fell into a twin that I can't get out of. I don't think it's possible. I don't think it's possible. I'm lost. I don't know what happened to me, what's happening to me. I don't remember and I don't want to remember anything. I don't know what's happening to me, I don't know what I'm doing, what I want, what I'm interested in is just drinking some kind of lol, this is the best and most reliable friend, isn't it good? There are no friends, only one and only friend, this is drinking, I don't want to hear that word, friendship with friendship, what? I don't know why I'm still in this life anyway I feel like wind and air so why?? It's just a waste, I don't know, I don't know, I'm not interested either, really, I'm in a kind of bubble of my own, yes, I called, I was in a meeting, I don't remember what they said, and they didn't get back to me, so I'm probably not interested, I don't know, I'm broken by everything, I don't care about anything anymore, sorry for the sentence about my dick I can't take this whole life anymore. I'm already 35. What can I tell you, how beautiful my moments are, how happy I am, how happy I am that I came into this world, how life just smiles at me, how good I am and how happy I am. Unfortunately, I have a family, but I'm not in contact with them. I don't have Hobbies and I don't like to do anything. I listen to everything from everything. Even if I drink and don't have it. I probably won't like it. The song is not for nothing. Now I received very good and happy news that they closed my 2 cases, do you understand how black I am? What I didn't understand was exactly what kind of light they closed my complaints, they don't treat me there either, it doesn't interest me today, it's just a celebration, drink more for closing the cases, everything is fine, I'm not I'm angry or hurt don't feel uncomfortable I'm already immune I can't be hurt by anything and nothing after this year with already I'm sorry yes I'm not explaining myself correctly and I'm sorry for that understand it's from the drinking I'm really not I'm not out of it I want me to tell you Something that I saw myself a little bit more, really a little bit, that I also get worse from drinking, why alone I can't do it anyway, I don't have a family to support me, no, there is no one to help me, they haven't helped me until now, why will they help me now, the difficulty in general is my whole life And they didn't help me and this year what I went through in my whole life is nothing
"""
text_to_vector(text)
