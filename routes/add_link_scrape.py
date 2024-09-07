from flask import Blueprint, request, jsonify
from utils.addLinkScrape import scrape_and_add_link, get_chatbot_links
class Scrap:
      scrape_bp = Blueprint('scrape_bp', __name__)

      @scrape_bp.route('/add-link-scrape', methods=['POST'])
      def add_link_scrape_route():
            data = request.json
            result = scrape_and_add_link(data)
            return jsonify(result), result.get('status', 500)
      @scrape_bp.route('/get-link', methods=['GET'])
      def get_link_route():
            chatbot_id = request.args.get('chatbotId')
            if not chatbot_id:
                  return jsonify({'message': 'Chatbot ID is required', 'status': 400}), 400
            
            result = get_chatbot_links(chatbot_id)
            return jsonify(result), result.get('status', 500)
      