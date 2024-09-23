from flask import Blueprint, request, jsonify
from utils.get_credits import calculate_total_credits
from datetime import datetime, timezone
import traceback

class GetCreditsRoutes:
    get_credits_bp = Blueprint('get_credits_bp', __name__)

    @get_credits_bp.route('/get-credits', methods=['POST'])
    def calculate_total_credits_route():
        try:
            data = request.json
            client_id = data.get('clientId')
            start_date = data.get('start_date')
            end_date = data.get('end_date')

            if not all([client_id, start_date, end_date]):
                return jsonify({'message': 'Missing required parameters. Please provide clientId, start_date, and end_date.'}), 400

            # Convert input strings to datetime objects
            start_datetime = datetime.strptime(start_date, '%Y-%m-%d').replace(tzinfo=timezone.utc)
            end_datetime = datetime.strptime(end_date, '%Y-%m-%d').replace(tzinfo=timezone.utc)
            
            # Convert datetime objects to Unix timestamps (in seconds)
            start_timestamp = int(start_datetime.timestamp())
            end_timestamp = int(end_datetime.timestamp())

            result = calculate_total_credits(client_id, start_date, end_date, start_timestamp, end_timestamp)
            return jsonify(result), result['status']
        except Exception as e:
            error_message = f"An error occurred: {str(e)}\n\nTraceback:\n{traceback.format_exc()}"
            return jsonify({'message': error_message, 'status': 500}), 500