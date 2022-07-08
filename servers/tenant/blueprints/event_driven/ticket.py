import json
from datetime import datetime
from wsgiref import validate

from numpy import number
from flask import make_response, request, jsonify, Blueprint
from flask_cors import cross_origin

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
@cross_origin(supports_credentials=True)
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


def corsify(resp):
    resp = make_response(json.dumps(resp))
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Headers"] = [
        "Origin",
        "X-Requested-With",
        "Content-Type",
        "Accept",
    ]
    return resp


def get_clean_filters_dict(immutable_args):
    sql_filters = dict(immutable_args)
    if "start" in sql_filters:
        del sql_filters["start"]
    if "end" in sql_filters:
        del sql_filters["end"]
    if "limit" in sql_filters:
        del sql_filters["limit"]
    return sql_filters


def validate_date_format(date_text):
    try:
        return datetime.strptime(date_text, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        raise ValueError("Incorrect data format, should be %Y-%m-%dT%H:%M:%S")


def default_start():
    dt_start = validate_date_format("1900-01-01T00:00:00")
    return dt_start


def default_end():
    dt_end = validate_date_format("2100-01-01T00:00:00")
    return dt_end


@ticket_bp.route("/", methods=["GET"])
@cross_origin(supports_credentials=True)
# @require_appkey
def ticket_get_all():
    filters = request.args or {}
    sql_filters = get_clean_filters_dict(filters)
    limit = 5000 if "limit" not in filters else filters["limit"]

    dt_start = (
        validate_date_format(filters["start"])
        if "start" in filters
        else default_start()
    )
    dt_end = validate_date_format(filters["end"]) if "end" in filters else default_end()

    data = ticket_controller._get_latest_event_objects_in_range(
        dt_start, dt_end, sql_filters, number_of_res=limit
    )

    res = alchemyConverter(data)

    return corsify(res)


@ticket_bp.route("/<ticket_id>", methods=["GET"])
@cross_origin(supports_credentials=True)
# @require_appkey
def ticket_get(ticket_id):
    filters = request.args.get("filters") or {}

    sql_filters = get_clean_filters_dict(filters)
    sql_filters["ticketId"] = ticket_id
    data = ticket_controller._get_latest_event_objects_in_range(
        default_start(), default_end(), filters=sql_filters
    )

    res = alchemyConverter(data[0])
    return corsify(res)


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
@cross_origin(supports_credentials=True)
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
