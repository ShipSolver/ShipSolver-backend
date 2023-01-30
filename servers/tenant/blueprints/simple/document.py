import os
from flask import request, jsonify, Blueprint
import io
from uuid import uuid4
import traceback

from celery_client import client, logger, fan_out, do_all_work
from tenant.models.models import DocumentStatus, Documents
from tenant.controllers.DocumentController import DocumentController, DocumentStatusController
import PyPDF2
import extraction.app as ex
from celery import group
import json
from flask_cognito_lib.decorators import auth_required
from utils import (
    AlchemyEncoder,
    alchemyConverter,
)

document_bp = Blueprint("document_bp", __name__, url_prefix="document")

FAILURE = -1
SUCCESS = 0
UPLOAD_FOLDER = "/opt/metadata-extraction/uploads"
document_status_controller = DocumentStatusController()
document_controller = DocumentController()

@document_bp.route("/", methods=["POST"])
# @auth_required()
def document_post():
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
        document_status = document_status_controller._create({"numPages": 0})
        response = {"documentStatusId": document_status.documentStatusId}
        resp = jsonify(response)
        resp.status_code = 202
        tasks_to_run = fan_out(file, document_status.documentStatusId)  # split up tasks
        do_all_work(tasks_to_run)  # run ocr pipeline for each task
        document_status = document_status_controller._modify({"documentStatusId": document_status.documentStatusId}, {"numPages": len(tasks_to_run)})
        return resp
    else:
        resp = jsonify({"message": "Allowed file types are pdf only"})
        resp.status_code = 400
        return resp


@document_bp.route("/<document_id>", methods=["GET"])
# @auth_required()
def document_get(document_id):
    filters = {"documentStatusId": document_id}
    documents = document_controller._get(filters)
    ds_entry = document_status_controller._get(filters)
    ds_entry = alchemyConverter(ds_entry)
    num_pages = ds_entry[0]["numPages"]
    documents = alchemyConverter(documents)
    if len(documents) == num_pages:
        res = {"status": "COMPLETE", "progress": 100, "documents": documents}
    else:
        res = {"status": "PENDING", "progress": 100*len(documents) // num_pages, "documents": []}
    res = jsonify(res)
    res.status_code = 200
    return res

