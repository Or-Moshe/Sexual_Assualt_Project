# routes.py
import base64

from flask import Blueprint, jsonify, request
from flask_cors import CORS
import pandas as pd
import io

from nlp.scripts.execute import (
    do_nlp, classify_file_by_vectors, classify_file_without_vectors_he,
    classify_single_text_by_vectors_en, classify_single_text_by_vectors_he, classify_single_text_en, classify_single_text_he
)

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
        return jsonify({"error": str(e)}), 500