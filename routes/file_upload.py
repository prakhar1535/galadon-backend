from flask import Blueprint, request, jsonify
from utils.addFile import upload_file

class FileUploadRoutes:
    file_upload_bp = Blueprint('file_upload_bp', __name__)

    @file_upload_bp.route('/upload/<chatbot_id>', methods=['POST'])
    def upload_file_route(chatbot_id):
        if 'file' not in request.files:
            return jsonify({"message": "No file part"}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({"message": "No selected file"}), 400
        
        result = upload_file(file, chatbot_id)
        return jsonify(result), result['status']