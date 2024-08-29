from flask import jsonify, request
from db.db import supabase

def get_session():
    chatbot_id = request.json.get('chatbotId')

    if not chatbot_id:
        return {"error": "chatbotId is required"}, 400

    # Fetch data from Supabase based on chatbotId
    response = supabase.table('chatbots').select('*').eq('chatbotId', chatbot_id).execute()

    if not response.data:
        return {"error": "Session not found"}, 404

    # Assuming there's only one session per chatbotId
    session_data = response.data[0]

    return session_data, 200
