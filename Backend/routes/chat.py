from flask import Blueprint, request, jsonify

from main import run_query


chat_bp = Blueprint("chat", __name__)


@chat_bp.post("/api/chat")
def chat():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    message = data.get("message", "").strip()

    if not message:
        return jsonify({
            "error": "Message is required"
        }), 400

    try:

        response = run_query(message)

        return jsonify({
            "response": response
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500