import json
<<<<<<< HEAD
<<<<<<< HEAD
from datetime import datetime
from wsgiref import validate
<<<<<<< HEAD

from numpy import number
from flask import make_response, request, jsonify, Blueprint
=======
import datetime
=======
from datetime import datetime
>>>>>>> get endpoints
=======
>>>>>>> Fixing default date bug

from numpy import number
from flask import request, jsonify, Blueprint
>>>>>>> modifying db schema

import sys

sys.path.insert(0, "..")  # import parent folder

<<<<<<< HEAD
from controllers.controllerMapper import TicketController, TicketStatusController
=======
from controllers.controllerMapper import TicketController
>>>>>>> fix schema
from models.models import TicketEvents
from utils import (
    AlchemyEncoder,
    alchemyConverter,
)

from logger import logger
from flask_cognito_lib.decorators import auth_required

ticket_bp = Blueprint("ticket_bp", __name__, url_prefix="ticket")

ticket_controller = TicketController()
<<<<<<< HEAD
ticket_status_controller = TicketStatusController()
PIECES_SEPERATOR = ",+-"
=======

>>>>>>> fix schema
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


@ticket_bp.route("/status/<status>", methods=["GET"])
@auth_required()
def ticket_get_all_with_status(status):  # create ticket

    limit = 5000 if "limit" not in request.args else request.args["limit"]
    ticket_sql_filters = get_clean_filters_dict(request.args)
    
    tickets = ticket_status_controller._get_tickets_with_status(status, ticket_sql_filters, limit)
    num_tickets = ticket_status_controller._get_count(ticket_sql_filters)

    res = {"tickets": alchemyConverter(tickets), "count": num_tickets}

    logger.info(res)

    return make_response(json.dumps(res, cls=AlchemyEncoder))


@ticket_bp.route("/", methods=["POST"])
@auth_required()
def ticket_post():  # create ticket
    print("Creating ticket from the following JSON:")
    print(request.data)
    ticket_dict = json.loads(request.data)
    ticket_dict = ticket_dict["data"]

    # remove ticketId and ticketEventId if present
    ticket_dict.pop(ticket_controller.primary_key, None)
    ticket_dict.pop(TicketEvents.non_prim_identifying_column_name, None)
    #join pieces into single string 
    ticket_dict["pieces"] =  PIECES_SEPERATOR.join(ticket_dict["pieces"])
    ticket_event = ticket_controller._create_base_event(ticket_dict)

<<<<<<< HEAD
<<<<<<< HEAD
    response = {"ticketId": ticket_event.ticketId}
    return make_response(json.dumps(response))

# TODO fix primary key issue, ticketeventID needs to be unique for edits
@ticket_bp.route("/<ticket_id>", methods=["POST"])
@auth_required()
def ticket_edit(ticket_id):  # create ticket
    print("Creating ticket from the following JSON:")
    print(request.data)
    ticket_dict = json.loads(request.data)
    ticket_dict = ticket_dict["data"]
    ticket_dict["ticketId"] = ticket_id
    # remove ticketId and ticketEventId if present
    ticket_dict.pop(ticket_controller.primary_key, None)
    #join pieces into single string 
    ticket_dict["pieces"] =  PIECES_SEPERATOR.join(ticket_dict["pieces"])
    ticket_event = ticket_controller._create_base_event(ticket_dict)
=======
    return {"success"}


# http://127.0.0.1:6767/api/ticket/?start=2022-01-01T00:00:00&end=2022-04-04T00:00:00&shipperName=Eric%20Shea
# curl http://127.0.0.1:6767/api/ticket/?shipperName
# # curl http://127.0.0.1:6767/api/ticket?key=a
# # curl http://127.0.0.1:6767/api/ticket/?start=2022-01-01T00:00:00Z&end=2022-04-04T00:00:00Z
>>>>>>> get endpoints

    response = {"ticketId": ticket_event.ticketId}
    return make_response(json.dumps(response))

