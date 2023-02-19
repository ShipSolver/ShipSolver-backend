import json
import datetime
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
def milestone_get(ticket_id):  # create ticket

    filters = {
        "ticketId" : ticket_id
    }
    all_milestones = []
    for milestone_controller in milestones_controllers_list:
        data = milestone_controller._get(filters, 1000)
        milestones = alchemyConverter(data)
        for milestone in milestones:
            for status in "oldStatus", "newStatus":
                if status in milestone:
                    milestone[status] = str(milestone[status]).split(".")[-1]

        string_milestones = milestone_controller.convert_to_desc(milestones)
        all_milestones.extend(string_milestones)

   
    return make_response(json.dumps(all_milestones, cls=AlchemyEncoder))


@milestone_bp.route("/<milestone_type>", methods=["POST"])
# @auth_required()
def milestone_post(milestone_type):  # create ticket
    milestone_class = getattr(sys.modules[__name__], milestone_type)
    milestone_controller = class_to_cntrl_map[milestone_class]
    
    request_dict = json.loads(request.data)
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
    
    if milestone_class == PickupMilestones:
         if request_dict["newStatus"] == Generic_Milestone_Status.requested_pickup.value:
            update_dict["requesterUserId"] = request_dict["assignedToassignedToUserId"]
         if request_dict["newStatus"] == Generic_Milestone_Status.declined_pickup.value:
            update_dict["requesterUserId"] = None

    if milestone_class == IncompleteDeliveryMilestones or milestone_class == DeliveryMilestones:
        update_dict["requesterUserId"] = None
    
    ticket_status_controller._modify({"ticketId": request_dict["ticketId"]}, update_dict)    
    milestone_controller._create(request_dict)

    return make_response("success")
