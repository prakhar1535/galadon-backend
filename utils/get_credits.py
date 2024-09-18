from db.db import supabase
from datetime import datetime, timezone

def calculate_total_credits(client_id, start_timestamp, end_timestamp):
    try:
        # Convert Unix timestamps to datetime objects
        start_datetime = datetime.fromtimestamp(start_timestamp, tz=timezone.utc)
        end_datetime = datetime.fromtimestamp(end_timestamp, tz=timezone.utc)

        # Convert datetime objects to date strings in ISO format
        start_date_str = start_datetime.date().isoformat()
        end_date_str = end_datetime.date().isoformat()

        # Fetch all chatbots for the given client_id
        chatbots_response = supabase.table('chatbots').select('chatbotId').eq('client_id', client_id).execute()

        if not chatbots_response.data:
            return {'message': 'No chatbots found for the given client ID', 'status': 404}

        chatbot_credits = []
        total_credits_all_chatbots = 0

        for chatbot in chatbots_response.data:
            chatbot_id = chatbot['chatbotId']

            # Fetch credit entries for the current chatbot_id within the date range
            credit_response = supabase.table('credit').select('credits', 'updated_date') \
                .eq('chatbotId', chatbot_id) \
                .gte('updated_date', start_date_str) \
                .lte('updated_date', end_date_str) \
                .execute()

            if credit_response.data:
                chatbot_total_credits = sum(entry['credits'] for entry in credit_response.data)
                total_credits_all_chatbots += chatbot_total_credits
                chatbot_credits.append({
                    'chatbot_id': chatbot_id,
                    'total_used_credits': chatbot_total_credits,
                    'start_date': start_timestamp,
                    'end_date': end_timestamp
                })

        if not chatbot_credits:
            return {'message': 'No credit data found for the given period', 'total_credits': 0, 'status': 404}

        return {
            'message': 'Total credits calculated successfully',
            'chatbot_credits': chatbot_credits,
            'total_credits_all_chatbots': total_credits_all_chatbots,
            'start_date': start_timestamp,
            'end_date': end_timestamp,
            'status': 200
        }
    except Exception as e:
        return {'message': str(e), 'status': 500}