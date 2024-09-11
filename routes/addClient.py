from flask import Blueprint, request, jsonify
from utils.addClient import create_client


class ClientRoutes:
    client_bp = Blueprint('client_bp', __name__)

    @client_bp.route('/add-client', methods=['POST'])
    def create_client_route():
        data = request.json
        result = create_client(data)
        return jsonify(result), result.get('status', 500)