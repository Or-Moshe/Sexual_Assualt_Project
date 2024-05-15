# routes.py
from flask import Blueprint, jsonify, request
from nlp.scripts.execute import do_nlp

# Create a Blueprint
main_routes = Blueprint('main', __name__)

@main_routes.route('/')
def home():
    return "Welcome to the Home Page!"

@main_routes.route('/analyze', methods=['GET'])
def analyze_text():
    # Retrieve text from query parameter
    text = request.args.get('text', '')  # Default to empty string if not provided
    print("text: ", text)
    if text:  # Check if text is not empty
        result = do_nlp(text)
        return jsonify(result)
    else:
        return jsonify({"error": "No text provided"}), 400