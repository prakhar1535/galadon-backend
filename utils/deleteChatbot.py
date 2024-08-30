from db.db import supabase

def delete_chatbot(chatbot_id):
    response = supabase.table('chatbots').delete().eq('chatbotId', chatbot_id).execute()

    if response.data:
        return {'message': 'Chatbot deleted successfully', 'status': 200}
    elif response.error:
        return {'message': 'Failed to delete chatbot', 'status': 400, 'error': response.error.message}
    else:
        return {'message': 'Unexpected response structure', 'status': 500}
