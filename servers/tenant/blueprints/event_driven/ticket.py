import json
import datetime

from numpy import number
from flask import request, jsonify, Blueprint

import sys

sys.path.insert(0, "..")  # import parent folder

from controllers.controllerMapper import PieceController, TicketController
from models.models import TicketEvents, PieceEvents
from utils import (
    AlchemyEncoder,
    require_appkey,
    alchemyConverter,
)

ticket_bp = Blueprint("ticket_bp", __name__, url_prefix="ticket")

# TODO: USER BASED AUTH

ticket_controller = TicketController()
pieces_controller = PieceController()

"""
Route expects requests of format:

{
    "ticket" : {
        "shipperEventId" : value,
        "consigneeEventId" : value, 
        "userId" : value,
        "customerId" : value, 
        ... 

        "pieces": [
            {
                "userId" : value,  
                "pieceDescription" : value
                ...
            }
            {
                "userId" : value,  
                "pieceDescription" : value
                ...
            }
            ...
        }
 
    } # do not provide ticketId, ticketEventId

}

"""


@ticket_bp.route("/", methods=["POST"])
@require_appkey
def ticket_post():  # create ticket

    ticket_dict = request.args.get("ticket")

    # remove ticketId and ticketEventId if present
    ticket_dict.pop(ticket_controller.primary_key, None)
    ticket_dict.pop(TicketEvents.non_prim_identifying_column_name, None)

    ticket_event = ticket_controller._create_base_event(ticket_dict)

    pieces_args_array = ticket_dict["pieces"]

    for pieces_args in pieces_args_array:
        pieces_args["ticketEventId"] = ticket_event.ticketEventId
        pieces_controller._create_base_event(pieces_args)

    return "success"


@ticket_bp.route("/", methods=["GET"])
# @require_appkey
def ticket_get_all():

    filters = request.args.get("filters") or {}
    limit = request.args.get("limit") or 1

    data = ticket_controller._get_latest_event_objects(filters, number_of_res=limit)
    print("data------------------")
    print(data)
    res = alchemyConverter(data)
    response = json.dumps(res, cls=AlchemyEncoder)

    return response

"""
Route expects requests of format:

{
    "datetime" : "value", 
    "filters" : {
        "field1": "value1",
        "field2": "value2",
        ....
    }
}

"""


@ticket_bp.route("/date-range", methods=["GET"])
@require_appkey
def ticket_get_range():
    def validate_date_format(date_text):
        try:
            datetime.datetime.strptime(date_text, "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYY-MM-DD")

    dt = request.args.get("datetime")
    validate_date_format(dt)

    filters = request.args.get("filters")

    data = ticket_controller._get_latest_event_objects_from_start_date(
        dt, filters=filters
    )

    res = alchemyConverter(data)
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
    },
    "number_of_res" : value,

}

"""

@ticket_bp.route("/attribute/{attribute_name}", methods=["GET"])
@require_appkey
def ticket_attribute_get(attribute_name):

    filters.extend({"ticket_id": ticket_id})

    latest_ticket = ticket_controller._get_latest_event_objects(
        number_of_res=number_of_res, filters=filters
    )

    res = alchemyConverter(latest_ticket)
    response = json.dumps(res, cls=AlchemyEncoder)

    return response


@ticket_bp.route("/id/{ticket_id}", methods=["GET"])
@require_appkey
def ticket_get(ticket_id):
    filters = request.args.get("filters")
    number_of_res = request.args.get("number_of_res")

    filters.extend({"ticket_id": ticket_id})

    latest_ticket = ticket_controller._get_latest_event_objects(
        number_of_res=number_of_res, filters=filters
    )

    res = alchemyConverter(latest_ticket)
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


@ticket_bp.route("/id/{ticket_id}", methods=["GET"])
@require_appkey
def ticket_get_history(ticket_id):
    filters = request.args.get("filters")
    filters.extend({"ticket_id": ticket_id})

    latest_ticket = ticket_controller._get_latest_event_objects(
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


@ticket_bp.route("/id/{ticket_id}", methods=["PUT"])
@require_appkey
def ticket_update(ticket_id):

    update_dict = request.form["update_dict"]

    # remove ticketId and ticketEventId if present
    update_dict.pop(ticket_controller.primary_key, None)
    update_dict.pop(TicketEvents.non_prim_identifying_column_name, None)

    filters = request.form["filters"]
    filters.extend({"ticket_id": ticket_id})

    updated_object = ticket_controller._modify_latest_object(
        update_dict, filters=filters
    )

    res = alchemyConverter(updated_object)
    response = json.dumps(res, cls=AlchemyEncoder)

    return response
