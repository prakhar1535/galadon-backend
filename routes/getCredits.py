from flask import Blueprint, request, jsonify
from utils.get_credits import calculate_total_credits

class GetCreditsRoutes:
    get_credits_bp = Blueprint('get_credits_bp', __name__)

    @get_credits_bp.route('/get-credits', methods=['POST'])
    def calculate_total_credits_route():
        data = request.json
        chatbot_id = data.get('chatbot_id')
        start_timestamp = data.get('start_date')
        end_timestamp = data.get('end_date')

        if not all([chatbot_id, start_timestamp, end_timestamp]):
            return jsonify({'message': 'Missing required parameters. Please provide chatbot_id, start_date, and end_date in the request body.'}), 400

        try:
            start_timestamp = int(start_timestamp)
            end_timestamp = int(end_timestamp)
        except ValueError:
            return jsonify({'message': 'Invalid date format. Please provide Unix timestamps for start_date and end_date.'}), 400

        result = calculate_total_credits(chatbot_id, start_timestamp, end_timestamp)
        return jsonify(result), result['status']