# http://127.0.0.1:6767/api/ticket/?start=2022-01-01T00:00:00&end=2022-04-04T00:00:00&shipperName=Eric%20Shea
# curl http://127.0.0.1:6767/api/ticket/?shipperName
# # curl http://127.0.0.1:6767/api/ticket?key=a
# # curl http://127.0.0.1:6767/api/ticket/?start=2022-01-01T00:00:00Z&end=2022-04-04T00:00:00Z

<<<<<<< HEAD
def get_clean_filters_dict(immutable_args):
    sql_filters = dict(immutable_args)
    if "start" in sql_filters:
        del sql_filters["start"]
    if "end" in sql_filters:
        del sql_filters["end"]
    if "limit" in sql_filters:
        del sql_filters["limit"]
    return sql_filters
=======
@ticket_bp.route("/", methods=["GET"])
# @require_appkey
def ticket_get_all():

<<<<<<< HEAD
    filters = request.args.get("filters") or {}
    limit = request.args.get("limit") or 2

    data = ticket_controller._get_latest_event_objects(filters, number_of_res=limit)
    res = alchemyConverter(data)
    response = json.dumps(res, cls=AlchemyEncoder)
>>>>>>> modifying db schema


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
@auth_required()
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
=======
    filters = request.args or {}
    sql_filters = dict(filters)
    
=======

def get_clean_filters_dict(immutable_args):
    sql_filters = dict(immutable_args)
>>>>>>> ALL tickets API done
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
# @require_appkey
def ticket_get_all():
    filters = request.args or {}
    sql_filters = get_clean_filters_dict(filters)
<<<<<<< HEAD
    if "limit" not in filters:
        limit = 5
    else:
        limit = filters["limit"]
    
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
<<<<<<< HEAD
>>>>>>> get endpoints

    res = alchemyConverter(data)
    for ticket in res:
        ticket["pieces"] = ticket["pieces"].split(PIECES_SEPERATOR)
        ticket["ticketStatus"]["currentStatus"] = ticket["ticketStatus"]["currentStatus"].value

    return make_response(json.dumps(res, cls=AlchemyEncoder))
=======
=======
    limit = 5 if "limit" not in filters else filters["limit"]

    dt_start = validate_date_format(filters["start"]) if "start" in filters else default_start()
    dt_end = validate_date_format(filters["end"]) if "end" in filters else default_end()

    data = ticket_controller._get_latest_event_objects_in_range(dt_start, dt_end, sql_filters, number_of_res=limit)
>>>>>>> Fixing default date bug
    
    res = alchemyConverter(data)
    
    print("\n\n\n\nRES POST AC ----------------------")
    print(res)
    response = json.dumps(res)

    print("\n\n\n\nRESULT RESPONSE ------------------" )
    print(response)
>>>>>>> ALL tickets API done


<<<<<<< HEAD
def get_single(ticket_id):
    filters = request.args.get("filters") or {}

    sql_filters = get_clean_filters_dict(filters)
    sql_filters["ticketId"] = ticket_id
    data = ticket_controller._get_latest_event_objects_in_range(
        default_start(), default_end(), filters=sql_filters
    )

    logger.info("DATA", str(data))

    return data[0] if isinstance(data, list) else data

@ticket_bp.route("/<ticket_id>", methods=["GET"])
@auth_required()
def ticket_get(ticket_id):
    data = get_single(ticket_id)
    res = alchemyConverter(data)
    return make_response(json.dumps(res, cls=AlchemyEncoder))
=======
@ticket_bp.route("/<ticket_id>", methods=["GET"])
# @require_appkey
def ticket_get(ticket_id):
    filters = request.args.get("filters") or {}
    
    
    sql_filters = get_clean_filters_dict(filters)
    sql_filters["ticketId"] = ticket_id
    data = ticket_controller._get_latest_event_objects_in_range(
        default_start(), default_end(), filters=sql_filters
    )

    res = alchemyConverter(data[0])
    response = json.dumps(res)

    return response
>>>>>>> get endpoints

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

<<<<<<< HEAD
=======


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




>>>>>>> get endpoints
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

<<<<<<< HEAD
=======

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
>>>>>>> get endpoints
