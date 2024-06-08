# routes.py
from flask import Blueprint, jsonify, request
from nlp.scripts.execute import do_nlp, classify_file_by_vectors, classify_file_without_vectors_he, classify_single_text_by_vectors_en, classify_single_text_by_vectors_he

# Create a Blueprint
main_blueprint = Blueprint('main_blueprint', __name__)

model_path = "./nlp/models/torch-bert-base-uncased-model"

@main_blueprint.route('/analyze', methods=['GET'])
def analyze_text():
    # Retrieve text from query parameter
    text = request.args.get('text', '')  # Default to empty string if not provided
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
        result = classify_single_text_by_vectors_en(text) if lang == 'en' else classify_single_text_by_vectors_he(text)
        #result = classify_single_text_by_vectors_en(text)

        res = {"classification": result}
        print("res: ", res)
        print("lang: ", lang)
        return res
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

@main_blueprint.route('/analyze_file_no_vectors', methods=['POST'])
def analyze_file_no_vectors():
    # Retrieve text from query parameter
    text = request.args.get('text', '')  # Default to empty string if not provided
    print("text: ", text)
    if text:  # Check if text is not empty
        result = classify_file_without_vectors_he(text, model_path)
        res = {"classification": result}
        print("res: ", res)
        return res
    else:
        return jsonify({"error": "No text provided"}), 400

