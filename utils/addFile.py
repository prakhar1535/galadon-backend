from db.db import supabase
import requests

def upload_file(file_or_url, chatbot_id, is_url=False):
    try:
        if is_url:
            # Handle cloud link
            response = requests.get(file_or_url)
            response.raise_for_status()  # Raise an exception for bad status codes
            content = response.text
        else:
            # Handle file upload
            if not file_or_url:
                return {'message': 'No file provided', 'status': 400}
            
            if not file_or_url.filename.endswith('.txt'):
                return {'message': 'Invalid file type. Please upload a .txt file', 'status': 400}
            
            content = file_or_url.read().decode('utf-8')
        
        # Check if a record with the given chatbot_id already exists
        result = supabase.table("chatbot_scraped_content").select("id").eq("chatbot_id", chatbot_id).execute()
        
        if result.data:
            # If record exists, update it
            data, count = supabase.table("chatbot_scraped_content").update({"file": content}).eq("chatbot_id", chatbot_id).execute()
            message = 'File content updated successfully'
        else:
            # If record doesn't exist, insert a new one
            data, count = supabase.table("chatbot_scraped_content").insert({"chatbot_id": chatbot_id, "file": content}).execute()
            message = 'File uploaded and content stored successfully'
        
        return {
            'message': message,
            'status': 200,
            'data': {'id': data[1][0]['id']}
        }
    except requests.RequestException as e:
        return {'message': f"Error fetching file from URL: {str(e)}", 'status': 500}
    except Exception as e:
        return {'message': str(e), 'status': 500}