from db.db import supabase

import uuid
def create_chatbot(data):
    chatbot_id = data.get('chatbotId', str(uuid.uuid4()))

    chatbot_data = {
        'chatbotId': chatbot_id,
        "user": data.get("user", []),
        'model': data.get('model', ''),
        'systemPrompt': data.get('systemPrompt', ''),
        'suggestedMessage': data.get('suggestedMessage', ''),
        "initialMessage": data.get("initialMessage", ""),
        'get_user_name': data.get('get_user_name', True),
        'get_user_email': data.get('get_user_email', True),
        'get_user_phone': data.get('get_user_phone', True),
        'branding': data.get('branding', True),
        'status': data.get('status', True),
        'send_email': data.get('send_email', []),
        'name_msg': data.get('name_msg', ''),
        'email_msg': data.get('email_msg', ''),
        'phone_msg': data.get('phone_msg', ''),
        'client_id': data.get('client_id', ''),
        'chatbot_name': data.get('chatbot_name', ''),
        'avatarUrl': data.get('avatarUrl', ''),
        'themeColor': data.get('themeColor', ''),
        'fontColor': data.get('fontColor', '')
    }

    response = supabase.table('chatbots').insert(chatbot_data).execute()

    if response.data:
        return {'message': 'Chatbot created successfully', 'status': 201, 'data': response.data}
    elif response.error:
        return {'message': 'Failed to create chatbot', 'status': 400, 'error': response.error.message}
    else:
        return {'message': 'Unexpected response structure', 'status': 500}