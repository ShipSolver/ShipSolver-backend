import json
from datetime import datetime
from wsgiref import validate
from pprint import pprint
from flask import make_response, request, jsonify, session, Blueprint, abort
from flask_cors import cross_origin
from helpers.identity_helpers import IdentityHelper
import controllers as Controllers
import boto3
from botocore.client import Config
import os
import sys

sys.path.insert(0, "..")  # import parent folder

from models.models import TicketEvents, UserType
from utils import (
    AlchemyEncoder,
    alchemyConverter,
    get_clean_filters_dict
)

from flask_cognito_lib.decorators import auth_required

ticket_bp = Blueprint("ticket_bp", __name__, url_prefix="ticket")

# Dependencies
ticket_controller = Controllers.ticket_controller
ticket_status_controller = Controllers.ticket_status_controller
user_controller = Controllers.user_controller

PIECES_SEPERATOR = ",+-"
TENANT = "test-tenant2"
BUCKET = f"{TENANT}-bucket"
aws_access_key_id = os.getenv("aws_access_key_id")
aws_secret_access_key = os.getenv("aws_secret_access_key")
s3 = boto3.resource('s3', region_name='us-east-2', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, config=Config(signature_version='s3v4'))
bucket = s3.Bucket(BUCKET)
s3_client = boto3.client('s3', region_name='us-east-2', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, config=Config(signature_version='s3v4'))

@ticket_bp.route("/status/<status>", methods=["GET"])
@auth_required()
def ticket_get_all_with_status(status):  # create ticket
    user = IdentityHelper.get_logged_in_userId()
    ticket_sql_filters = get_clean_filters_dict(request.args)

    # Build & Modify Filters Arguments
    # Check if we are on driver app. If so, we need to filter for tickets assigned to driver.
    if user_controller.get_user_type(user) == UserType.driver.value:
        ticket_sql_filters["ticketStatusAssignedTo"] = user

    limit = 5000 if "limit" not in ticket_sql_filters else ticket_sql_filters["limit"]
    
    # Make call to get tickets
    tickets = ticket_status_controller._get_tickets_with_status(status, ticket_sql_filters, limit)

    res = {"tickets": alchemyConverter(tickets), "count": len(tickets)}

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
@auth_required()
def ticket_post():  # create ticket
    print("Creating ticket from the following JSON:")
    ticket_dict = json.loads(request.data)
    ticket_dict = json.loads(ticket_dict["data"])
    # remove ticketId and ticketEventId if present
    ticket_dict.pop(ticket_controller.primary_key, None)
    ticket_dict.pop(TicketEvents.non_prim_identifying_column_name, None)

    #join pieces into single string 
    ticket_dict["pieces"] =  PIECES_SEPERATOR.join(ticket_dict["pieces"])
    if not ticket_dict["isPickup"]:
        ticket_dict["isPickup"] = False
    if "noSignatureRequired" not in ticket_dict:
        ticket_dict["noSignatureRequired"] = False
    if "tailgateAuthorized" not in ticket_dict:
        ticket_dict["tailgateAuthorized"] = False
    ticket_dict["userId"] = IdentityHelper.get_logged_in_userId()
    ticket_event = ticket_controller._create_base_event(ticket_dict)

    response = {"ticketId": ticket_event.ticketId}
    return make_response(json.dumps(response))

# TODO fix primary key issue, ticketeventID needs to be unique for edits
@ticket_bp.route("/<ticket_id>", methods=["POST"])
@auth_required()
def ticket_edit(ticket_id):  # create ticket
    ticket_dict = json.loads(request.data)
    ticket_dict = json.loads(ticket_dict["data"])
    ticket_dict["ticketId"] = ticket_id
    ticket_dict["userId"] = IdentityHelper.get_logged_in_userId()
    
    # remove ticketId
    ticket_dict.pop("timestamp", None)
    ticket_dict.pop(ticket_controller.primary_key, None)
    
    #join pieces into single string 
    ticket_dict["pieces"] =  PIECES_SEPERATOR.join(ticket_dict["pieces"])
    ticket_event = ticket_controller._create_base_event(ticket_dict)

    response = {"ticketId": ticket_event.ticketId}
    return make_response(json.dumps(response))


@ticket_bp.route("/edits/<ticket_id>", methods=["GET"])
@auth_required()
def ticket_get_edits(ticket_id):

    data = ticket_controller._get_ticket_edits(ticket_id)

    if data is None:
        abort(404)

    return make_response(json.dumps(data, cls=AlchemyEncoder))

@ticket_bp.route("/<ticket_id>", methods=["DELETE"])
@auth_required()
def ticket_delete(ticket_id):
    delete_performed = ticket_controller._delete_base_ticket(ticket_id, IdentityHelper.get_logged_in_userId())
    if not delete_performed:
        abort(403)

    return "Valid delete occured"


@ticket_bp.route("/", methods=["GET"])
@auth_required()
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

    data = ticket_controller._get_latest_base_object_in_range(
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
    data = ticket_controller._get_event_objects_by_latest(
        filters={
            TicketEvents.non_prim_identifying_column_name : ticket_id
        }
    )
    res = alchemyConverter(data)
    if len(res) > 0:
        view_url = ""
        if res[0]["orderS3Link"] != "":
             s3Path = '/'.join(res[0]["orderS3Link"].split("/")[3:]) 
             view_url = s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': BUCKET, 'Key': s3Path},
                ExpiresIn=3600
            )
        res[0]["orderS3Link"] = view_url
        return make_response(json.dumps(res[0], cls=AlchemyEncoder))
    else:
        abort(404)
