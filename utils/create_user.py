import uuid
from db.db import supabase

def create_user(data):
    user_id = data.get('userId', str(uuid.uuid4()))
    user_data = {
        'userId': user_id,
        'chatbotId': data.get('chatbotId'),
        'messages': data.get('messages', [])
    }

    chatbot_response = supabase.table('chatbots').select('*').eq('chatbotId', user_data['chatbotId']).execute()
    if not chatbot_response.data:
        return {'message': 'Chatbot not found', 'status': 404}

    user_response = supabase.table('users').insert(user_data).execute()

    if user_response.data:

        updated_users = chatbot_response.data[0]['user'] + [{'userId': user_id}]
        update_response = supabase.table('chatbots').update({'user': updated_users}).eq('chatbotId', user_data['chatbotId']).execute()

        if update_response.data:
            return {'message': 'User created and chatbot updated successfully', 'status': 201, 'data': user_response.data}
        else:
            return {'message': 'User created but failed to update chatbot', 'status': 500, 'error': update_response.error.message}

    elif user_response.error:
        return {'message': 'Failed to create user', 'status': 400, 'error': user_response.error.message}
    else:
        return {'message': 'Unexpected response structure', 'status': 500}
