import json
import datetime
import time
from typing import Generic
from flask import request, Blueprint, make_response, jsonify
from utils import alchemyConverter, AlchemyEncoder
from const.milestones import stateTable
import sys

sys.path.insert(0, "..")  # import parent folder

import controllers as Controllers
from flask_cognito_lib.decorators import auth_required

from models.models import (
    CreationMilestones,
    Generic_Milestone_Status,
    PickupMilestones,
    InventoryMilestones,
    AssignmentMilestones,
    IncompleteDeliveryMilestones,
    DeliveryMilestones,
)
from helpers import model_helpers
from helpers.identity_helpers import IdentityHelper

# Dependencies
milestones_controllers_list = {
    Controllers.creation_milestones_controller,
    Controllers.pickup_milestones_controller,
    Controllers.inventory_milestones_controller,
    Controllers.assignment_milestones_controller,
    Controllers.incomplete_delivery_milestones_controller,
    Controllers.delivery_milestones_controller,
}
class_to_cntrl_map = {
    CreationMilestones: Controllers.creation_milestones_controller,
    PickupMilestones: Controllers.pickup_milestones_controller,
    InventoryMilestones: Controllers.inventory_milestones_controller,
    AssignmentMilestones: Controllers.assignment_milestones_controller,
    IncompleteDeliveryMilestones: Controllers.incomplete_delivery_milestones_controller,
    DeliveryMilestones: Controllers.delivery_milestones_controller,
}
ticket_status_controller = Controllers.ticket_status_controller

old_status_exemptions = set([DeliveryMilestones, IncompleteDeliveryMilestones, CreationMilestones])
new_status_exemptions = set([DeliveryMilestones, IncompleteDeliveryMilestones, CreationMilestones])


milestone_bp = Blueprint(f"milestones_bp", __name__, url_prefix="milestones")


@milestone_bp.route("/<ticket_id>", methods=["GET"])
# @auth_required()
def get_all_milestones_for_ticket(ticket_id):  # create ticket

    filters = {
        "ticketId" : ticket_id
    }
    all_milestones = []
    for milestone_controller in milestones_controllers_list:
        data = milestone_controller._get(filters, limit=1000)
        milestones = alchemyConverter(data)
        for milestone in milestones:
            for status in "oldStatus", "newStatus":
                if status in milestone:
                    milestone[status] = str(milestone[status]).split(".")[-1]

        string_milestones = milestone_controller.convert_to_desc(milestones)
        all_milestones.extend(string_milestones)

   
    return make_response(json.dumps(all_milestones, cls=AlchemyEncoder))



@milestone_bp.route("/<milestone_type>/<ticket_id>", methods=["GET"])
# @auth_required()
def milestones_get(milestone_type, ticket_id): 
    milestone_controller = Controllers.get_controller_by_model_name(milestone_type)
    if not milestone_controller:
        return make_response(json.dumps({'error': f"milestone_type '{milestone_type}' not recognized."}), 400)
    
    filters = {
        "ticketId" : ticket_id
    }

    print(ticket_id, milestone_type)
    data = milestone_controller._get(filters, limit=1000)
    milestones = alchemyConverter(data)
    milestone_res_objects = milestone_controller.convert_to_desc(milestones)
    
    print(milestone_res_objects)
    return make_response(json.dumps(milestone_res_objects, cls=AlchemyEncoder))


@milestone_bp.route("/<milestone_type>", methods=["POST"])
# @auth_required()
def milestone_post(milestone_type):  # create ticket
    milestone_class = model_helpers.get_model_by_name(milestone_type)
    milestone_controller = Controllers.get_controller_by_model_name(milestone_type)
    if not milestone_controller:
        return make_response(json.dumps({'error': f"milestone_type '{milestone_type}' not recognized."}), 400)
    
    request_dict = json.loads(request.data)['data']
    if "ticketId" not in request_dict:
        message = 'ticketId is required'
        print(message)
        res = jsonify({'message': message})
        res.status_code = 400
        return res

    # status checking 
    if milestone_class in old_status_exemptions: 
        request_dict["oldStatus"] = str(milestone_class.oldStatus.default).split("'")[1]
    else:
        if "oldStatus" not in request_dict:
            message = 'oldStatus is required'
            print(message)
            res = jsonify({'message': message})
            res.status_code = 400
            return res
    if milestone_class in new_status_exemptions:
        request_dict["newStatus"] = str(milestone_class.oldStatus.default).split("'")[1]
    else:
        if "newStatus" not in request_dict:     
            message = 'newStatus is required'
            print(message)
            res = jsonify({'message': message})
            res.status_code = 400
            return res

    # state verification
    # paths_possible = stateTable[request_dict["oldStatus"]]
    # if request_dict["newStatus"] not in paths_possible[]

    # ticketId = request_dict["ticketId"]
    update_dict = {"currentStatus": request_dict["newStatus"]}
    if milestone_class == AssignmentMilestones and request_dict["newStatus"] == Generic_Milestone_Status.assigned.value:
        update_dict["assignedTo"] = request_dict["assignedToUserId"]
    
    elif milestone_class == InventoryMilestones:
        update_dict["assignedTo"] = None
        request_dict["approvedByUserId"] = IdentityHelper.get_logged_in_userId()
    
    elif milestone_class == DeliveryMilestones:
        '''
        Sample Data Payload: 
            "data": {
                "ticketId" : 1,
                "newStatus": "completed_delivery",
                "oldStatus": "in_transit",
                "completingUserId": "0088a8aa-0e5f-4924-a9d5-68ef3cba8cd1",
                "pictures": {
                    "POD.jpeg": picturedata,
                    "Picture1.jpeg": picturedata,
                    "Picture2.jpeg" : picturedata,
                    "Picture3.jpeg" : picturedata
                }
            } 
        '''
        
        if "POD.jpeg" not in request_dict["pictures"] or "Picture1.jpeg" not in request_dict["pictures"]:
            # print(request_dict["pictures"]["Picture1.jpeg"])
            res = jsonify({"message": "Missing files for upload"})
            res.status_code = 400
            return res

    
    ticket_status_controller._modify({"ticketId": request_dict["ticketId"]}, update_dict)
    time.sleep(4) # yes it's ugly. But it fixes async issue
    milestone_controller._create(request_dict)

    return make_response("success")
