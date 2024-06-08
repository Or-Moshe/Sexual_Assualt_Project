import torch
import numpy as np
import pandas as pd
from transformers import BertTokenizerFast, BertForSequenceClassification
from sklearn.ensemble import RandomForestClassifier
import pickle


def text_to_vector(text):
    # Ensure the input is a string
    if not isinstance(text, str):
        text = str(text)

    model_to_vector_path = "../models/text-to-vector/en/customer-en-encoded"
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


# Example usage:
# Assuming df is your DataFrame and it has a column 'transcriptConsumer_en' containing text data.
df = pd.DataFrame({
    'transcriptConsumer_en': [
        "Hi, I fell into a twin that I can't get out of.",
        "I don't know what happened to me, what's happening to me.",
        "I'm lost. I don't know what happened to me.",
        "I feel like I'm in a bubble, everything is fine.",
        "I'm really happy today, everything is going great."
    ]
})

# Vectorize the text and update the DataFrame
df = file_to_vector(df)

# Check the DataFrame structure
print(df.head())

# Load the Random Forest model
classifier_model_path = '../models/vector-to-classification/random_forest_model.pkl'
with open(classifier_model_path, 'rb') as file:
    classifier_model = pickle.load(file)

# Prepare the feature matrix X for prediction (all vector columns)
vector_columns = [col for col in df.columns if col.startswith('vector_')]
X = df[vector_columns].values

# Make predictions
predictions = classifier_model.predict(X)
df['predictions'] = predictions

print(df[['transcriptConsumer_en', 'predictions']])
