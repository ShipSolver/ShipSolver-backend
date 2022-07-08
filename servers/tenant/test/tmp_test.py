from controllers.controllerMapper import (
    Generic_Milestone_Status,
    Creation_Milestone_Status,
    Pickup_Milestone_Status,
    Inventory_Milestone_Status,
    Assignment_Milestone_Status,
    Delivery_Milestone_Status,
    Incomplete_Delivery_Milestone_Status,
)

stateTable = {
    Generic_Milestone_Status.ticket_created: [Creation_Milestone_Status.ticket_created],
    Generic_Milestone_Status.unassigned_pickup: [
        Creation_Milestone_Status.unassigned_pickup
    ],
}

print(type(Creation_Milestone_Status.unassigned_pickup).__name__)
