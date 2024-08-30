import uuid
from db.db import supabase

def add_chat(data):
    user_id = data.get('userId')
    new_messages = data.get('messages', [])
    user_response = supabase.table('users').select('*').eq('userId', user_id).execute()
    if not user_response.data:
        return {'message': 'User not found', 'status': 404}
    existing_messages = user_response.data[0].get('messages', [])
    updated_messages = existing_messages + new_messages
    update_response = supabase.table('users').update({'messages': updated_messages}).eq('userId', user_id).execute()

    if update_response.data:
        return {'message': 'Messages added successfully', 'status': 200, 'data': update_response.data}
    else:
        return {'message': 'Failed to update messages', 'status': 500, 'error': update_response.error.message}
