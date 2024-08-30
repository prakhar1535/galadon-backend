from db.db import supabase

def update_chatbot(chatbot_id, data):
    update_data = {
        'fontColor': data.get('fontColor', ''),
        'themeColor': data.get('themeColor', ''),
        'user': data.get('user', []),
        'font': data.get('font', ''),
        'model': data.get('model', ''),
        'systemPrompt': data.get('systemPrompt', ''),
        'suggestedMessage': data.get('suggestedMessage', ''),
        'initialMessage': data.get('initialMessage', '')
    }

    response = supabase.table('chatbots').update(update_data).eq('chatbotId', chatbot_id).execute()

    if response.data:
        return {'message': 'Chatbot updated successfully', 'status': 200, 'data': response.data}
    elif response.error:
        return {'message': 'Failed to update chatbot', 'status': 400, 'error': response.error.message}
    else:
        return {'message': 'Unexpected response structure', 'status': 500}
