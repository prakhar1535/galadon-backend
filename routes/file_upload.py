from flask import Blueprint, request, jsonify
from utils.addFile import upload_file
from utils.deleteFile import delete_file

class FileUploadRoutes:
    file_upload_bp = Blueprint('file_upload_bp', __name__)

    @file_upload_bp.route('/upload/<chatbot_id>', methods=['POST'])
    def upload_file_route(chatbot_id):
        if 'file' in request.files:
            file = request.files['file']
            result = upload_file(file, chatbot_id)
        elif 'url' in request.form:
            url = request.form['url']
            result = upload_file(url, chatbot_id, is_url=True)
        else:
            return jsonify({"message": "No file or URL provided"}), 400

        return jsonify(result), result['status']
    @file_upload_bp.route('/delete-file', methods=['DELETE'])
    def delete_file_route():
        data = request.json
        chatbot_id = data.get('chatbot_id')
        file_id = data.get('file_id')

        if not chatbot_id or not file_id:
            return jsonify({'message': 'Both chatbot_id and file_id are required', 'status': 400}), 400

        result = delete_file(chatbot_id, file_id)
        return jsonify(result), result['status']
