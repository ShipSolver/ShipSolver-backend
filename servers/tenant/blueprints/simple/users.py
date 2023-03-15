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
from helpers.identity_helpers import IdentityHelper

user_bp = Blueprint("user_bp", __name__, url_prefix="user")

# Dependencies
user_controller = Controllers.user_controller

@user_bp.route("/<user_id>", methods=["GET"])
@auth_required()
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


@user_bp.route("/login", methods=["POST"])
@auth_required()
def user_login():
    user = IdentityHelper.get_logged_in_userId()

    if user_controller._get_count(filters={'userId' : user}) > 0:
        return "success"
    
    existing_users = user_controller._get(None)
    existing_users_lookup = {}
    for eu in existing_users:
        existing_users_lookup[eu.userId] = True

    cognito_users = IdentityHelper.get_cognito_users()
    sync_users = []
    for cu in cognito_users:
        if cu["userId"] in existing_users_lookup:
            continue
        sync_users.append(cu)

    inserted = user_controller._create_bulk(sync_users)
    print(f"Successfully Synchronised {len(inserted)} Users.")

    return "success"


@user_bp.route("", methods=["PUT"])
@auth_required()
def user_modify():

    userId = request.form["userId"]
    update_dict = request.form["update_dict"]
    user_controller._modify(userId, **update_dict)
    return "success"


@user_bp.route("/", methods=["DELETE"])
@auth_required()
def user_delete():
    userId = request.args.get("userId")
    filters = {}
    user_controller._delete(userId, filters)
    return "success"
