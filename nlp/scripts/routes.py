# routes.py
from flask import Blueprint, jsonify, request
from flask_cors import CORS
import pandas as pd
import io

from nlp.scripts.execute import (
    do_nlp, classify_file_by_vectors, classify_file_without_vectors_he,
    classify_single_text_by_vectors_en, classify_single_text_by_vectors_he
)

# Create a Blueprint
main_blueprint = Blueprint('main_blueprint', __name__)

model_path = "./nlp/models/torch-bert-base-uncased-model"

@main_blueprint.route('/analyze', methods=['GET'])
def analyze_text():
    # Retrieve text from query parameter
    text = request.args.get('text', '')  # Default to empty string if not provided
    lang = request.args.get('lang', '')
    print("text: ", text)
    if text:  # Check if text is not empty
        result = do_nlp(text, model_path)
        return jsonify(result)
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

@main_blueprint.route('/analyze_file_no_vectors', methods=['POST'])
def upload_csv():
    # Check if the post request has the file part
    print(request.files)
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    # If the user does not select a file, the browser submits an empty file without a filename
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # Read the file into a pandas DataFrame
        df = pd.read_csv(io.StringIO(file.stream.read().decode("UTF8")))
        # Process the DataFrame as needed
        # Example: print the DataFrame
        print(df)

        # You can also convert the DataFrame to JSON and return it
        data = df.to_json(orient='records')
        return jsonify(data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500