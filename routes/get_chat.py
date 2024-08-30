from flask import Blueprint, request, jsonify
from utils.getChat import get_chat

class GetChat:
    get_chat_bp = Blueprint('get_chat_bp', __name__)

    @get_chat_bp.route('/get-chat/<user_id>', methods=['GET'])
    def get_chat_route(user_id):
        result = get_chat(user_id)
        return jsonify(result), result.get('status', 500)
