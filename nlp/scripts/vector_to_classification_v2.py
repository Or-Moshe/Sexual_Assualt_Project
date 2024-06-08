import torch
import torch.nn as nn
import numpy as np
import pandas as pd

model_path = "../models/vector-to-classification/SimpleNNClassifier-model-customer-en.pth"

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

class SimpleNNClassifier(nn.Module):
    def __init__(self, input_size, num_classes):
        super(SimpleNNClassifier, self).__init__()
        self.fc1 = nn.Linear(input_size, 128)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(128, num_classes)

    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        return out


# Example parameters (these should match your model)
input_size = len(cols)  # Number of input features (length of the vector)
num_classes = 7  # Number of classes

# Initialize the model
model = SimpleNNClassifier(input_size, num_classes)

# Load the model weights
model.load_state_dict(torch.load(model_path))
model.eval()


def predict_single_text(input_vector):
    # Example input vector (replace this with actual input vector)
    #input_vector = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0])
    print(input_vector)
    # Convert the input vector to tensor
    input_tensor = torch.tensor(input_vector, dtype=torch.float32).unsqueeze(0)  # Add batch dimension

    # Predict classification
    with torch.no_grad():
        output = model(input_tensor)
        prediction = torch.argmax(output, dim=1).item()

    print(f'Predicted class: {prediction}')
    return prediction


def predict_texts():
    # Make predictions for each vector
    list_of_vectors = [
        [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
        [0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0]
    ]
    predictions = []
    for vector in list_of_vectors:
        # Convert the vector to tensor
        input_tensor = torch.tensor(vector, dtype=torch.float32).unsqueeze(0)  # Add batch dimension

        # Predict classification
        with torch.no_grad():
            output = model(input_tensor)
            prediction = torch.argmax(output, dim=1).item()
            predictions.append(prediction)

    # Print the predictions
    for i, prediction in enumerate(predictions):
        print(f'Prediction for vector {i + 1}: {prediction}')

def predict_file():
    df = pd.read_csv("../data/results/english/text-to-vector-results.csv")
    list_of_vectors = df[cols].values
    predictions = []
    for vector in list_of_vectors:
        # Convert the vector to tensor
        input_tensor = torch.tensor(vector, dtype=torch.float32).unsqueeze(0)  # Add batch dimension

        # Predict classification
        with torch.no_grad():
            output = model(input_tensor)
            prediction = torch.argmax(output, dim=1).item()
            predictions.append(prediction)

    df['predictions'] = predictions
    df.to_csv("../data/results/vectorized-one-encoded-SimpleNNClassifier.csv", index=False)
    return df


def classify_file2(df):
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
    df.to_csv("../data/results/vectorized-one-encoded.csv", index=False)
#predict_file()