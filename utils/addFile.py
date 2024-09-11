from db.db import supabase

def upload_file(file, chatbot_id):
    if not file:
        return {'message': 'No file provided', 'status': 400}
    
    if not file.filename.endswith('.txt'):
        return {'message': 'Invalid file type. Please upload a .txt file', 'status': 400}
    
    try:
        content = file.read().decode('utf-8')
        
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
    except Exception as e:
        return {'message': str(e), 'status': 500}