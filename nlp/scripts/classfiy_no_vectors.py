
from transformers import BertForSequenceClassification, BertTokenizer
import torch

def predict_single_text_by_text(single_text, model_path):
    model = BertForSequenceClassification.from_pretrained(model_path)
    # Initialize the tokenizer
    tokenizer = BertTokenizer.from_pretrained(model_path)

    # Tokenize the text
    inputs = tokenizer(single_text, truncation=True, padding='max_length', max_length=512, return_tensors='pt')

    # Move model to device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    # Move inputs to the same device as the model
    inputs = {key: val.to(device) for key, val in inputs.items()}

    # Function to make a single prediction
    def predict_single_text(model, inputs):
        model.eval()
        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits
            predicted_class_id = torch.argmax(logits, dim=-1).item()
            return predicted_class_id

    predicted_class_id = predict_single_text(model, inputs)
    id2label = {0: 'not relevant', 1: 'emotional', 2: 'information', 3: 'high risk', 4: 'high risk', 5: 'high risk', 6: 'high risk'}

    # Get the predicted label
    predicted_label = id2label[predicted_class_id]
    return predicted_label
