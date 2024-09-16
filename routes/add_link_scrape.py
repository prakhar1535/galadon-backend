from flask import Blueprint, request, jsonify
from utils.addLinkScrape import scrape_and_add_link, get_chatbot_links
from db.db import supabase
import json
class Scrap:
    scrape_bp = Blueprint('scrape_bp', __name__)

    @scrape_bp.route('/add-link-scrape', methods=['POST'])
    def add_link_scrape_route():
        data = request.json
        result = scrape_and_add_link(data)
        return jsonify(result), result.get('status', 500)

    @scrape_bp.route('/get-link', methods=['POST'])
    def get_link_route():
        data = request.json
        print(f"Received request data: {data}")
        
        chatbot_id = data.get('chatbotId')
        if not chatbot_id:
            print("No chatbot ID provided in request")
            return jsonify({'message': 'Chatbot ID is required', 'status': 400}), 400
        
        print(f"Calling get_chatbot_links with chatbot ID: {chatbot_id}")
        result = get_chatbot_links(chatbot_id)
        print(f"Result from get_chatbot_links: {result}")
        
        return jsonify(result), result.get('status', 500)
    
    @scrape_bp.route('/get-all-links', methods=['POST'])
    def get_all_links():
        data = request.json
        chatbot_id = data.get('chatbotId')

        if not chatbot_id:
            return jsonify({'message': 'Chatbot ID is required', 'status': 400}), 400

        try:
            response = supabase.table('chatbot_scraped_content').select('url', 'title', 'links').eq('chatbot_id', chatbot_id).execute()

            if response.data:
                return jsonify({
                    'message': 'Data retrieved successfully',
                    'status': 200,
                    'data': response.data
                }), 200
            else:
                return jsonify({
                    'message': 'No data found for the given chatbot ID',
                    'status': 404
                }), 404

        except Exception as e:
            return jsonify({
                'message': f'Error retrieving data: {str(e)}',
                'status': 500
            }), 500
    @scrape_bp.route('/delete-link', methods=['POST'])
    def delete_link_route():
        try:
            # Extract data from the JSON request body
            data = request.json
            chatbot_id = data.get('chatbotId')
            link_id = data.get('linkId')

            if not chatbot_id or not link_id:
                return jsonify({'message': 'Chatbot ID and Link ID are required', 'status': 400}), 400

            # Retrieve the existing chatbot data
            response = supabase.table('chatbot_scraped_content').select('id', 'links').eq('chatbot_id', chatbot_id).execute()
            if not response.data:
                return jsonify({'message': 'No data found for the given chatbot ID', 'status': 404}), 404

            # Process the data to remove the link
            updated = False
            for item in response.data:
                links = json.loads(item.get('links', '[]'))
                
                # Debugging: Print the current links
                print(f"Current links: {links}")
                
                updated_links = [link for link in links if link.get('id') != link_id]
                
                if len(links) != len(updated_links):  # Link was found and removed
                    # Update the record with the new links list
                    update_response = supabase.table('chatbot_scraped_content').update({'links': json.dumps(updated_links)}).eq('id', item['id']).execute()
                    if update_response.data:
                        updated = True
                    else:
                        return jsonify({'message': 'Failed to update the record', 'status': 500}), 500

            if updated:
                return jsonify({'message': 'Link removed successfully', 'status': 200}), 200
            else:
                return jsonify({'message': 'Link ID not found in the links list', 'status': 404}), 404

        except Exception as e:
            return jsonify({'message': f'Error processing request: {str(e)}', 'status': 500}), 500