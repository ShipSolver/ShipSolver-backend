from statistics import mode
from controllers.baseController import (
    BaseController,
    BaseTimeSeriesController,
    BaseNestedDependencyContoller,
)
import sys
from models.models import *


class UserController(BaseController):
    def __init__(self):
        super().__init__(Users)


class CustomerController(BaseController):
    def __init__(self):
        super().__init__(Customers)


class TicketStatusController(BaseController):
    def __init__(self):
        super().__init__(TicketStatus)


class MilestoneController(BaseController):
    def __init__(self, model):
        super().__init__(model=model)
        self.model = model  # redudant
        self.ticket_status = TicketStatusController()

    def _create(self, args_dict, ticket_id):

        assert isinstance(args_dict, dict)
        assert "newStatus" in args_dict

        obj = self.model(**args_dict)
        self.session.add(obj)
        self.session.commit()

        # update current ticket status
        self.ticket_status._modify(
            filters={"ticket_id": ticket_id},
            update_dict={"currentStatus": args_dict["newStatus"]},
        )

        return obj

    def __getattr__(self, attr_name):
        if attr_name != "_create":
            raise AttributeError
        return getattr(self._wrapped, attr_name)


""" MILESTONES """


class CreationMilestonesController(MilestoneController):
    def __init__(self):
        super().__init__(CreationMilestones)


class PickupMilestonesController(MilestoneController):
    def __init__(self):
        super().__init__(PickupMilestones)


class InventoryMilestonesController(MilestoneController):
    def __init__(self):
        super().__init__(InventoryMilestones)


class AssignmentMilestonesController(MilestoneController):
    def __init__(self):
        super().__init__(AssignmentMilestones)


class IncompleteDeliveryMilestonesController(MilestoneController):
    def __init__(self):
        super().__init__(IncompleteDeliveryMilestones)


class DeliveryMilestonesController(MilestoneController):
    def __init__(self):
        super().__init__(DeliveryMilestones)


""""""


class TicketController(BaseTimeSeriesController):
    def __init__(self):
        super().__init__(TicketEvents)
        self.ticket_status_controller = TicketStatusController()
        self.creation_milestone_controller = CreationMilestonesController()
        self.assigned_milestones_controller = AssignmentMilestonesController()

    def _create_base_event(self, args_dict):
        print(args_dict)

        is_pickup = args_dict["isPickup"]

        if not is_pickup:
            args_dict["newStatus"] = Creation_Milestone_Status.ticket_created.value

            fields = {
                "currentStatus": Creation_Milestone_Status.ticket_created.value,
            }
            if "assignedTo" in args_dict:
                fields["assignedTo"] = args_dict["assignedTo"]

            milestone = self.ticket_status_controller._create(fields)

        else:
            args_dict["newStatus"] = Creation_Milestone_Status.unassigned_pickup.value

            fields = {
                "currentStatus": Creation_Milestone_Status.unassigned_pickup.value,
            }
            if "assignedTo" in args_dict:
                fields["assignedTo"] = args_dict["assignedTo"]

            milestone = self.ticket_status_controller._create(fields)

        args_dict.pop("newStatus", None)
        args_dict[self.primary_key] = milestone.ticketId
        args_dict[self.model.non_prim_identifying_column_name] = milestone.ticketId

        obj = self.model(**args_dict)
        self.session.add(obj)
        self.session.commit()

        return obj
