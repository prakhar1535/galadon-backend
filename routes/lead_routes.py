from flask import Blueprint, request, jsonify
from utils.lead_managment import manage_lead

class LeadRoutes:
    lead_bp = Blueprint('lead_bp', __name__)

    @lead_bp.route('/manage-lead', methods=['POST'])
    def manage_lead_route():
        data = request.json
        result = manage_lead(data)
        return jsonify(result), result.get('status', 500)