from db.db import supabase
def create_client(data):
    chatbot_data = {
        'chatbotId': data.get('chatbot_id', ''),
        'client_id': data.get('client_id', ''),
        'credits' : 0
    }

    response = supabase.table('client').insert(chatbot_data).execute()

    if response.data:
        return {'message': 'Chatbot created successfully', 'status': 201, 'data': response.data}
    elif response.error:
        return {'message': 'Failed to create chatbot', 'status': 400, 'error': response.error.message}
    else:
        return {'message': 'Unexpected response structure', 'status': 500}