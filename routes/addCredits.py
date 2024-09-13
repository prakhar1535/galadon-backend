from flask import Blueprint, request, jsonify
from utils.add_credits import add_credits

class CreditsRoutes:
    credits_bp = Blueprint('credits_bp', __name__)

    
    @credits_bp.route('/add-credits', methods=['POST'])
    def add_credits_route():
        data = request.json
        if not data:
            return jsonify({'message': 'No input data provided', 'status': 400}), 400

        result = add_credits(data)
        return jsonify(result), result['status']
