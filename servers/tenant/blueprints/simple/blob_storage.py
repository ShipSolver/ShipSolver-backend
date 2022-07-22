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
@auth_required()
def file_upload():
    if "file" not in request.files:
        flash("No file part")
        return redirect(request.url)
    file = request.files["file"]
    if file.filename == "":
        flash("No image selected for uploading")
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))

        if not storage_controller.upload_file(file_name=filename):
            res = jsonify({"message": "Unable to upload file to S3"})
            res.status_code = 500
            return res

        return "success"

    else:
        flash(f"Allowed image types are - {[a for a in ALLOWED_EXTENSIONS]}")
        return redirect(request.url)


@blob_storage_bp.route("/{uploaded_file_name}", methods=["GET"])
@auth_required()
def file_download(uploaded_file_name):
    local_path = storage_controller.download_file(uploaded_file_name)

    if local_path is None:
        res = jsonify({"message": f'Uploaded file: "{uploaded_file_name}", not found.'})
        res.status_code = 404
        return res

    return send_file(local_path)
