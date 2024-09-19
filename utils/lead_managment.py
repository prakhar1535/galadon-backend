from db.db import supabase
from datetime import datetime, timezone

def manage_lead(data):
    user_id = data.get('user_id')
    field = data.get('field')
    value = data.get('value')
    current_time = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S+00')

    if not user_id or not field or value is None:
        return {'message': 'Missing required fields', 'status': 400}

    try:
        # Check if the lead exists
        result = supabase.table('leads').select('*').eq('user_id', user_id).execute()
        
        if len(result.data) == 0:
            # If lead doesn't exist, create a new one
            new_lead = {
                'user_id': user_id,
                field: value,
                'created_at': current_time,
                
            }
            response = supabase.table('leads').insert(new_lead).execute()
        else:
            # If lead exists, update the specific field
            update_data = {
                field: value,
                'created_at': current_time
            }
            response = supabase.table('leads').update(update_data).eq('user_id', user_id).execute()

        if response.data:
            return {'message': 'Lead information updated successfully', 'status': 200, 'data': response.data}
        elif response.error:
            return {'message': 'Failed to update lead information', 'status': 400, 'error': response.error.message}
        else:
            return {'message': 'Unexpected response structure', 'status': 500}
    
    except Exception as e:
        return {'message': f'Error updating lead information: {str(e)}', 'status': 500}