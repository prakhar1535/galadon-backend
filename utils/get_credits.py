from db.db import supabase

def calculate_total_credits(client_id, start_date, end_date, start_timestamp, end_timestamp):
    try:
        chatbots_response = supabase.table('chatbots').select('chatbotId').eq('client_id', client_id).execute()

        if not chatbots_response.data:
            return {'message': 'No chatbots found for the given client ID', 'status': 404}

        chatbot_credits = []
        total_credits_all_chatbots = 0

        for chatbot in chatbots_response.data:
            chatbot_id = chatbot['chatbotId']

            credit_response = supabase.table('credit').select('credits', 'updated_date') \
                .eq('chatbotId', chatbot_id) \
                .gte('updated_date', start_date) \
                .lte('updated_date', end_date) \
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