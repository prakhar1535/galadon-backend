from flask import Blueprint, request, jsonify
from utils.create_chatbot import create_chatbot
from utils.updateChatbot import update_chatbot
from utils.deleteChatbot import delete_chatbot
from db.db import supabase

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
    @chatbot_bp.route('/get-chat-history', methods=['POST'])
    def get_chat_history():
        data = request.json
        user_id = data.get('userId')

        if not user_id:
            return jsonify({'message': 'User ID is required', 'status': 400}), 400

        try:
           
            response = supabase.table('users').select('messages').eq('userId', user_id).execute()

            if not response.data:
                return jsonify({'message': 'No chat history found for the given user ID', 'status': 404}), 404

            chat_history = response.data[0].get('messages', [])

            return jsonify({
                'message': 'Chat history retrieved successfully',
                'status': 200,
                'data': chat_history
            }), 200

        except Exception as e:
            return jsonify({'message': f'Error retrieving chat history: {str(e)}', 'status': 500}), 500
