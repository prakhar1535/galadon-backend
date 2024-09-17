from flask import Blueprint, request, jsonify
from db.db import supabase

def delete_file(chatbot_id):
    try:
        # Check if a record with the given chatbot_id exists
        result = supabase.table("chatbot_scraped_content").select("id").eq("chatbot_id", chatbot_id).execute()
        
        if result.data:
            # If record exists, delete it
            data, count = supabase.table("chatbot_scraped_content").delete().eq("chatbot_id", chatbot_id).execute()
            return {
                'message': 'File content deleted successfully',
                'status': 200,
                'data': {'id': data[1][0]['id'] if data and data[1] else None}
            }
        else:
            return {
                'message': 'No file content found for the given chatbot ID',
                'status': 404
            }
    except Exception as e:
        return {'message': f"Error deleting file: {str(e)}", 'status': 500}