import json
import datetime
from flask import request, Blueprint, make_response
import sys

sys.path.insert(0, "..")  # import parent folder

import controllers as Controllers
from models.models import Users
from flask_cognito_lib.decorators import auth_required
from utils import (
    AlchemyEncoder,
    alchemyConverter
)

customer_bp = Blueprint("customer_bp", __name__, url_prefix="customer")

# Dependencies
customer_controller = Controllers.user_controller


@customer_bp.route("/", methods=["POST"])
# @auth_required()
def customer_post():  # create ticket
    customer = customer_controller._create(json.loads(request.data))
    response = {"customerId": customer.customerId}
    return make_response(json.dumps(response))

@customer_bp.route("/", methods=["GET"])
# @auth_required()
def customer_get():  # create ticket
    limit = 5000 if "limit" not in request.args else request.args["limit"]
    if "limit" in request.args:
        limit = int(request.args["limit"])
    customers = customer_controller._get({}, limit=limit)
    customers = alchemyConverter(customers)
    return make_response(json.dumps(customers, cls=AlchemyEncoder))