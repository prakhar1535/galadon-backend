from flask import request, jsonify

@app.route('/get_credits', methods=['GET'])
def get_credits_route():
    chatbot_id = request.args.get('chatbotId')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if not all([chatbot_id, start_date, end_date]):
        return jsonify({'message': 'Missing required parameters', 'status': 400}), 400

    result = get_credits(chatbot_id, start_date, end_date)
    return jsonify(result), result['status']