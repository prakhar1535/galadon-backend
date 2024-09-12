from flask import Blueprint, request, jsonify
from utils.add_credits import add_credits

class CreditsRoutes:
    credits_bp = Blueprint('credits_bp', __name__)

    @credits_bp.route('/add-credits', methods=['POST'])
    def add_credits_route():
        data = request.json
        chatbot_id = data.get('chatbot_id')
        credits = data.get('credits')

        if not chatbot_id or not isinstance(credits, int):
            return jsonify({'message': 'Invalid input. Please provide chatbot_id and credits (integer).'}), 400

        result = add_credits(chatbot_id, credits)
        return jsonify(result), result['status']