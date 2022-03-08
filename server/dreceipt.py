import os
from flask import request, jsonify, Blueprint
from celery import group
import PyPDF2
import io
from uuid import uuid4
import extraction.app as ex
import traceback
from server.celery_client import client, logger

FAILURE = -1
SUCCESS = 0
UPLOAD_FOLDER = "/opt/metadata-extraction/uploads"
dreceipt_bp = Blueprint("dreceipt_bp", __name__)

@dreceipt_bp.route('pdf', methods=['POST'])
def dreceipt_pdf():
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
        folder = f"{UPLOAD_FOLDER}/{folder_uuid}"
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
        doclist = ex.work(pdf_folder)
    except Exception as e:
        logger.info(f"file {pdf_folder}/{pdf_file} error. msg: {str(e)}")
        logger.info(traceback.format_exc())
        return {"status": FAILURE, "folder": pdf_folder}
    return {"status": SUCCESS, "folder": pdf_folder, "doclist": doclist}

