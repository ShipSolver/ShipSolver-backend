from pprint import pprint
from controllers.baseController import (
    BaseController,
    BaseTimeSeriesController,
    BaseNestedDependencyContoller,
)
from utils import alchemyConverter
from models.models import *
import uuid
import base64
from controllers.S3Controller import S3Controller
from helpers.identity_helpers import IdentityHelper
FileTypes = DeliveryMilestones.FileTypes

class DocumentController(BaseController):
    def __init__(self):
        super().__init__(Documents)

class DocumentStatusController(BaseController):
    def __init__(self):
        super().__init__(DocumentStatus)


class UserController(BaseController):
    def __init__(self):
        super().__init__(Users)
    
    def get_user_type(self, userId):

        
        user_arr = alchemyConverter(self._get(filters={
            "userId" : userId
        }))

        assert len(user_arr) > 0, f"NO USER WITH {userId} IS FOUND"

        return user_arr[0]["userType"]


class CustomerController(BaseController):
    def __init__(self):
        super().__init__(Customers)


class TicketStatusController(BaseController):
    def __init__(self):
        super().__init__(TicketStatus)
        self.ticket_controller = BaseTimeSeriesController(TicketEvents)

    def _get_tickets_with_status(self, status, filters: dict, limit):
        subq_filter = [TicketStatus.currentStatus == status]

        if "ticketStatusAssignedTo" in filters:
            subq_filter.append(TicketStatus.assignedTo == filters["ticketStatusAssignedTo"])
            filters.pop("ticketStatusAssignedTo")

        subq = (
            self._get_session().query(TicketStatus.ticketId, TicketStatus.assignedTo)
            .filter(*subq_filter)
            .subquery()
        )

        q = self._get_session().query(TicketEvents).join(
            subq, TicketEvents.ticketId == subq.c.ticketId
        )

        tickets = self.ticket_controller._get_latest_event_object(filters=filters, queryObj=q, distinct=TicketEvents.ticketId)

        return tickets

""" MILESTONES """

class MilestoneController(BaseController):
    def __init__(self, model):
        super().__init__(model=model)
        self.model = model  # redudant
        self.ticket_status = TicketStatusController()

    def _create(self, args_dict):
        fltrs = {}
        updt = {}
        if "ticketId" in args_dict:
            fltrs[TicketStatus.ticketId.name] = args_dict["ticketId"]

            if "newStatus" in args_dict:
                updt[TicketStatus.currentStatus.name] = args_dict["newStatus"]
            
            if self.get_assigned_to_attr().name in args_dict:
                updt[TicketStatus.assignedTo.name] = args_dict[self.get_assigned_to_attr().name]
            
            self.ticket_status._modify(
                filters=fltrs,
                update_dict=updt
            )

        return super()._create(args_dict)
    
    def get_prev_status(self, ticket_id):
        ticket_stat = self.ticket_status._get(filters={"ticketId" : ticket_id})
        if ticket_stat:
            return ticket_stat[0].currentStatus
        return None
    
    def get_assigned_to_attr(self):
        '''
        Abstract Class Function
        Must be implemented by inheriting class.
        '''
        raise NotImplementedError

class CreationMilestonesController(MilestoneController):
    def __init__(self):
        super().__init__(CreationMilestones)
    
    # Note - Creation Milestones Type has no "oldStatus" attribute. This should change to support PickupMilestones -> Creation Milestones state change
    def get_prev_status(self, ticket_id=None):
        # if next_status == Creation_Milestone_Status.unassigned_pickup:
        #     ticket_stat = self.ticket_status._get(filters={"ticketId" : ticket_id})
        #     return ticket_stat.currentStatus
        return None

    def convert_to_desc(self, milestones):
        string_milestones = []
        for milestone in milestones:
                string_milestones.append({
                    "description":  f"Ticket created by {milestone['createdByUser']['username']}",
                    "timestamp": milestone["createdAt"]
                })
        return string_milestones
    
    # Note - Creation Milestones Type has no "oldStatus" attribute. This should change to support PickupMilestones -> Creation Milestones state change
    def get_prev_status(self, ticket_id=None):
        # if next_status == Creation_Milestone_Status.unassigned_pickup:
        #     ticket_stat = self.ticket_status._get(filters={"ticketId" : ticket_id})
        #     return ticket_stat.currentStatus
        return None
    
    def get_assigned_to_attr(self):
        return CreationMilestones.createdByUserId
         

