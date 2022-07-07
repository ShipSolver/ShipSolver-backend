import json
import datetime
from flask import request, jsonify, Blueprint

import sys

sys.path.insert(0, "..")  # import parent folder

from controllers.controllerMapper import PdfController
from models.models import TicketEvents
from utils import (
    AlchemyEncoder,
    require_appkey,
    alchemyConverter,
)

shipper_bp = Blueprint("shipper_bp", __name__, url_prefix="shipper")


# TODO: USER BASED AUTH

ticket_controller = TicketController()