from flask import Blueprint, request, jsonify
from utils.addLinkScrape import scrape_and_add_link
class Scrap:
      scrape_bp = Blueprint('scrape_bp', __name__)

      @scrape_bp.route('/add-link-scrape', methods=['POST'])
      def add_link_scrape_route():
            data = request.json
            result = scrape_and_add_link(data)
            return jsonify(result), result.get('status', 500)