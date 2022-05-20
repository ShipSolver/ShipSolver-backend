import json
import datetime
from flask import request, jsonify, Blueprint

import sys

sys.path.insert(0, "..")  # import parent folder

from controllers.controllerMapper import PieceController
from models.models import TicketEvents, PieceEvents
from utils import (
    AlchemyEncoder,
    require_appkey,
    alchemyConverter,
)

pieces_bp = Blueprint("pieces_bp", __name__, url_prefix="piece")


# TODO: USER BASED AUTH


pieces_controller = PieceController()


"""
Route expects requests of format:

{
    "piece_id" : "value", 
    "filters" : {
        "field1": "value1",
        "field2": "value2",
        ....
    }
}

"""


@pieces_bp.route("/{piece_id}", methods=["GET"])
@require_appkey
def pieces_get_history(piece_id):
    filters = request.args.get("filters")
    filters.extend({"piece_id": piece_id})

    pieces = pieces_controller._get_latest_event_objects(
        page=1, number_of_res=20, filters=filters
    )

    res = alchemyConverter(pieces)
    response = json.dumps(res, cls=AlchemyEncoder)

    return response
