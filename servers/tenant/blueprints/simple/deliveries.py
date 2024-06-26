import json
import datetime
from flask import request, Blueprint, make_response
import sys

sys.path.insert(0, "..")  # import parent folder

import controllers as Controllers
from models.models import UserType
from flask_cognito_lib.decorators import auth_required
from utils import (
    AlchemyEncoder,
    alchemyConverter
)

delivery_bp = Blueprint("delivery_bp", __name__, url_prefix="delivery")

# Dependencies
user_controller = Controllers.user_controller


@delivery_bp.route("/", methods=["GET"])
#@auth_required()
def driver_get(): 
    
    drivers = user_controller._get({'userType': UserType.driver.value})
    drivers = alchemyConverter(drivers)
    return make_response(json.dumps(drivers, cls=AlchemyEncoder))


