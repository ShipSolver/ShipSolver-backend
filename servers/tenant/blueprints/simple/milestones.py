import json
import datetime
from flask import request, Blueprint

import sys

sys.path.insert(0, "..")  # import parent folder

from controllers.controllerMapper import (
    GenericMilestoneController,
    InventoryMilestoneController,
    DeliveryMilestoneController,
)
from models.models import GenericMilestones, InventoryMilestones, DeliveryMilestones
from flask_cognito_lib.decorators import auth_required


class_to_cntrl_map = {
    GenericMilestones: GenericMilestoneController,
    InventoryMilestones: InventoryMilestoneController,
    DeliveryMilestones: DeliveryMilestoneController,
}

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
        milestone_controller._create(**request.form["object"])

        return "success"

    @milestone_bp.route("/modify", methods=["POST"])
    @auth_required()
    def milestone_modify():

        milestoneId = request.form["milestoneId"]
        update_dict = request.form["update_dict"]

        milestone_controller._modify(milestoneId, **update_dict)

        return "success"

    @milestone_bp.route("/", methods=["DELETE"])
    @auth_required()
    def milestone_delete():
        milestoneId = request.args.get("milestoneId")
        milestone_controller._delete(milestoneId)
        return "success"
