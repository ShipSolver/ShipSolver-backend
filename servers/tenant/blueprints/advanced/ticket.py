import json
import datetime
from flask import request, jsonify, Blueprint

import sys

sys.path.insert(0, "..")  # import parent folder

from controllers.baseController import BaseTimeSeriesController
from models.models import TicketEvents
from utils import require_appkey, alchemyConverter, AlchemyEncoder

ticket_bp = Blueprint("ticket_bp", __name__, url_prefix="ticket")


# TODO: AUTH


ticket_controller = BaseTimeSeriesController(TicketEvents)


@ticket_bp.route("", methods=["POST"])
@require_appkey
def ticket_post():  # create ticket

    ticket_dict = request.args.get("ticket")
    ticket_controller._create_base_event(ticket_dict)

    return "success"


@ticket_bp.route("/", methods=["GET"])
@require_appkey
def ticket_get_range():
    def validate_date_format(date_text):
        try:
            datetime.datetime.strptime(date_text, "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYY-MM-DD")

    dt = request.args.get("datetime")
    validate_date_format(dt)

    data = ticket_controller._get_latest_objects_in_range(dt)

    res = alchemyConverter(data)
    response = json.dumps(res, cls=AlchemyEncoder)

    return response


# @ticket_bp.route("{ticket_id}", methods=["GET"])
# @require_appkey
# def ticket_get():
