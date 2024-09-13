from flask import Blueprint, request, jsonify
from utils.get_credits import calculate_total_credits

class GetCreditsRoutes:
    get_credits_bp = Blueprint('get_credits_bp', __name__)

    @get_credits_bp.route('/calculate-total-credits', methods=['GET'])
    def calculate_total_credits_route():
        chatbot_id = request.args.get('chatbot_id')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        if not all([chatbot_id, start_date, end_date]):
            return jsonify({'message': 'Missing required parameters. Please provide chatbot_id, start_date, and end_date.'}), 400

        result = calculate_total_credits(chatbot_id, start_date, end_date)
        return jsonify(result), result['status']