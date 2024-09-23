from db.db import supabase
from collections import defaultdict
from datetime import datetime, timezone
from dateutil import parser

def calculate_total_credits(client_id, start_date, end_date, start_timestamp, end_timestamp):
    try:
        # Query to get all chatbots for the client
        chatbots_response = supabase.table('chatbots').select('chatbotId').eq('client_id', client_id).execute()
        
        if not chatbots_response.data:
            return {'message': 'No chatbots found for the given client ID', 'status': 404}
        
        chatbot_ids = [chatbot['chatbotId'] for chatbot in chatbots_response.data]
        
        credits_per_day = defaultdict(int)
        total_credits_all_chatbots = 0
        
        # Query credits for all chatbots in a single query
        credit_response = supabase.table('credit').select('credits', 'updated_date') \
            .in_('chatbotId', chatbot_ids) \
            .gte('updated_date', start_date) \
            .lte('updated_date', end_date) \
            .execute()
        
        if credit_response.data:
            for entry in credit_response.data:
                try:
                    entry_date = parser.isoparse(entry['updated_date'])
                    credits = entry['credits']
                    credits_per_day[entry_date.date()] += credits
                    total_credits_all_chatbots += credits
                except Exception as e:
                    print(f"Error processing entry: {entry}, Error: {str(e)}")
        
        if not credits_per_day:
            return {'message': 'No credit data found for the given period', 'total_credits': 0, 'status': 404}
        
        perday_list = [
            {
                "date": date.isoformat(),
                "total_credits": total_credits
            }
            for date, total_credits in credits_per_day.items()
        ]
        
        result = {
            "chatbot_credits": [{"perday": perday_list}],
            "end_date": end_timestamp,
            "message": "Total credits calculated successfully",
            "start_date": start_timestamp,
            "status": 200,
            "total_credits_all_chatbots": total_credits_all_chatbots
        }
        
        return result
    except Exception as e:
        return {'message': str(e), 'status': 500}