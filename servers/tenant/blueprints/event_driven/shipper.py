import json
import datetime
from flask import request, jsonify, Blueprint

import sys

sys.path.insert(0, "..")  # import parent folder

from controllers.controllerMapper import ShipperController, TicketController
from models.models import TicketEvents, ShipperEvents
from utils import (
    AlchemyEncoder,
    require_appkey,
    alchemyConverter,
)

shipper_bp = Blueprint("shipper_bp", __name__, url_prefix="shipper")


# TODO: USER BASED AUTH


shipper_controller = ShipperController()
ticket_controller = TicketController()


"""
Route expects requests of format:

{
    "shipper" : {
        "shipperEventId" : value,
        "consigneeEventId" : value, 
        "userId" : value,
        "phoneNumber" : value, 
        ...
    }

}

"""


@shipper_bp.route("/", methods=["POST"])
@require_appkey
def shipper_post():  # create ticket

    shipper_dict = request.args.get("shipper")

    # remove ticketId and ticketEventId if present
    shipper_dict.pop(shipper_controller.primary_key, None)
    shipper_dict.pop(TicketEvents.non_prim_identifying_column_name, None)

    shipper_event = shipper_controller._create_base_event(shipper_dict)

    return shipper_event


"""
Route expects requests of format:

{
    "shipper_id" : "value", 
    "filters" : {
        "field1": "value1",
        "field2": "value2",
        ....
    },
    "number_of_res" : value,
}

"""


@shipper_bp.route("/{ticket_id}", methods=["GET"])
@require_appkey
def shipper_get(shipper_id):
    filters = request.args.get("filters")
    number_of_res = request.args.get("number_of_res")

    filters.extend({"shipper_id": shipper_id})

    latest_shippers = shipper_controller._get_latest_event_objects(
        number_of_res=number_of_res, filters=filters
    )

    res = alchemyConverter(latest_shippers)
    response = json.dumps(res, cls=AlchemyEncoder)

    return response


"""
Route expects requests of format:

{
    "ticket_id" : "value", 
    "filters" : {
        "field1": "value1",
        "field2": "value2",
        ....
    }
}

"""


@shipper_bp.route("/{shipper_id}", methods=["GET"])
@require_appkey
def shpiper_get_history(shipper_id):
    filters = request.args.get("filters")
    filters.extend({"shipper_id": shipper_id})

    latest_ticket = shipper_controller._get_latest_event_objects(
        page=1, number_of_res=20, filters=filters
    )

    res = alchemyConverter(latest_ticket)
    response = json.dumps(res, cls=AlchemyEncoder)

    return response


"""
Route expects requests of format:

{
    "update_dict" : {
        "field1": "value1",
        "field2": "value2",
        ...
    }, 
    "filters" : {
        "field1": "value1",
        "field2": "value2",
        ....
    }
}

"""


@shipper_bp.route("/{shipper_id}", methods=["POST"])
@require_appkey
def shipper_update(shipper_id):

    update_dict = request.form["update_dict"]

    # remove ticketId and ticketEventId if present
    update_dict.pop(shipper_controller.primary_key, None)
    update_dict.pop(TicketEvents.non_prim_identifying_column_name, None)

    filters = request.form["filters"]
    filters.extend({"shipper_id": shipper_id})

    updated_shipper = shipper_controller._modify_latest_object(
        update_dict, filters=filters
    )

    ticket_controller._modify_latest_object(updated_shipper.shipper_id)

    res = alchemyConverter(updated_object)
    response = json.dumps(res, cls=AlchemyEncoder)

    return response
