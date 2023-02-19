import json
import datetime
from flask import request, Blueprint

import sys

sys.path.insert(0, "..")  # import parent folder

import controllers as Controllers
from models.models import Users
from flask_cognito_lib.decorators import auth_required
from utils import (
    AlchemyEncoder,
    alchemyConverter
)
from flask import make_response, request, jsonify, Blueprint, abort

user_bp = Blueprint("user_bp", __name__, url_prefix="user")

# Dependencies
user_controller = Controllers.user_controller

@user_bp.route("/<user_id>", methods=["GET"])
##@auth_required()
def user_get(user_id):  # create ticket
    data = user_controller._get(
        filters={
            "userId" : user_id
        }
    )

    res = alchemyConverter(data)
    return make_response(json.dumps(res[0], cls=AlchemyEncoder))

# Frontend should not be creating users from a rest endpoint like this
@user_bp.route("/", methods=["POST"])
@auth_required()
def user_post():
    request_dict = json.loads(request.data)['data']
    request_dict.pop("withCredentials", None)
    
    user_controller._create((request_dict))

    return "success"


@user_bp.route("", methods=["PUT"])
##@auth_required()
def user_modify():

    userId = request.form["userId"]
    update_dict = request.form["update_dict"]
    user_controller._modify(userId, **update_dict)
    return "success"




@user_bp.route("/", methods=["DELETE"])
#@auth_required()
def user_delete():
    userId = request.args.get("userId")
    user_controller._delete(userId)
    return "success"
