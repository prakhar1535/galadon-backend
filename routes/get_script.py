from flask import Blueprint, request, jsonify, Response
from utils.getScript import get_script

class GetChatbotScript:
    getChatbotScript = Blueprint('getChatbotScript', __name__)

    @getChatbotScript.route('/get-chatbot-script/<chatbot_id>', methods=['GET'])
    def generate_chatbot(chatbot_id):
        try:
            script_data, status_code = get_script(chatbot_id)
            if status_code != 200:
                return jsonify(script_data), status_code
            
            return Response(
                script_data['content'],
                mimetype=script_data['media_type'],
                headers=script_data['headers']
            )
        except Exception as e:
            return jsonify({'message': 'Internal server error', 'error': str(e)}), 500