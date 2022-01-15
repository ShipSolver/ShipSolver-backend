from flask import Flask, render_template, request, jsonify
from uuid import uuid4
import os

import extraction.extract as e

UPLOAD_FOLDER = "/home/dante/WLP/metadata-extraction/uploads"

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route('/upload', methods=['GET', 'POST'])
def pdf_upload():
    if 'file' not in request.files:
        res = jsonify({'message': 'No file part in the request'})
        res.status_code = 400
        return res
    file = request.files['file']
    if file.filename == '':
        res = jsonify({'message': 'No file selected for uploading'})
        res.status_code = 400
        return res
    if file and file.filename.split(".")[-1].lower() == "pdf":
        file_uuid = uuid4()
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], f"{file_uuid}.pdf"))
        file.close()
        resp = jsonify({'message': 'File successfully uploaded'})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify({'message': 'Allowed file types are pdf only'})
        resp.status_code = 400
        return resp


if __name__ == '__main__':
    app.run(debug=True)