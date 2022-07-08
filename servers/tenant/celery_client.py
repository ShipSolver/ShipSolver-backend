from celery import Celery
from celery.utils.log import get_logger
import os
import io
from uuid import uuid4
import traceback
# import tenant.controllers.DocumentController as document_controller
import PyPDF2
import extraction.app as ex
from celery import group

CELERY_BROKER_URL = 'redis://redis:6379/0'
client = Celery(__name__, broker=CELERY_BROKER_URL)
logger = get_logger(__name__)
FAILURE = -1
SUCCESS = 0
UPLOAD_FOLDER = "/opt/metadata-extraction/uploads"    


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