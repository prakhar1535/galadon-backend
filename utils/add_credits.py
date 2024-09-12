from db.db import supabase

def add_credits(chatbot_id, credits):
    try:
        # Directly update the credits
        response = supabase.table('chatbots').update({'credits': credits}).eq('chatbotId', chatbot_id).execute()
        
        if response.data:
            return {
                'message': 'Credits updated successfully',
                'status': 200,
                'data': {'chatbotId': chatbot_id, 'credits': credits}
            }
        else:
            return {'message': 'Failed to update credits or chatbot not found', 'status': 404}
    except Exception as e:
        return {'message': str(e), 'status': 500}