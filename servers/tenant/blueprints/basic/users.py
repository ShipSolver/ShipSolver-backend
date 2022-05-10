import json
import datetime
from flask import request, Blueprint

import sys

sys.path.insert(0, "..")  # import parent folder

from controllers.baseController import BaseController
from models.models import Users
from utils import require_appkey

user_bp = Blueprint("user_bp", __name__, url_prefix="user")


# TODO: AUTH


user_controller = BaseController(Users)


@user_bp.route("/", methods=["POST"])
@require_appkey
def user_post():  # create ticket
    user_controller._create(**request.form["user"])
    return "success"


@user_bp.route("/modify", methods=["POST"])
@require_appkey
def user_modify():

    userId = request.form("userId")
    update_dict = request.form("update_dict`")

    user_controller._modify(userId, **update_dict)

    return "success"


@user_bp.route("/", methods=["GET"])
@require_appkey
def user_delete():
    userId = request.args.get("userId")
    user_controller._delete(userId)
    return "success"
