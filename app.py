from flask import Flask, request, jsonify
import logging
from nlp.scripts.routes import main_blueprint

app = Flask(__name__)
app.register_blueprint(main_blueprint)

if __name__ == "__main__":
    logging.info("Flask app started")
    app.run(host="0.0.0.0", port=8000)