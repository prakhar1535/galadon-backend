from db.db import supabase

def update_chatbot(chatbot_id, data):
    # Remove chatbotId from data if present, as it shouldn't be updated
    data.pop('chatbotId', None)

    if not data:
        return {'message': 'No data provided for update', 'status': 400}

    try:
        response = supabase.table('chatbots').update(data).eq('chatbotId', chatbot_id).execute()

        if response.data:
            return {'message': 'Chatbot updated successfully', 'status': 200, 'data': response.data}
        else:
            return {'message': 'No chatbot found with the given ID', 'status': 404}
    except Exception as e:
        return {'message': f'Failed to update chatbot: {str(e)}', 'status': 500}