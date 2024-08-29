from flask import Blueprint, request, jsonify
from utils.getSession import get_session

class getSessions:
    getSessions = Blueprint('getSessions', __name__)

    @getSessions.route('/get-sessions', methods=['POST'])
    def generate_chatbot():
        try:
            result, status_code = get_session()
            return jsonify(result), status_code
        except Exception as e:
            return jsonify({'message': 'Internal server error', 'error': str(e)}), 500