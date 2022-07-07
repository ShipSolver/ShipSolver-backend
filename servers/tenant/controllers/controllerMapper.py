from statistics import mode

from regex import D
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


<<<<<<< HEAD
class TicketStatusController(BaseController):
    def __init__(self):
        super().__init__(TicketStatus)
        self.ticket_controller = BaseTimeSeriesController(TicketEvents)


    def _get_tickets_with_status(self, status, filters: dict, limit):
        tickets = [] 

        ticketIds = (
            self.session.query(TicketStatus.ticketId)
            .filter(TicketStatus.currentStatus == status)
            .all()
        )

        print(filters, ticketIds)
        for i, tid_tup in enumerate(ticketIds):
            
            filters_cpy = filters.copy()
            filters_cpy["ticketId"] = tid_tup[0]
            print(filters_cpy)

            ticket = self.ticket_controller._get_latest_event_objects(filters=filters_cpy)
            tickets.append(ticket[0])
            
            if i == limit:
                break


        return tickets


class MilestoneController(BaseController):
    def __init__(self, model):
        super().__init__(model=model)
        self.model = model  # redudant
        self.ticket_status = TicketStatusController()


""" MILESTONES """


class CreationMilestonesController(MilestoneController):
    def __init__(self):
        super().__init__(CreationMilestones)
    
    def convert_to_desc(self, milestones):
        string_milestones = []
        for milestone in milestones:
                string_milestones.append({
                    "description":  f"Ticket created by {milestone['createdByUser']['username']}",
                    "timestamp": milestone["createdAt"]
                })
        return string_milestones
         

class PickupMilestonesController(MilestoneController):
    def __init__(self):
        super().__init__(PickupMilestones)

    def convert_to_desc(self, milestones):
        string_milestones = []
        for milestone in milestones:
            if milestone["oldStatus"] == Pickup_Milestone_Status.unassigned_pickup.value and  milestone["newStatus"] == Pickup_Milestone_Status.requested_pickup.value:
                string_milestones.append({
                    "description":  f"Pickup request sent to {milestone['requestedUser']['username']} by {milestone['requesterUser']['username']}",
                    "timestamp": milestone["timestamp"]
                })
            if milestone["oldStatus"] == Pickup_Milestone_Status.requested_pickup.value and  milestone["newStatus"] == Pickup_Milestone_Status.accepted_pickup.value:
                string_milestones.append({
                    "description":  f"Pickup request accepted by {milestone['requestedUser']['username']}",
                    "timestamp": milestone["timestamp"]
                })
            if milestone["oldStatus"] == Pickup_Milestone_Status.requested_pickup.value and milestone["newStatus"] == Pickup_Milestone_Status.declined_pickup.value:
                string_milestones.append({
                    "description":  f"Pickup request declined by {milestone['requestedUser']['username']}",
                    "timestamp": milestone["timestamp"]
                })
            if milestone["oldStatus"] == Pickup_Milestone_Status.accepted_pickup.value and  milestone["newStatus"] == Pickup_Milestone_Status.completed_pickup.value:
                string_milestones.append({
                    "description":  f"Pickup completed by {milestone['requestedUser']['username']}",
                    "timestamp": milestone["timestamp"]
                })
            if milestone["oldStatus"] == Pickup_Milestone_Status.unassigned_pickup.value and  milestone["newStatus"] == Pickup_Milestone_Status.incomplete_pickup.value:
                string_milestones.append({
                    "description":  f"Pickup not completed by {milestone['requestedUser']['username']}",
                    "timestamp": milestone["timestamp"]
                })
        return string_milestones

class InventoryMilestonesController(MilestoneController):
    def __init__(self):
        super().__init__(InventoryMilestones)
=======
class TicketController(BaseTimeSeriesController):
    def __init__(self):
        super().__init__(TicketEvents)


