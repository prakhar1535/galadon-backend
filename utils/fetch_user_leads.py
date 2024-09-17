from db.db import supabase
def fetch_user_leads(user_id):
    try:
        # Fetch leads for the specific user ID
        leads_response = supabase.table('leads').select('*').eq('user_id', user_id).execute()

        if not leads_response.data:
            return {'message': 'No leads found for the given user ID', 'status': 404}

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