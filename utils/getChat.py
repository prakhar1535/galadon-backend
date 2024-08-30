from db.db import supabase

def get_chat(user_id):
    user_response = supabase.table('users').select('messages').eq('userId', user_id).execute()
    
    if not user_response.data:
        return {'message': 'User not found', 'status': 404}
    
    messages = user_response.data[0].get('messages', [])
    
    return {'message': 'Messages retrieved successfully', 'status': 200, 'data': messages}
