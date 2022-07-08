import json
import datetime
from flask import request, Blueprint

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
    PickupMilestones,
    InventoryMilestones,
    AssignmentMilestones,
    IncompleteDeliveryMilestones,
    DeliveryMilestones,
)


class_to_cntrl_map = {
    CreationMilestones: CreationMilestonesController,
    PickupMilestones: PickupMilestonesController,
    InventoryMilestones: InventoryMilestonesController,
    AssignmentMilestones: AssignmentMilestonesController,
    IncompleteDeliveryMilestones: IncompleteDeliveryMilestonesController,
    DeliveryMilestones: DeliveryMilestonesController,
}

ticket_status_controller = TicketStatusController()
for milestoneCls in class_to_cntrl_map:

    milestone_bp = Blueprint(
        f"{milestoneCls.__tablename__}_bp",
        __name__,
        url_prefix=milestoneCls.__tablename__,
    )

    milestone_controller = class_to_cntrl_map[milestoneCls]

    @milestone_bp.route("/", methods=["POST"])
    @auth_required()
    def miltestone_post():  # create ticket
        ticketId = request.form["ticketId"]

        milestoneCls.__tablename__
        ticket_status_controller._modify(
            ticketId, {"ticket_status": request.form["new_status"]}
        )
        milestone_controller._create(**request.form["object"])

        return "success"

    @milestone_bp.route("/modify", methods=["POST"])
    @auth_required()
    def milestone_modify():

    # milestone_controller._modify(milestoneId, **update_dict)

    # return "success"

        return "success"

    @milestone_bp.route("/", methods=["DELETE"])
    @auth_required()
    def milestone_delete():
        milestoneId = request.args.get("milestoneId")
        milestone_controller._delete(milestoneId)
        return "success"
