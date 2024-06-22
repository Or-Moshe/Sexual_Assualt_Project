# routes.py
import base64
import traceback

from flask import Blueprint, jsonify, request, send_file
from flask_cors import CORS
import pandas as pd
import io

from nlp.scripts.execute import (
    do_nlp, classify_file_by_vectors, classify_file_without_vectors_he,
    classify_single_text_by_vectors_en, classify_single_text_by_vectors_he, classify_single_text_en, classify_single_text_he
)
from nlp.scripts.preprocessing import Preprocessing

# Create a Blueprint
main_blueprint = Blueprint('main_blueprint', __name__)


@main_blueprint.route('/analyze', methods=['GET'])
def analyze_text():
    # Retrieve text from query parameter
    text = request.args.get('text', '')  # Default to empty string if not provided
    lang = request.args.get('lang', '')
    print("text: ", text)
    if text:  # Check if text is not empty
        res = classify_single_text_en(text) if lang == 'en' else classify_single_text_he(text)
        return jsonify(res)
    else:
        return jsonify({"error": "No text provided"}), 400

@main_blueprint.route('/analyze_by_vectors', methods=['GET'])
def analyze_by_vectors():
    # Retrieve text from query parameter
    text = request.args.get('text', '')  # Default to empty string if not provided
    lang = request.args.get('lang', '')
    print("text: ", text)
    if text:  # Check if text is not empty
        res = classify_single_text_by_vectors_en(text) if lang == 'en' else classify_single_text_by_vectors_he(text)
        print("res: ", res)
        return jsonify(res)
    else:
        return jsonify({"error": "No text provided"}), 400

@main_blueprint.route('/analyze_file_by_vectors', methods=['POST'])
def analyze_file_by_vectors():
    # Retrieve text from query parameter
    text = request.args.get('text', '')  # Default to empty string if not provided
    print("text: ", text)
    if text:  # Check if text is not empty
        result = classify_single_text_by_vectors_en(text)
        print("result: ", result)
        return jsonify(result)
    else:
        return jsonify({"error": "No text provided"}), 400

"""
@main_blueprint.route('/analyze_file_no_vectors', methods=['POST'])
def analyze_file_no_vectors():
    # Retrieve text from query parameter
    text = request.args.get('text', '')  # Default to empty string if not provided
    print("text: ", text)
    if text:  # Check if text is not empty
        result = classify_file_without_vectors_he(text, model_path)
        res = {"classification": result}
        print("res: ", res)
        return jsonify(res)
    else:
        return jsonify({"error": "No text provided"}), 400
"""

def classify_file_without_vectors_he(df):
    column_to_predict = 'transcriptConsumer'  # Use the correct column name

    preprocessing = Preprocessing(df)
    df = preprocessing.process_dataframe(column_to_predict)

    # Apply the function and expand the results into separate columns
    predictions = df[column_to_predict].apply(classify_single_text_en).apply(pd.Series)

    # Join the predictions with the original DataFrame
    df = df.join(predictions)
    return df


class Preprocessing:
    def __init__(self, df):
        self.df = df

    def process_dataframe(self, column_to_predict):
        print("Preprocessing - Initial DataFrame shape:", self.df.shape)

        # Check for missing values
        print("Missing values before drop:", self.df.isnull().sum())

        # Drop rows with missing values in the column_to_predict
        self.df = self.df.dropna(subset=[column_to_predict])
        print("DataFrame shape after dropping missing values:", self.df.shape)

        # Check for duplicates
        print("Duplicates before drop:", self.df.duplicated().sum())

        # Drop duplicate rows
        self.df = self.df.drop_duplicates()
        print("DataFrame shape after dropping duplicates:", self.df.shape)

        print("Preprocessing - Final DataFrame shape:", self.df.shape)
        return self.df


@main_blueprint.route('/analyze_file_no_vectors', methods=['POST'])
def upload_csv():
    try:
        # Get the JSON data from the request
        data = request.get_json()

        # Check if 'file' and 'filename' keys are in the JSON data
        if 'file' not in data or 'filename' not in data:
            return jsonify({"error": "No file or filename part"}), 400

        # Decode the base64 string to bytes
        file_data = base64.b64decode(data['file'])
        filename = data['filename']
        print(file_data)
        print(filename)

        # If the user does not select a file, the browser submits an empty file without a filename
        if filename == '':
            return jsonify({"error": "No selected file"}), 400

        df = pd.read_excel(io.BytesIO(file_data))
        classify_file_without_vectors_he(df)
        return jsonify({"success": "success"}), 200

    except Exception as e:
        print("Unexpected error:", str(e))
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
