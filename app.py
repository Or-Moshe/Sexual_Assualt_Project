from flask import Flask, request, jsonify
import logging
from nlp.scripts.execute import do_nlp

app = Flask(__name__)

@app.route('/analyze', methods=['GET'])
def analyze_text():
    text = request.args.get('text', '')
    if text:
        result = do_nlp(text)
        return jsonify(result)
    else:
        return jsonify({"error": "no text provided"}), 400

if __name__ == "__main__":
    logging.info("Flask app started")
    app.run(host="0.0.0.0", port=8000)