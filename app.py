from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all origins

# Configure upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'file' not in request.files and 'folder' not in request.files and 'text' not in request.form:
        return jsonify({"error": "No files or text provided"}), 400

    uploaded_files = request.files.getlist('file')
    folder_files = request.files.getlist('folder')
    text_data = request.form.get('text', '')

    response = {
        "files_saved": [],
        "folder_files_saved": [],
        "text_saved": False
    }

    # Save uploaded files
    for file in uploaded_files:
        if file.filename:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            response["files_saved"].append(filename)

    # Save folder files
    for file in folder_files:
        if file.filename:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            response["folder_files_saved"].append(filename)

    # Save text data
    if text_data:
        text_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'uploaded_text.txt')
        with open(text_file_path, 'w') as text_file:
            text_file.write(text_data)
        response["text_saved"] = True

    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)
