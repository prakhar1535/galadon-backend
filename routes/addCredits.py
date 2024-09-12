from flask import Blueprint, request, jsonify
from utils.add_credits import add_credits
from utils.getCredits import get_credits

class CreditsRoutes:
    credits_bp = Blueprint('credits_bp', __name__)

    
    @credits_bp.route('/add-credits', methods=['POST'])
    def add_credits_route():
        data = request.json
        if not data:
            return jsonify({'message': 'No input data provided', 'status': 400}), 400

        result = add_credits(data)
        return jsonify(result), result['status']

    
    @credits_bp.route('/get-credits', methods=['GET'])
    def get_credits_route():
        chatbot_id = request.args.get('chatbotId')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if not all([chatbot_id, start_date, end_date]):
            return jsonify({'message': 'Missing required parameters', 'status': 400}), 400

        result = get_credits(chatbot_id, start_date, end_date)
        return jsonify(result), result['status']