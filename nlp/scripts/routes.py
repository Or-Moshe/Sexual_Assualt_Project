# routes.py
from flask import Blueprint, jsonify, request
from nlp.scripts.execute import do_nlp

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