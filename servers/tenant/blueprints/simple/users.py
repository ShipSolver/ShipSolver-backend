import json
import datetime
from flask import request, Blueprint

import sys

sys.path.insert(0, "..")  # import parent folder

from controllers.controllerMapper import UserController
from models.models import Users
from utils import require_appkey

user_bp = Blueprint("user_bp", __name__, url_prefix="user")


# TODO: AUTH


user_controller = UserController()


@user_bp.route("/", methods=["GET"])
@require_appkey
def user_get():  # create ticket
    user_controller._get(**request.form["user"])
    return "success"


@user_bp.route("/", methods=["POST"])
# @require_appkey
def user_post():  # create ticket

    (request.get_json(force=True)['user'])
    user_controller._create((request.get_json(force=True)['user']))
    return "success"


@user_bp.route("/modify", methods=["POST"])
@require_appkey
def user_modify():

    userId = request.form["userId"]
    update_dict = request.form["update_dict"]

    user_controller._modify(userId, **update_dict)

    return "success"


@user_bp.route("/", methods=["DELETE"])
@require_appkey
def user_delete():
    userId = request.args.get("userId")
    user_controller._delete(userId)
    return "success"