class PickupMilestonesController(MilestoneController):
    def __init__(self):
        super().__init__(PickupMilestones)

    def convert_to_desc(self, milestones):
        string_milestones = []
        for milestone in milestones:
            if milestone["oldStatus"] == Pickup_Milestone_Status.unassigned_pickup.value and milestone["newStatus"] == Pickup_Milestone_Status.requested_pickup.value:
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
    
    def get_assigned_to_attr(self):
        return PickupMilestones.requestedUserId

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
    
    def get_assigned_to_attr(self):
        return InventoryMilestones.approvedByUserId

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
    
    def _create(self, args_dict):
        if args_dict["newStatus"] == Assignment_Milestone_Status.in_transit:
            prev_milestone = self._get(filters={"ticketId" : args_dict["ticketId"]}, ordered=True, limit=1)
            if prev_milestone:
                args_dict["assignedByUserId"] = prev_milestone[0].assignedByUserId
                args_dict["assignedToUserId"] = prev_milestone[0].assignedToUserId
        return super()._create(args_dict)
    
    def get_assigned_to_attr(self):
        return AssignmentMilestones.assignedToUserId

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
    
    def get_assigned_to_attr(self):
        return IncompleteDeliveryMilestones.assigneeUserId
         
class DeliveryMilestonesController(MilestoneController):
    
    s3controller = S3Controller()

    def __init__(self):
        super().__init__(DeliveryMilestones)

    def _upload_file(self, ticketId, temp_milestone_id, args_dict, file_type:DeliveryMilestones.FileTypes):
        s3_base_path = "deliverymilestones"
        file_link = f"{s3_base_path}_{ticketId}_{temp_milestone_id}_{file_type.value}" 
        with open(file_link, "wb") as f:
            f.write(base64.b64decode(args_dict["pictures"][file_type.value]))

        self.s3controller._upload_file(file_link,  file_link.replace("_", "/"))
        os.remove(file_link)
        return file_link


    def _create(self, args_dict):
        
        # create temporary files 
        temp_milestone_id = str(uuid.uuid4())
        ticketId = args_dict["ticketId"]

        # parallelize this ?
        args_dict[FileTypes.PODLink.name] = self._upload_file(ticketId, temp_milestone_id, args_dict, FileTypes.PODLink)
        
        args_dict[FileTypes.picture1Link.name] = self._upload_file(ticketId, temp_milestone_id, args_dict, FileTypes.picture1Link)

        if (
            FileTypes.picture2Link.value in args_dict["pictures"] 
            and args_dict["pictures"][FileTypes.picture2Link.value] is not None
        ):
            args_dict[FileTypes.picture2Link.name] = self._upload_file(
                ticketId, temp_milestone_id, args_dict, FileTypes.picture2Link)

        if (
            FileTypes.picture3Link.value in args_dict["pictures"] 
            and args_dict["pictures"][FileTypes.picture3Link.value] is not None
        ):
            args_dict[FileTypes.picture3Link.name] = self._upload_file(
                ticketId, temp_milestone_id, args_dict, FileTypes.picture3Link)
        
        args_dict.pop("pictures")

        args_dict["completingUserId"] = IdentityHelper.get_logged_in_userId()
        
        print("Successfully uploaded milestones files to S3")

        return super()._create(args_dict)
            

    def convert_to_desc(self, milestones):
        string_milestones = []
        for milestone in milestones:
                presigned_pod_link = self.s3controller._generate_presigned_url(
                    milestone[FileTypes.PODLink.name].replace("_", "/") if milestone[FileTypes.PODLink.name] else None)
                
                presigned_pic1_link = self.s3controller._generate_presigned_url(
                    milestone[FileTypes.picture1Link.name].replace("_", "/") if milestone[FileTypes.picture1Link.name] else None)
                
                presigned_pic2_link = self.s3controller._generate_presigned_url(
                    milestone[FileTypes.picture2Link.name].replace("_", "/") if milestone[FileTypes.picture2Link.name] else None)
                
                presigned_pic3_link = self.s3controller._generate_presigned_url(
                    milestone[FileTypes.picture3Link.name].replace("_", "/") if milestone[FileTypes.picture3Link.name] else None)

                string_milestones.append(
                    {
                        "description":  f"Delivery completed by {milestone['completingUser']['username']}",
                        "timestamp": milestone["timestamp"],
                        FileTypes.PODLink.value : presigned_pod_link, 
                        FileTypes.picture1Link.value : presigned_pic1_link, 
                        FileTypes.picture2Link.value : presigned_pic2_link,
                        FileTypes.picture3Link.value : presigned_pic3_link
                    }
                )

        return string_milestones
    
    def get_assigned_to_attr(self):
        return DeliveryMilestones.completingUserId

