from db.db import supabase
def fetch_leads(chatbot_id):
        try:
            # First, fetch the user array from the chatbots table
            chatbot_response = supabase.table('chatbots').select('user').eq('chatbotId', chatbot_id).execute()

            if not chatbot_response.data:
                return {'message': 'Chatbot not found', 'status': 404}

            user_array = chatbot_response.data[0].get('user', [])

            # Extract user IDs from the user array
            user_ids = [user.get('userId') for user in user_array if isinstance(user, dict) and 'userId' in user]

            if not user_ids:
                return {'message': 'No user IDs found for this chatbot', 'status': 404}

            # Now, fetch leads for these user IDs
            leads_response = supabase.table('leads').select('*').in_('user_id', user_ids).execute()

            if not leads_response.data:
                return {'message': 'No leads found for the given user IDs', 'status': 404}

            # Process and return the leads data
            leads = leads_response.data
            return {
                'message': 'Leads fetched successfully',
                'status': 200,
                'data': leads,
                'total_leads': len(leads)
            }

        except Exception as e:
            return {'message': f'Error fetching leads: {str(e)}', 'status': 500}
        