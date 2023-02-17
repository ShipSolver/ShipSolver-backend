import json
from datetime import datetime
from wsgiref import validate
from pprint import pprint
from flask import make_response, request, jsonify, Blueprint, abort
from flask_cors import cross_origin

import sys

sys.path.insert(0, "..")  # import parent folder

from controllers.controllerMapper import TicketController, TicketStatusController, UserController
from models.models import TicketEvents
from utils import (
    AlchemyEncoder,
    alchemyConverter,
    get_clean_filters_dict
)

from flask_cognito_lib.decorators import auth_required

ticket_bp = Blueprint("ticket_bp", __name__, url_prefix="ticket")

ticket_controller = TicketController()
ticket_status_controller = TicketStatusController()
user_controller = UserController()

PIECES_SEPERATOR = ",+-"



@ticket_bp.route("/status/<status>", methods=["GET"])
# @auth_required()
def ticket_get_all_with_status(status):  # create ticket

    limit = 5000 if "limit" not in request.args else request.args["limit"]
    ticket_sql_filters = get_clean_filters_dict(request.args)
    tickets = ticket_status_controller._get_tickets_with_status(status, ticket_sql_filters, limit)
    num_tickets = ticket_status_controller._get_count(ticket_sql_filters)

    res = {"tickets": alchemyConverter(tickets), "count": num_tickets}

    return make_response(json.dumps(res, cls=AlchemyEncoder))



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
# @auth_required()
def ticket_post():  # create ticket
    print("Creating ticket from the following JSON:")
    ticket_dict = json.loads(request.data)
    ticket_dict = json.loads(ticket_dict["data"])

    # remove ticketId and ticketEventId if present
    ticket_dict.pop(ticket_controller.primary_key, None)
    ticket_dict.pop(TicketEvents.non_prim_identifying_column_name, None)

    #join pieces into single string 
    ticket_dict["pieces"] =  PIECES_SEPERATOR.join(ticket_dict["pieces"])
    ticket_event = ticket_controller._create_base_event(ticket_dict)

    response = {"ticketId": ticket_event.ticketId}
    return make_response(json.dumps(response))

# TODO fix primary key issue, ticketeventID needs to be unique for edits
@ticket_bp.route("/<ticket_id>", methods=["POST"])
# @auth_required()
def ticket_edit(ticket_id):  # create ticket
    ticket_dict = json.loads(request.data)
    ticket_dict = json.loads(ticket_dict["data"])
    ticket_dict["ticketId"] = ticket_id

    
    # remove ticketId
    ticket_dict.pop("timestamp", None)
    ticket_dict.pop(ticket_controller.primary_key, None)
    
    #join pieces into single string 
    ticket_dict["pieces"] =  PIECES_SEPERATOR.join(ticket_dict["pieces"])
    ticket_event = ticket_controller._create_base_event(ticket_dict)

    response = {"ticketId": ticket_event.ticketId}
    return make_response(json.dumps(response))



@ticket_bp.route("/edits/<ticket_id>", methods=["GET"])
# @auth_required()
def ticket_get_edits(ticket_id):

    data = ticket_controller.get_ticket_edits(ticket_id)
    print(data)

    if data is None:
        abort(404)

    return make_response(json.dumps(data, cls=AlchemyEncoder))




@ticket_bp.route("/", methods=["GET"])
# @auth_required()
def ticket_get_all():

    def validate_date_format(date_text):
        try:
            return datetime.strptime(date_text, "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            raise ValueError("Incorrect data format, should be %Y-%m-%dT%H:%M:%S")


    filters = request.args or {}
    sql_filters = get_clean_filters_dict(filters)
    limit = 5000 if "limit" not in filters else filters["limit"]
    default_start = validate_date_format("1900-01-01T00:00:00")
    default_end = validate_date_format("2100-01-01T00:00:00")


    dt_start = (
        validate_date_format(filters["start"])
        if "start" in filters
        else default_start
    )
    dt_end = validate_date_format(filters["end"]) if "end" in filters else default_end

    data = ticket_controller._get_latest_event_objects_in_range(
        dt_start, dt_end, sql_filters, number_of_res=limit
    )

    res = alchemyConverter(data)
    for ticket in res:
        ticket["pieces"] = ticket["pieces"].split(PIECES_SEPERATOR)
        ticket["ticketStatus"]["currentStatus"] = ticket["ticketStatus"]["currentStatus"].value

    return make_response(json.dumps(res, cls=AlchemyEncoder))


@ticket_bp.route("/<ticket_id>", methods=["GET"])
# @auth_required()
def ticket_get(ticket_id):
    data = ticket_controller._get_latest_event_objects(
        filters={
            TicketEvents.non_prim_identifying_column_name : ticket_id
        }
    )
    res = alchemyConverter(data)

    if len(res) > 0:
        return make_response(json.dumps(res[0], cls=AlchemyEncoder))
    else:
        abort(404)
