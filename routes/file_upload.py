from flask import Blueprint, request, jsonify
from utils.addFile import upload_file

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