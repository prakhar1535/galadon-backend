from db.db import supabase
from datetime import datetime

def calculate_total_credits(chatbot_id, start_date, end_date):
    try:
        # Convert string dates to datetime objects
        start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
        end_datetime = datetime.strptime(end_date, "%Y-%m-%d")

        # Fetch all credit entries for the given chatbot_id within the date range
        response = supabase.table('credit').select('credits', 'updated_date') \
            .eq('chatbotId', chatbot_id) \
            .gte('updated_date', start_datetime.isoformat()) \
            .lte('updated_date', end_datetime.isoformat()) \
            .execute()

        if not response.data:
            return {'message': 'No credit data found for the given period', 'total_credits': 0, 'status': 404}

        # Calculate total credits
        total_credits = sum(entry['credits'] for entry in response.data)

        return {
            'message': 'Total credits calculated successfully',
            'total_credits': total_credits,
            'start_date': start_date,
            'end_date': end_date,
            'status': 200
        }
    except Exception as e:
        return {'message': str(e), 'status': 500}