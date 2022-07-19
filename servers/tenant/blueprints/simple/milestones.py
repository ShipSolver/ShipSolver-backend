import json
import datetime
from flask import request, Blueprint, make_response, jsonify
from utils import alchemyConverter, AlchemyEncoder
from const.milestones import stateTable
import sys

sys.path.insert(0, "..")  # import parent folder

from controllers.controllerMapper import (
    CreationMilestonesController,
    PickupMilestonesController,
    InventoryMilestonesController,
    AssignmentMilestonesController,
    IncompleteDeliveryMilestonesController,
    DeliveryMilestonesController,
    TicketStatusController,
)
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

class_to_cntrl_map = {
    CreationMilestones: CreationMilestonesController(),
    PickupMilestones: PickupMilestonesController(),
    InventoryMilestones: InventoryMilestonesController(),
    AssignmentMilestones: AssignmentMilestonesController(),
    IncompleteDeliveryMilestones: IncompleteDeliveryMilestonesController(),
    DeliveryMilestones: DeliveryMilestonesController(),
}

old_status_exemptions = set([DeliveryMilestones, IncompleteDeliveryMilestones, CreationMilestones])
new_status_exemptions = set([DeliveryMilestones, IncompleteDeliveryMilestones, CreationMilestones])

ticket_status_controller = TicketStatusController()

milestone_bp = Blueprint(f"milestones_bp", __name__, url_prefix="milestones")


@milestone_bp.route("/<ticket_id>", methods=["GET"])
# @auth_required()
def miltestone_get(ticket_id):  # create ticket

    filters = {
        "ticketId" : ticket_id
    }
    all_milestones = []
    for cls, milestone_controller in class_to_cntrl_map.items():
        data = milestone_controller._get(filters, 1000)
        milestones = alchemyConverter(data)
        all_milestones.extend(milestones)

    for milestone in all_milestones:
        for status in "oldStatus", "newStatus":
            if status in milestone:
                milestone[status] = str(milestone[status]).split(".")[-1]

    return make_response(json.dumps(all_milestones, cls=AlchemyEncoder))




@milestone_bp.route("/<milestone_type>", methods=["POST"])
# @auth_required()
def milestone_post(milestone_type):  # create ticket
    milestone_class = getattr(sys.modules[__name__], milestone_type)
    milestone_controller = class_to_cntrl_map[milestone_class]
    request_dict = dict(request.form)
    if "ticketId" not in request.form:
        message = 'ticketId is required'
        print(message)
        res = jsonify({'message': message})
        res.status_code = 400
        return res

    # status checking 
    if milestone_class in old_status_exemptions: 
        request_dict["oldStatus"] = str(milestone_class.oldStatus.default).split("'")[1]
    else:
        if "oldStatus" not in request.form:
            message = 'oldStatus is required'
            print(message)
            res = jsonify({'message': message})
            res.status_code = 400
            return res
    if milestone_class not in new_status_exemptions:
        request_dict["newStatus"] = str(milestone_class.oldStatus.default).split("'")[1]
    else:
        if "newStatus" not in request.form:
            message = 'newStatus is required'
            print(message)
            res = jsonify({'message': message})
            res.status_code = 400
            return res

    # state verification
    # paths_possible = stateTable[request_dict["oldStatus"]]
    # if request_dict["newStatus"] not in paths_possible[]

    ticketId = request_dict["ticketId"]
    update_dict = {"ticket_status": request_dict["newStatus"]}

    if milestone_class == AssignmentMilestones and request_dict["newStatus"] == Generic_Milestone_Status.assigned:
        update_dict["assignedToUserId"] = request_dict["assignedToassignedToUserId"]
    
    if milestone_class == PickupMilestones:
         if request_dict["newStatus"] == Generic_Milestone_Status.requested_pickup:
            update_dict["requesterUserId"] = request_dict["assignedToassignedToUserId"]
         if request_dict["newStatus"] == Generic_Milestone_Status.declined_pickup:
            update_dict["requesterUserId"] = None

    if milestone_class == IncompleteDeliveryMilestones or milestone_class == DeliveryMilestones:
        update_dict["requesterUserId"] = None
    
    ticket_status_controller._modify(ticketId, update_dict)    
    milestone_controller._create(**request.form["object"])

    return "success"
