from flask import Blueprint, request, jsonify
from utils.create_chatbot import create_chatbot
from utils.updateChatbot import update_chatbot
from utils.deleteChatbot import delete_chatbot

class ChatbotRoutes:
    chatbot_bp = Blueprint('chatbot_bp', __name__)

    @chatbot_bp.route('/create-chatbot', methods=['POST'])
    def create_chatbot_route():
        data = request.json
        result = create_chatbot(data)
        return jsonify(result), result.get('status', 500)

    @chatbot_bp.route('/update-chatbot/<chatbot_id>', methods=['PUT'])
    def update_chatbot_route(chatbot_id):
        data = request.json
        result = update_chatbot(chatbot_id, data)
        return jsonify(result), result.get('status', 500)

    @chatbot_bp.route('/delete-chatbot/<chatbot_id>', methods=['DELETE'])
    def delete_chatbot_route(chatbot_id):
        result = delete_chatbot(chatbot_id)
        return jsonify(result), result.get('status', 500)