>>>>>>> modifying db schema

    def convert_to_desc(self, milestones):
        string_milestones = []
        for milestone in milestones:
                if milestone["oldStatus"] == Inventory_Milestone_Status.ticket_created.value and  milestone["newStatus"] == Inventory_Milestone_Status.checked_into_inventory.value:
                    string_milestones.append({
                        "description":  f"Item checked into inventory by {milestone['approvedByUser']['username']}",
                        "timestamp": milestone["timestamp"]
                    })
                if milestone["oldStatus"] == Inventory_Milestone_Status.incomplete_delivery.value and  milestone["newStatus"] == Inventory_Milestone_Status.checked_into_inventory.value:
                    string_milestones.append({
                        "description":  f"Item checked back into inventory by {milestone['approvedByUser']['username']}",
                        "timestamp": milestone["timestamp"]
                    })
                if milestone["oldStatus"] == Inventory_Milestone_Status.completed_delivery.value and  milestone["newStatus"] == Inventory_Milestone_Status.incomplete_delivery.value:
                    string_milestones.append({
                        "description":  f"POD rejected by {milestone['approvedByUser']['username']}",
                        "timestamp": milestone["timestamp"]
                    })
                # if milestone["oldStatus"] == Inventory_Milestone_Status.completed_delivery.value and milestone["newStatus"] == Inventory_Milestone_Status.approved_pod.value:
                #     string_milestones.append({
                #         "description":  f"POD rejected by {milestone['approvedByUser']['username']}",
                #         "timestamp": milestone["timestamp"]
                #     })
                # TODO fix schema and add remaining inventory milestones
        return string_milestones

class AssignmentMilestonesController(MilestoneController):
    def __init__(self):
        super().__init__(AssignmentMilestones)
        
    def convert_to_desc(self, milestones):
        string_milestones = []
        for milestone in milestones:
                if milestone["oldStatus"] == Assignment_Milestone_Status.checked_into_inventory.value and  milestone["newStatus"] == Assignment_Milestone_Status.assigned.value:
                    string_milestones.append({
                        "description":  f"Delivery assigned to {milestone['requestedUser']['username']} by {milestone['requesterUser']['username']}",
                        "timestamp": milestone["timestamp"]
                    })
                else:
                    string_milestones.append({
                        "description":  f"Delivery is now heading toward its destination with {milestone['requestedUser']['username']}",
                        "timestamp": milestone["timestamp"]
                    })
        return string_milestones

class IncompleteDeliveryMilestonesController(MilestoneController):
    def __init__(self):
        super().__init__(IncompleteDeliveryMilestones)

    def convert_to_desc(self, milestones):
        string_milestones = []
        for milestone in milestones:
                string_milestones.append({
                    "description":  f"Delivery not completed by {milestone['assigneeUser']['username']}",
                    "timestamp": milestone["timestamp"]
                })
        return string_milestones
         
class DeliveryMilestonesController(MilestoneController):
    def __init__(self):
        super().__init__(DeliveryMilestones)

<<<<<<< HEAD
    def convert_to_desc(self, milestones):
        string_milestones = []
        for milestone in milestones:
                string_milestones.append({
                    "description":  f"Delivery completed by {milestone['assigneeUser']['username']}",
                    "timestamp": milestone["timestamp"]
                })
        return string_milestones

""""""


class TicketController(BaseTimeSeriesController):
    def __init__(self):
        super().__init__(TicketEvents)
        self.ticket_status_controller = TicketStatusController()
        self.creation_milestone_controller = CreationMilestonesController()
        self.inventory_milestone_controller = InventoryMilestonesController()
        self.assigned_milestones_controller = AssignmentMilestonesController()

    def _create_base_event(self, args_dict):

        is_pickup = args_dict["isPickup"]

        if not is_pickup:
            # THIS WILL BE CHANGED BACK WHEN INVENTORY CHECK IN IS A FEATURE
            args_dict["newStatus"] = Creation_Milestone_Status.ticket_created.value
            fields = {
                "currentStatus": Inventory_Milestone_Status.checked_into_inventory.value
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

        new_status = args_dict["newStatus"]
        args_dict.pop("newStatus", None)
        # args_dict[self.primary_key] = milestone.ticketId
        args_dict[self.model.non_prim_identifying_column_name] = milestone.ticketId

        obj = self.model(**args_dict)
        self.session.add(obj)
        self.session.commit()

        self.creation_milestone_controller._create(
            {
                "ticketId": obj.ticketId,
                "newStatus": new_status,
                "createdByUserId": args_dict["userId"],
            }
        )

        self.inventory_milestone_controller._create(
            {
                "ticketId": obj.ticketId,
                "oldStatus": new_status,
                "newStatus": Inventory_Milestone_Status.checked_into_inventory.value,
                "approvedByUserId": args_dict["userId"],
            }
        )
        return obj
=======

class UserController(DocumentController):
    def __init__(self):
        super().__init__(Documents)
>>>>>>> Stefan codeazzzzzzzzzzzzzzzzzzzzzzzzzzzz
