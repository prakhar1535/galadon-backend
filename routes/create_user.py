from flask import Blueprint, request, jsonify
from utils.create_user import create_user
class createUser:
      user_bp = Blueprint('user_bp', __name__)

      @user_bp.route('/create-user', methods=['POST'])
      def create_user_route():
                  data = request.json
                  result = create_user(data)
                  return jsonify(result), result.get('status', 500)
