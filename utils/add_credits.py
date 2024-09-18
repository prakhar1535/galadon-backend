from db.db import supabase
from datetime import datetime
import uuid
def add_credits(data):
    id  = data.get('id', str(uuid.uuid4()))
    try:
        # Prepare the data for upsert
        credit_data = {
            'id': id,
            'chatbotId': data.get('chatbotId', ''),
            'credits': data.get('credits', 1),
            'updated_date': datetime.utcnow().isoformat(),
            
        }

        # Use upsert to insert or update the record
        response = supabase.table('credit').insert(credit_data).execute()
        
        if response.data:
            return {
                'message': 'Credits updated successfully',
                'status': 200,
                'data': [dict(item) for item in response.data]  # Convert each item to a dictionary
            }
        else:
            return {'message': 'Failed to update credits', 'status': 500}
    except Exception as e:
        return {'message': str(e), 'status': 500}