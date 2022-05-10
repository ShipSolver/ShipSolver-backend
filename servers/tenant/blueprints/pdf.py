import os
from flask import request, jsonify, Blueprint
from celery import group
import PyPDF2
import io
from uuid import uuid4
import traceback
from celery_client import client, logger
from controllers.pdfController import PDFController

pdf_bp = Blueprint("pdf_bp", __name__)

pdfcontroller = PDFController()


@pdf_bp.route("", methods=["POST"])
def pdf_post():
    if "file" not in request.files:
        res = jsonify({"message": "No file part in the request"})
        res.status_code = 400
        return res

    file = request.files["file"]

    if file.filename == "":
        res = jsonify({"message": "No file selected for uploading"})
        res.status_code = 400
        return res
    if file and file.filename.split(".")[-1].lower() == "pdf":
        pdfcontroller.process_files()
        resp = jsonify({"message": "File successfully uploaded"})
        resp.status_code = 200
        return resp
    else:
        resp = jsonify({"message": "Allowed file types are pdf only"})
        resp.status_code = 400
        return resp


@pdf_bp.route("{pdf_id}", methods=["GET"])
def pdf_get():
    res = jsonify({"message": "Please specify PDFId"})
    # TODO ...
    res.status_code = 400
    return res
