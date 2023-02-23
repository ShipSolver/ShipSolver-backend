from celery import Celery
from celery.utils.log import get_logger
import os
import io
from uuid import uuid4
import traceback
import PyPDF2
import extraction.app as ex
import extraction.extract as ext
from celery import group

from tenant.controllers.DocumentController import DocumentController
import boto3
from botocore.client import Config

TENANT = "test-tenant2"
BUCKET = f"{TENANT}-bucket"
aws_access_key_id = os.getenv("aws_access_key_id")
aws_secret_access_key = os.getenv("aws_secret_access_key")
CELERY_BROKER_URL = 'redis://redis:6379/0'
client = Celery(__name__, broker=CELERY_BROKER_URL)
logger = get_logger(__name__)
FAILURE = -1
SUCCESS = 0
PIECES_SEPERATOR = ",+-"
UPLOAD_FOLDER = "tenant/uploads"
UPLOAD_FOLDER_CELERY = "uploads"
s3 = boto3.resource('s3', region_name='us-east-2', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, config=Config(signature_version='s3v4'))
bucket = s3.Bucket(BUCKET)
s3_client = boto3.client('s3', region_name='us-east-2', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, config=Config(signature_version='s3v4'))

def fan_out(file, documentStatusId):
    if not os.path.exists(UPLOAD_FOLDER):
        os.mkdir(UPLOAD_FOLDER)
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

            bucket.upload_file(f"{f_dir}/{file_uuid}.pdf", f"documents/{folder_uuid}/{file_uuid}.pdf")
    file.close()
    pdf_folders = os.listdir(folder)
    celery_folder = f"{UPLOAD_FOLDER_CELERY}/{folder_uuid}"
    return group([work.s(f"{celery_folder}/{pdf_folder}", documentStatusId) for pdf_folder in pdf_folders])


def do_all_work(tasks_to_run):
    result = tasks_to_run.apply_async()
    return result


@client.task
def work(pdf_folder, documentStatusId, UPLOAD_FOLDER):
    document_controller = DocumentController()
    pdf_file = f"{pdf_folder}.pdf"
    OBJECT = f"documents{pdf_file.replace(UPLOAD_FOLDER_CELERY, '')}"
    view_url = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': BUCKET, 'Key': OBJECT},
        ExpiresIn=3600)
    try:
        doclist = ex.work(pdf_folder)
        doclist["orderS3Path"] = f"s3://{BUCKET}/{OBJECT}"
        doclist["orderS3Link"] = view_url
        doclist["pieces"] = PIECES_SEPERATOR.join(doclist["pieces"])
        doclist["documentStatusId"] = documentStatusId
        doclist["success"] = True
        print(doclist)
        document_controller._create(doclist)
    except Exception as e:
        logger.info(f"file {pdf_folder}/{pdf_file} error. msg: {str(e)}")
        logger.info(traceback.format_exc())
        doclist = ext.generate_doclist({})
        doclist["orderS3Path"] = f"s3://{BUCKET}/{OBJECT}"
        doclist["orderS3Link"] = view_url
        doclist["pieces"] = PIECES_SEPERATOR.join(doclist["pieces"])
        doclist["documentStatusId"] = documentStatusId
        doclist["success"] = False
        document_controller._create(doclist)
        return {"status": FAILURE, "folder": pdf_folder}
    return {"status": SUCCESS, "folder": pdf_folder, "doclist": doclist}