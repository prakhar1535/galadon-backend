from flask import Blueprint, request, jsonify
from utils.create_chatbot import create_chatbot
class generateChatbot:
    chatbot = Blueprint('generateChatbot', __name__)

    @chatbot.route('/generate-chatbot', methods=['POST'])
    def generate_chatbot():
        try:
            data = request.json
            result = create_chatbot(data)
            return jsonify(result), result.get('status')
        except Exception as e:
            return jsonify({'message': 'Internal server error', 'status': 500, 'error': str(e)}), 500
