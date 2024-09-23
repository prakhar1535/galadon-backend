from db.db import supabase
from datetime import datetime

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

        # Process the leads data and convert created_at to Unix timestamp
        leads = []
        for lead in leads_response.data:
            lead_copy = lead.copy()
            if lead_copy.get('created_at'):
                try:
                    # Convert created_at to Unix timestamp
                    created_at = datetime.fromisoformat(lead_copy['created_at'].replace('Z', '+00:00'))
                    lead_copy['created_at'] = int(created_at.timestamp())
                except ValueError:
                    # If conversion fails, set to None
                    print(f"Warning: Unable to convert created_at for lead {lead_copy.get('id', 'unknown')}")
                    lead_copy['created_at'] = None
            leads.append(lead_copy)

        return {
            'message': 'Leads fetched successfully',
            'status': 200,
            'data': leads,
            'total_leads': len(leads)
        }

    except Exception as e:
        return {'message': f'Error fetching leads: {str(e)}', 'status': 500}