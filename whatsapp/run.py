import logging

from app import create_app

#run ngrok: ngrok http 8000 --domain on-toad-tidy.ngrok-free.app
app = create_app()

if __name__ == "__main__":
    logging.info("Flask app started")
    app.run(host="0.0.0.0", port=8000)
