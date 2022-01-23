import os
from flask import Flask, render_template, request, jsonify
import PyPDF2
import io
from uuid import uuid4
import extraction.app as e
UPLOAD_FOLDER = "/home/dante/WLP/metadata-extraction/uploads"

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route('/upload', methods=['POST'])
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
        folder_uuid = uuid4()
        with io.BytesIO(file.read()) as open_pdf_file:
            read_pdf = PyPDF2.PdfFileReader(open_pdf_file)
            num_pages = read_pdf.getNumPages()
            folder_dir = f"{app.config['UPLOAD_FOLDER']}/{folder_uuid}"
            os.mkdir(folder_dir)
            for i in range(num_pages):
                output_pdf = PyPDF2.PdfFileWriter()
                output_pdf.addPage(read_pdf.getPage(i))
                file_uuid = uuid4()
                f_dir = f"{folder_dir}/{file_uuid}"
                os.mkdir(f_dir)
                with open(f"{f_dir}/{file_uuid}.pdf", "wb") as f:
                    output_pdf.write(f)
        file.close()
        e.fan_out(folder_dir)
        resp = jsonify({'message': 'File successfully uploaded'})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify({'message': 'Allowed file types are pdf only'})
        resp.status_code = 400
        return resp


if __name__ == '__main__':
    app.run(debug=True)