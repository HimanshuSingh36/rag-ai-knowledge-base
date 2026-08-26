from flask import Flask, jsonify
from flask_cors import CORS
import os

port = int(os.environ.get("PORT", 5002))

from routes.chat import chat_bp


app = Flask(__name__)

CORS(app)


app.register_blueprint(chat_bp)


@app.get("/api/health")
def health_check():

    return jsonify({
        "status": "ok",
        "message": "AI Knowledge Base backend is running"
    })


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )