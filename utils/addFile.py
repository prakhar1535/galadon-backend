from db.db import supabase
import requests
import uuid
import json

def upload_file(file_or_url, chatbot_id, is_url=False):
    try:
        new_file_entry = {
            "file_id": str(uuid.uuid4()),
            "file_url": file_or_url if is_url else None,
            "file_content": None
        }

        if is_url:
            # Handle cloud link
            response = requests.get(file_or_url)
            response.raise_for_status()  # Raise an exception for bad status codes
            new_file_entry["file_content"] = response.text
        else:
            # Handle file upload
            if not file_or_url:
                return {'message': 'No file provided', 'status': 400}
            
            if not file_or_url.filename.endswith('.txt'):
                return {'message': 'Invalid file type. Please upload a .txt file', 'status': 400}
            
            new_file_entry["file_content"] = file_or_url.read().decode('utf-8')
        
        # Check if a record with the given chatbot_id already exists
        result = supabase.table("chatbot_scraped_content").select("id", "files").eq("chatbot_id", chatbot_id).execute()
        
        if result.data:
            # If record exists, update it by appending the new file entry
            existing_files = result.data[0].get('files')
            if existing_files is None:
                existing_files = []
            elif isinstance(existing_files, str):
                existing_files = json.loads(existing_files)
            existing_files.append(new_file_entry)
            data, count = supabase.table("chatbot_scraped_content").update({"files": json.dumps(existing_files)}).eq("chatbot_id", chatbot_id).execute()
            message = 'File content added successfully'
        else:
            # If record doesn't exist, insert a new one with the file entry in a JSON array
            data, count = supabase.table("chatbot_scraped_content").insert({
                "chatbot_id": chatbot_id, 
                "files": json.dumps([new_file_entry])
            }).execute()
            message = 'File uploaded and content stored successfully'
        
        return {
            'message': message,
            'status': 200,
            'data': {
                'id': data[1][0]['id'],
                'file_id': new_file_entry['file_id']
            }
        }
    except requests.RequestException as e:
        return {'message': f"Error fetching file from URL: {str(e)}", 'status': 500}
    except json.JSONDecodeError as e:
        return {'message': f"Error parsing JSON: {str(e)}", 'status': 500}
    except Exception as e:
        return {'message': str(e), 'status': 500}