from db.db import supabase

import uuid
def create_chatbot(data):
    chatbot_id = data.get('chatbotId', str(uuid.uuid4()))

    chatbot_data = {
        'chatbotId': chatbot_id,
        'fontColor': data.get('fontColor', ''),
        'themeColor': data.get('themeColor', ''),
        "user": data.get("user", []),
        'font': data.get('font', ''),
        'model': data.get('model', ''),
        'systemPrompt': data.get('systemPrompt', ''),
        'suggestedMessage': data.get('suggestedMessage', ''),
        "initialMessage": data.get("suggestedMessage", "")
    }

    response = supabase.table('chatbots').insert(chatbot_data).execute()

    if response.data:
        return {'message': 'Chatbot created successfully', 'status': 201, 'data': response.data}
    elif response.error:
        return {'message': 'Failed to create chatbot', 'status': 400, 'error': response.error.message}
    else:
        return {'message': 'Unexpected response structure', 'status': 500}