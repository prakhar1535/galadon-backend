from db.db import supabase
from datetime import datetime, timezone

def calculate_total_credits(chatbot_id, start_timestamp, end_timestamp):
    try:
        # Convert Unix timestamps to datetime objects
        start_datetime = datetime.fromtimestamp(start_timestamp, tz=timezone.utc)
        end_datetime = datetime.fromtimestamp(end_timestamp, tz=timezone.utc)

        # Convert datetime objects to date strings in ISO format
        start_date_str = start_datetime.date().isoformat()
        end_date_str = end_datetime.date().isoformat()

        # Fetch all credit entries for the given chatbot_id within the date range
        response = supabase.table('credit').select('credits', 'updated_date') \
            .eq('chatbotId', chatbot_id) \
            .gte('updated_date', start_date_str) \
            .lte('updated_date', end_date_str) \
            .execute()

        if not response.data:
            return {'message': 'No credit data found for the given period', 'total_credits': 0, 'status': 404}

        # Calculate total credits
        total_credits = sum(entry['credits'] for entry in response.data)

        return {
            'message': 'Total credits calculated successfully',
            'total_credits': total_credits,
            'start_date': start_timestamp,
            'end_date': end_timestamp,
            'status': 200
        }
    except Exception as e:
        return {'message': str(e), 'status': 500}