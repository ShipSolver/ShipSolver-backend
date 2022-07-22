from flask_cognito_lib.decorators import auth_required
from flask import (
    Blueprint,
    flash,
    request,
    redirect,
    request,
    redirect,
    jsonify,
    send_file,
)
import urllib.request
import os
from werkzeug.utils import secure_filename
import sys

sys.path.insert(0, "..")  # import parent folder

from controllers.storageController import StorageController, FileTypes

blob_storage_bp = Blueprint("blob_storage_bp", __name__, url_prefix="blob_storage")
storage_controller = StorageController()

UPLOAD_FOLDER = "/uploads"
ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@blob_storage_bp.route("/", methods=["POST"])
# @auth_required()
def file_upload():

    if "upload[file]" not in request.files:
        res = jsonify({"message": "No file found in request"})
        res.status_code = 500
        return res
    file = request.files["upload[file]"]
    if file.filename == "":
        res = jsonify({"message": "No image selected for uploading"})
        res.status_code = 500
        return res
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # file.save(os.path.join(UPLOAD_FOLDER, filename))
        file.save(filename)

        s3_path = storage_controller.upload_file(local_file=filename)
        if not s3_path:
            res = jsonify({"message": "Unable to upload file to S3"})
            res.status_code = 500
            return res

        return s3_path
    else:
        res = jsonify({"message": "No file found in request"})
        res.status_code = 500
        return res


# @blob_storage_bp.route("/", methods=["GET"])
# # @auth_required()
# def generate_presigned_url():

#     if "uploaded_file_name" not in request.args:
#         res = jsonify({"message": 'Missing uploaded file name "uploaded_file_name"'})
#         res.status_code = 500
#         return res

#     uploaded_file_name = request.args.get("uploaded_file_name")
#     local_path = storage_controller.download_file(uploaded_file_name)

#     if local_path is None:
#         res = jsonify({"message": f'Uploaded file: "{uploaded_file_name}", not found.'})
#         res.status_code = 404
#         return res

#     return send_file(local_path)
