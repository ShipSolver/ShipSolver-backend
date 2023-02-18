from pprint import pprint
from controllers.baseController import (
    BaseController,
    BaseTimeSeriesController,
    BaseNestedDependencyContoller,
)
from utils import alchemyConverter
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
        self.ticket_controller = BaseTimeSeriesController(TicketEvents)

    def _get_tickets_with_status(self, status, filters: dict, limit):
        tickets = [] 

        ticketIds = (
            self.session.query(TicketStatus.ticketId)
            .filter(TicketStatus.currentStatus == status)
            .limit(limit)
            .all()
        )

        for i, tid_tup in enumerate(ticketIds):

            filters_cpy = filters.copy()
            filters_cpy["ticketId"] = tid_tup[0]

            ticket = self.ticket_controller._get_latest_event_objects(filters=filters_cpy)
            if len(ticket) > 0:
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
        else:
            args_dict["newStatus"] = Creation_Milestone_Status.unassigned_pickup.value

            fields = {
                "currentStatus": Creation_Milestone_Status.unassigned_pickup.value,
            }

        if "assignedTo" in args_dict:
            fields["assignedTo"] = args_dict["assignedTo"]

        new_ticket_creation = "ticketId" not in args_dict
        if not new_ticket_creation:
            self.ticket_status_controller._modify(
                filters={
                    "ticketId" : args_dict["ticketId"]
                }, 
                update_dict=fields)
            
            ticket_id = args_dict["ticketId"]
        else:
            ticket_id = self.ticket_status_controller._create(fields).ticketId

        new_status = args_dict["newStatus"]
        args_dict.pop("newStatus", None)
        args_dict.pop("ticketStatus", None)
        args_dict.pop("user", None)

        print("NEW TICKET EVENT:")
        pprint(args_dict)
        args_dict[self.model.non_prim_identifying_column_name] = ticket_id

        obj = self.model(**args_dict)
        self.session.add(obj)
        self.session.commit()

        print("\n TIME:", obj.timestamp)

        
        if new_ticket_creation:
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
    
    def get_ticket_edits(self, ticket_id):
        data = self._get_latest_event_objects(
            filters={
                TicketEvents.non_prim_identifying_column_name : ticket_id
            }
        )

        edits = alchemyConverter(data)

        if len(edits) == 0:
            return None

        updates_arr = []
        
        latest = None
        for ticket_dict in edits:
            if latest is None:
                latest = ticket_dict
                continue

            updates = {}
            for k in ticket_dict:
                if k not in latest or latest[k]!= ticket_dict[k]:
                    updates[k] = ticket_dict[k]

                if k == "user":
                    updates["userId"] = ticket_dict[k]["userId"]
                    updates["firstName"] = ticket_dict[k]["firstName"]
                    if "lastName" in ticket_dict[k]:
                        updates["lastName"] = ticket_dict[k]["lastName"]

                if k == "timestamp": # if two edits are made at the same second
                    updates[k] = ticket_dict[k]

            updates.pop(self.primary_key)
            updates_arr.append(updates)

            latest = ticket_dict
        return updates_arr

        
class DocumentController(BaseController):
    def __init__(self):
        super().__init__(Documents)
