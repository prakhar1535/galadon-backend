from flask import Blueprint, request, jsonify
from db.db import supabase
import json

def delete_file(chatbot_id, file_id):
    try:
        # Fetch the record with the given chatbot_id
        result = supabase.table("chatbot_scraped_content").select("id", "files").eq("chatbot_id", chatbot_id).execute()
        
        if not result.data:
            return {
                'message': 'No content found for the given chatbot ID',
                'status': 404
            }
        
        record = result.data[0]
        files = json.loads(record.get('files', '[]'))
        
        # Find and remove the file with the given file_id
        updated_files = [file for file in files if file.get('file_id') != file_id]
        
        if len(updated_files) == len(files):
            return {
                'message': 'File not found with the given file ID',
                'status': 404
            }
        
        # Update the record with the new files list
        data, count = supabase.table("chatbot_scraped_content").update({"files": json.dumps(updated_files)}).eq("id", record['id']).execute()
        
        return {
            'message': 'File deleted successfully',
            'status': 200,
            'data': {'id': record['id'], 'deleted_file_id': file_id}
        }
    except Exception as e:
        return {'message': f"Error deleting file: {str(e)}", 'status': 500}