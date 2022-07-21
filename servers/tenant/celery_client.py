from celery import Celery
from celery.utils.log import get_logger
import os
import io
from uuid import uuid4
import traceback
<<<<<<< HEAD
import PyPDF2
import extraction.app as ex
import extraction.extract as ext
=======
# import tenant.controllers.DocumentController as document_controller
import PyPDF2
import extraction.app as ex
>>>>>>> 32dee55d98864ba43414c8757ab4abe2e4881f66
from celery import group

from tenant.controllers.DocumentController import DocumentController
import boto3


# def get_file_s3():
#     s3_client = boto3.client('s3')
#     TENANT = "test-tenant1"
#     BUCKET = f"{TENANT}-bucket"
#     OBJECT = 'signatures/cook-with-roommates-bonus-carbonara.jpg'

#     download_url = s3_client.generate_presigned_url(
#         'get_object',
#         Params={'Bucket': BUCKET, 'Key': OBJECT, 'ResponseContentDisposition': 'attachment'},
#         ExpiresIn=600)

#     view_url = s3_client.generate_presigned_url(
#         'get_object',
#         Params={'Bucket': BUCKET, 'Key': OBJECT},
#         ExpiresIn=600)
TENANT = "test-tenant1"
BUCKET = f"{TENANT}-bucket"
aws_access_key_id = os.getenv("aws_access_key_id")
aws_secret_access_key = os.getenv("aws_secret_access_key")
print(aws_secret_access_key, aws_access_key_id)
CELERY_BROKER_URL = 'redis://redis:6379/0'
client = Celery(__name__, broker=CELERY_BROKER_URL)
logger = get_logger(__name__)
FAILURE = -1
SUCCESS = 0
<<<<<<< HEAD
PIECES_SEPERATOR = ",+-"
UPLOAD_FOLDER = "/opt/metadata-extraction/uploads"    
s3 = boto3.resource('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
bucket = s3.Bucket(BUCKET)

def fan_out(file, documentStatusId):
=======
UPLOAD_FOLDER = "/opt/metadata-extraction/uploads"    


def fan_out(file):
>>>>>>> 32dee55d98864ba43414c8757ab4abe2e4881f66
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
<<<<<<< HEAD

            bucket.upload_file(f"{f_dir}/{file_uuid}.pdf", f"documents/{folder_uuid}/{file_uuid}.pdf")
    file.close()
    pdf_folders = os.listdir(folder)
    return group([work.s(f"{folder}/{pdf_folder}", documentStatusId) for pdf_folder in pdf_folders])
=======
    file.close()
    pdf_folders = os.listdir(folder)
    return group([work.s(f"{folder}/{pdf_folder}") for pdf_folder in pdf_folders])
>>>>>>> 32dee55d98864ba43414c8757ab4abe2e4881f66


def do_all_work(tasks_to_run):
    result = tasks_to_run.apply_async()
    return result


@client.task
<<<<<<< HEAD
def work(pdf_folder, documentStatusId):
    document_controller = DocumentController()
    pdf_file = f"{pdf_folder}.pdf"
    try:
        doclist = ex.work(pdf_folder)
        doclist["orderS3Link"] = f"s3://{BUCKET}/documents/{pdf_file.replace(UPLOAD_FOLDER, '')}"
        doclist["pieces"] = PIECES_SEPERATOR.join(doclist["pieces"])
        doclist["documentStatusId"] = documentStatusId
        doclist["success"] = True
        document_controller._create(doclist)
    except Exception as e:
        logger.info(f"file {pdf_folder}/{pdf_file} error. msg: {str(e)}")
        logger.info(traceback.format_exc())
        doclist = ext.generate_doclist({})
        doclist["orderS3Link"] = f"s3://{BUCKET}/documents/{pdf_file.replace(UPLOAD_FOLDER, '')}"
        doclist["pieces"] = PIECES_SEPERATOR.join(doclist["pieces"])
        doclist["documentStatusId"] = documentStatusId
        doclist["success"] = False
        document_controller._create(doclist)
=======
def work(pdf_folder):
    pdf_file = f"{pdf_folder}.pdf"
    try:
        doclist = ex.work(pdf_folder)
    except Exception as e:
        logger.info(f"file {pdf_folder}/{pdf_file} error. msg: {str(e)}")
        logger.info(traceback.format_exc())
>>>>>>> 32dee55d98864ba43414c8757ab4abe2e4881f66
        return {"status": FAILURE, "folder": pdf_folder}
    return {"status": SUCCESS, "folder": pdf_folder, "doclist": doclist}