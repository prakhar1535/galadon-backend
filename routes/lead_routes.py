from flask import Blueprint, request, jsonify
from utils.lead_managment import manage_lead
from utils.fetch_leads import fetch_leads
from utils.fetch_user_leads import fetch_user_leads
class LeadRoutes:
    lead_bp = Blueprint('lead_bp', __name__)

    @lead_bp.route('/manage-lead', methods=['POST'])
    def manage_lead_route():
        data = request.json
        result = manage_lead(data)
        return jsonify(result), result.get('status', 500)
    @lead_bp.route('/fetch-leads', methods=['POST'])
    def fetch_leads_route():
        data = request.json
        chatbot_id = data.get('chatbotId')

        if not chatbot_id:
            return jsonify({'message': 'Chatbot ID is required', 'status': 400}), 400

        result = fetch_leads(chatbot_id)
        return jsonify(result), result.get('status', 500)
    @lead_bp.route('/fetch-user-leads', methods=['POST'])
    def fetch_user_leads_route():
        data = request.json
        user_id = data.get('userId')

        if not user_id:
            return jsonify({'message': 'User ID is required', 'status': 400}), 400

        result = fetch_user_leads(user_id)
        return jsonify(result), result.get('status', 500)

