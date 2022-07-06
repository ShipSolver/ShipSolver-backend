import json
from datetime import datetime

from numpy import number
from flask import request, jsonify, Blueprint

import sys

sys.path.insert(0, "..")  # import parent folder

from controllers.controllerMapper import TicketController
from models.models import TicketEvents
from utils import (
    AlchemyEncoder,
    require_appkey,
    alchemyConverter,
)

ticket_bp = Blueprint("ticket_bp", __name__, url_prefix="ticket")

# TODO: USER BASED AUTH

ticket_controller = TicketController()

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

    return {"success"}


# http://127.0.0.1:6767/api/ticket/?start=2022-01-01T00:00:00&end=2022-04-04T00:00:00&shipperName=Eric%20Shea
# curl http://127.0.0.1:6767/api/ticket/?shipperName
# # curl http://127.0.0.1:6767/api/ticket?key=a
# # curl http://127.0.0.1:6767/api/ticket/?start=2022-01-01T00:00:00Z&end=2022-04-04T00:00:00Z

@ticket_bp.route("/", methods=["GET"])
# @require_appkey
def ticket_get_all():

    filters = request.args or {}
    sql_filters = dict(filters)
    
    if "start" in sql_filters: 
        del sql_filters["start"]
    if "end" in sql_filters:
        del sql_filters["end"]
    if "limit" in sql_filters:
        del sql_filters["limit"]

    if "limit" not in filters:
        limit = 5
    else:
        limit = filters["limit"]
    def validate_date_format(date_text):
        try:
            return datetime.strptime(date_text, "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            raise ValueError("Incorrect data format, should be %Y-%m-%dT%H:%M:%S")
    
    if "start" in filters:    
        dt_start_str = filters["start"]
        dt_start = validate_date_format(dt_start_str)
        if "end" in filters:
            dt_end_str= filters["end"]
            dt_end = validate_date_format(dt_end_str)
            data = ticket_controller._get_latest_event_objects_in_range(
                dt_start, dt_end, filters=sql_filters, number_of_res=limit
            )
        else:
            data = ticket_controller._get_latest_event_objects_from_start_date(
                dt_start, filters=sql_filters, number_of_res=limit
            )
    else:
        data = ticket_controller._get_latest_event_objects(sql_filters, number_of_res=limit)

    res = alchemyConverter(data)
    response = json.dumps(res, cls=AlchemyEncoder)

    return response


@ticket_bp.route("/<ticket_id>", methods=["GET"])
# @require_appkey
def ticket_get(ticket_id):
    filters = request.args.get("filters") or {}

    number_of_res = request.args.get("number_of_res")

    filters["ticketId"] = ticket_id


    latest_ticket = ticket_controller._get_latest_event_objects(
        number_of_res=number_of_res, filters=filters
    )

    res = alchemyConverter(latest_ticket[0])
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



# @ticket_bp.route("/attribute/{attribute_name}", methods=["GET"])
# @require_appkey
# def ticket_attribute_get(attribute_name):

#     filters.extend({"ticket_id": ticket_id})

#     latest_ticket = ticket_controller._get_latest_event_objects(
#         number_of_res=number_of_res, filters=filters
#     )

#     res = alchemyConverter(latest_ticket)
#     response = json.dumps(res, cls=AlchemyEncoder)

#     return response




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


@ticket_bp.route("/<ticket_id>", methods=["PUT"])
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