""""""


class TicketController(BaseTimeSeriesController):
    def __init__(self):
        super().__init__(TicketEvents)
        self.ticket_status_controller = TicketStatusController()
        self.creation_milestone_controller = CreationMilestonesController()
        self.inventory_milestone_controller = InventoryMilestonesController()
        self.assigned_milestones_controller = AssignmentMilestonesController()
        self.user_controller = UserController()

    def _create_base_event(self, args_dict):

        is_pickup = args_dict["isPickup"]
        fields = {}

        if not is_pickup:
            # THIS WILL BE CHANGED BACK WHEN INVENTORY CHECK IN IS A FEATURE
            args_dict["newStatus"] = Creation_Milestone_Status.ticket_created
            fields["currentStatus"] = Generic_Milestone_Status(Inventory_Milestone_Status.checked_into_inventory.value)
        else:
            args_dict["newStatus"] = Generic_Milestone_Status(Creation_Milestone_Status.unassigned_pickup.value)
            fields["currentStatus"] = Generic_Milestone_Status(Creation_Milestone_Status.unassigned_pickup.value)

        if "ticketStatusAssignedTo" in args_dict:
            fields["assignedTo"] = args_dict["ticketStatusAssignedTo"]

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

        args_dict["timestamp"] = int(time.time())

        new_status = args_dict["newStatus"]
        args_dict.pop("newStatus", None)
        args_dict.pop("ticketStatus", None)
        args_dict.pop("ticketStatusAssignedTo", None)
        args_dict.pop("user", None)

        print("NEW TICKET EVENT:")
        args_dict[self.model.non_prim_identifying_column_name] = ticket_id

        obj = self.model(**args_dict)
        self.session.add(obj)
        self.session.commit()
        
        if new_ticket_creation:
            self.creation_milestone_controller._create(
                {
                    "ticketId": obj.ticketId,
                    "newStatus": new_status,
                    "createdByUserId": args_dict["userId"],
                }
            )

            if not is_pickup:
                self.inventory_milestone_controller._create(
                    {
                        "ticketId": obj.ticketId,
                        "oldStatus": new_status,
                        "newStatus": Inventory_Milestone_Status.checked_into_inventory.value,
                        "approvedByUserId": args_dict["userId"],
                    }
                )
        return obj
    
    def _delete_base_ticket(self, ticket_id, actioner_user_id):
        user_type = self.user_controller.get_user_type(actioner_user_id)
        
        if user_type != UserType.manager:
            return False
        
        self._delete(filters={"ticketId" : ticket_id})
        return True

    
    def _get_ticket_edits(self, ticket_id):
        data = self._get_event_objects_by_latest(
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
                if k not in ticket_dict or latest[k]!= ticket_dict[k]:
                    updates[k] = latest[k]

                if k == "user":
                    updates["userId"] = latest[k]["userId"]
                    updates["firstName"] = latest[k]["firstName"]
                    if "lastName" in latest[k]:
                        updates["lastName"] = latest[k]["lastName"]

                if k == "timestamp": # if two edits are made at the same second
                    updates[k] = latest[k]

            updates.pop(self.primary_key)
            updates_arr.append(updates)

            latest = ticket_dict
        return updates_arr

