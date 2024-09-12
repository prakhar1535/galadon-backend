from db.db import supabase
from datetime import datetime

def get_credits(chatbot_id, start_date, end_date):
    try:
        # Convert start_date and end_date to ISO format if they're not already
        if isinstance(start_date, str):
            start_date = datetime.fromisoformat(start_date).isoformat()
        if isinstance(end_date, str):
            end_date = datetime.fromisoformat(end_date).isoformat()

        # Query the database
        response = supabase.table('credit') \
            .select('credits, updated_date') \
            .eq('chatbotId', chatbot_id) \
            .gte('updated_date', start_date) \
            .lte('updated_date', end_date) \
            .execute()

        if response.data:
            # Sum up the credits
            total_credits = sum(item['credits'] for item in response.data)
            
            return {
                'message': 'Credits retrieved successfully',
                'status': 200,
                'data': {
                    'chatbotId': chatbot_id,
                    'total_credits': total_credits,
                    'start_date': start_date,
                    'end_date': end_date,
                    'entries': response.data
                }
            }
        else:
            return {
                'message': 'No credits found for the specified chatbot and date range',
                'status': 404,
                'data': {
                    'chatbotId': chatbot_id,
                    'total_credits': 0,
                    'start_date': start_date,
                    'end_date': end_date,
                    'entries': []
                }
            }
    except Exception as e:
        return {'message': str(e), 'status': 500}