from flask import Blueprint, request, jsonify
from utils.addChat import add_chat

class AddChat:
    chat_bp = Blueprint('chat_bp', __name__)

    @chat_bp.route('/add-chat', methods=['POST'])
    def add_chat_route():
        data = request.json
        result = add_chat(data)
        return jsonify(result), result.get('status', 500)
