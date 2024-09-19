from flask import Blueprint, request, jsonify
from utils.get_credits import calculate_total_credits
from datetime import datetime

class GetCreditsRoutes:
    get_credits_bp = Blueprint('get_credits_bp', __name__)

    @get_credits_bp.route('/get-credits', methods=['POST'])
    def calculate_total_credits_route():
        data = request.json
        client_id = data.get('clientId')
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if not all([client_id, start_date, end_date]):
            return jsonify({'message': 'Missing required parameters. Please provide clientId, start_date, and end_date.'}), 400

        try:
            # Validate date format
            datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S+00')
            datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S+00')
        except ValueError:
            return jsonify({'message': 'Invalid date format. Please provide dates in the format YYYY-MM-DD HH:MM:SS+00.'}), 400

        result = calculate_total_credits(client_id, start_date, end_date)
        return jsonify(result), result['status']