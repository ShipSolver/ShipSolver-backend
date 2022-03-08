import os
from flask import Flask, request, jsonify
from celery import Celery, group
from celery.utils.log import get_logger
import PyPDF2
import io
from uuid import uuid4
import extraction.app as ex
import traceback

FAILURE = -1
SUCCESS = 0
UPLOAD_FOLDER = "/opt/metadata-extraction/uploads"
CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
logger = get_logger(__name__)

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['CELERY_BROKER_URL'] = CELERY_BROKER_URL

client = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
client.conf.update(app.config)

@app.route('/dreceipt', methods=['POST'])
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
        tasks_to_run = fan_out(file)  # split up tasks

        do_all_work(tasks_to_run)  # run ocr pipeline for each task
        resp = jsonify({'message': 'File successfully uploaded'})
        resp.status_code = 200
        return resp
    else:
        resp = jsonify({'message': 'Allowed file types are pdf only'})
        resp.status_code = 400
        return resp


def fan_out(file):
    folder_uuid = uuid4()
    with io.BytesIO(file.read()) as open_pdf_file:
        read_pdf = PyPDF2.PdfFileReader(open_pdf_file)
        num_pages = read_pdf.getNumPages()
        folder = f"{app.config['UPLOAD_FOLDER']}/{folder_uuid}"
        os.mkdir(folder)
        for i in range(num_pages):
            output_pdf = PyPDF2.PdfFileWriter()
            output_pdf.addPage(read_pdf.getPage(i))
            file_uuid = uuid4()
            f_dir = f"{folder}/{file_uuid}"
            os.mkdir(f_dir)
            with open(f"{f_dir}/{file_uuid}.pdf", "wb") as f:
                output_pdf.write(f)
    file.close()
    pdf_folders = os.listdir(folder)
    return group([work.s(f"{folder}/{pdf_folder}") for pdf_folder in pdf_folders])


def do_all_work(tasks_to_run):
    result = tasks_to_run.apply_async()
    return result


@client.task
def work(pdf_folder):
    pdf_file = f"{pdf_folder}.pdf"
    try:
        ex.work(pdf_folder)
    except Exception as e:
        logger.info(f"file {pdf_folder}/{pdf_file} error. msg: {str(e)}")
        logger.info(traceback.format_exc())
        return {"status": FAILURE, "folder": pdf_folder}
    return {"status": SUCCESS, "folder": pdf_folder}



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')