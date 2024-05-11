from flask import Flask, request, jsonify
import logging
from nlp.scripts.execute import do_nlp

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze_text():
    data = request.json
    #text = data['text']
    text = "Recently, I've been feeling very anxious and overwhelmed at work. It's started to affect my sleep and my relationships. I don't feel like it's an emergency, but I could really use some advice on how to manage this stress."
    result = do_nlp(text)
    #result2 = predict(text)
    print('result', result)
    #print('result2', result2)
    return jsonify(result)

if __name__ == "__main__":
    logging.info("Flask app started")
    app.run(host="0.0.0.0", port=8000)