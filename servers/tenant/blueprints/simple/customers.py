import json
import datetime
from flask import request, Blueprint
import sys

sys.path.insert(0, "..")  # import parent folder

from controllers.controllerMapper import CustomerController
from models.models import Users
from flask_cognito_lib.decorators import auth_required

customer_bp = Blueprint("customer_bp", __name__, url_prefix="customer")


customer_controller = CustomerController()


@customer_bp.route("/", methods=["POST"])
@auth_required()
def customer_post():  # create ticket
    customer_controller._create(**request.form["customer"])
    return "success"


@customer_bp.route("/modify", methods=["POST"])
@auth_required()
def customer_modify():

    customerId = request.form["customerId"]
    update_dict = request.form["update_dict"]

    customer_controller._modify(customerId, **update_dict)

    return "success"


@customer_bp.route("/", methods=["DELETE"])
@auth_required()
def customer_delete():
    customerId = request.args.get("customerId")
    customer_controller._delete(customerId)
    return "success"
