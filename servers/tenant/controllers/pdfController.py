import os
from flask import request, jsonify, Blueprint
# from celery import group
# import PyPDF2
import io
from uuid import uuid4
import sys

sys.path.insert(0, "../../")  # import parent folder

import extraction.app as ex
import traceback
from celery_client import client, logger

FAILURE = -1
SUCCESS = 0
UPLOAD_FOLDER = "/opt/metadata-extraction/uploads"


class PDFController:
    def process_files(self, file):

        tasks_to_run = self.fan_out(file)  # split up tasks

        self.do_all_work(tasks_to_run)  # run ocr pipeline for each task
        result = tasks_to_run.apply_async()
        return result

    def do_all_work(self, tasks_to_run):
        result = tasks_to_run.apply_async()
        return result

    def fan_out(self, file):
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
        return group(
            [self.work.s(f"{folder}/{pdf_folder}") for pdf_folder in pdf_folders]
        )

    @client.task
    def work(self, pdf_folder):
        pdf_file = f"{pdf_folder}.pdf"
        try:
            doclist = ex.work(pdf_folder)
        except Exception as e:
            logger.info(f"file {pdf_folder}/{pdf_file} error. msg: {str(e)}")
            logger.info(traceback.format_exc())
            return {"status": FAILURE, "folder": pdf_folder}
        return {"status": SUCCESS, "folder": pdf_folder, "doclist": doclist}
