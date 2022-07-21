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
        Generic_Milestone_Status.ticket_created: [
            Creation_Milestone_Status.ticket_created
        ],
        Generic_Milestone_Status.unassigned_pickup: {
            "happyPath": [Creation_Milestone_Status.unassigned_pickup],
            "failedPath1": [
                Creation_Milestone_Status.unassigned_pickup,
                Pickup_Milestone_Status.requested_pickup,
                Pickup_Milestone_Status.declined_pickup,
                Pickup_Milestone_Status.unassigned_pickup,
            ],
            "failedPath2": [
                Creation_Milestone_Status.unassigned_pickup,
                Pickup_Milestone_Status.requested_pickup,
                Pickup_Milestone_Status.accepted_pickup,
                Pickup_Milestone_Status.incomplete_pickup,
                Pickup_Milestone_Status.unassigned_pickup,
            ],
        },
        Generic_Milestone_Status.requested_pickup: [
            Creation_Milestone_Status.unassigned_pickup,
            Pickup_Milestone_Status.requested_pickup,
        ],
        Generic_Milestone_Status.accepted_pickup: [
            Creation_Milestone_Status.unassigned_pickup,
            Pickup_Milestone_Status.requested_pickup,
            Pickup_Milestone_Status.accepted_pickup,
        ],
        Generic_Milestone_Status.declined_pickup: [
            Creation_Milestone_Status.unassigned_pickup,
            Pickup_Milestone_Status.requested_pickup,
            Pickup_Milestone_Status.declined_pickup,
        ],
        Generic_Milestone_Status.completed_pickup: [
            Creation_Milestone_Status.unassigned_pickup,
            Pickup_Milestone_Status.requested_pickup,
            Pickup_Milestone_Status.accepted_pickup,
            Pickup_Milestone_Status.completed_pickup,
        ],
        Generic_Milestone_Status.incomplete_pickup: [
            Creation_Milestone_Status.unassigned_pickup,
            Pickup_Milestone_Status.requested_pickup,
            Pickup_Milestone_Status.accepted_pickup,
            Pickup_Milestone_Status.incomplete_pickup,
        ],
        Generic_Milestone_Status.checked_into_inventory: {
            "happyPath": [
                Creation_Milestone_Status.ticket_created,
                Inventory_Milestone_Status.checked_into_inventory,
            ],
            "failedPath1": [
                Creation_Milestone_Status.ticket_created,
                Inventory_Milestone_Status.checked_into_inventory,
                Assignment_Milestone_Status.assigned,
                Assignment_Milestone_Status.in_transit,
                Incomplete_Delivery_Milestone_Status.incomplete_delivery,
                Inventory_Milestone_Status.checked_into_inventory,
            ],
            "failedPath2": [
                Creation_Milestone_Status.ticket_created,
                Inventory_Milestone_Status.checked_into_inventory,
                Assignment_Milestone_Status.assigned,
                Assignment_Milestone_Status.in_transit,
                Delivery_Milestone_Status.completed_delivery,
                Inventory_Milestone_Status.incomplete_delivery,
                Inventory_Milestone_Status.checked_into_inventory,
            ]
        },
        Generic_Milestone_Status.completed_delivery: {
            "completed" : [
                Creation_Milestone_Status.ticket_created,
                Inventory_Milestone_Status.checked_into_inventory,
                Assignment_Milestone_Status.assigned,
                Assignment_Milestone_Status.in_transit,
                Delivery_Milestone_Status.completed_delivery,
            ],
            "approved" : [
                Creation_Milestone_Status.ticket_created,
                Inventory_Milestone_Status.checked_into_inventory,
                Assignment_Milestone_Status.assigned,
                Assignment_Milestone_Status.in_transit,
                Delivery_Milestone_Status.completed_delivery,
                Inventory_Milestone_Status.completed_delivery
            ]
        },
        Generic_Milestone_Status.incomplete_delivery: {
            "incomplete" : [
                Creation_Milestone_Status.ticket_created,
                Inventory_Milestone_Status.checked_into_inventory,
                Assignment_Milestone_Status.assigned,
                Assignment_Milestone_Status.in_transit,
                Incomplete_Delivery_Milestone_Status.incomplete_delivery,
            ],
            "declined" : [
                Creation_Milestone_Status.ticket_created,
                Inventory_Milestone_Status.checked_into_inventory,
                Assignment_Milestone_Status.assigned,
                Assignment_Milestone_Status.in_transit,
                Delivery_Milestone_Status.completed_delivery,
                Inventory_Milestone_Status.incomplete_delivery
            ]
        },
        Generic_Milestone_Status.assigned: [
            Creation_Milestone_Status.ticket_created,
            Inventory_Milestone_Status.checked_into_inventory,
            Assignment_Milestone_Status.assigned,
        ],
        Generic_Milestone_Status.in_transit: [
            Creation_Milestone_Status.ticket_created,
            Inventory_Milestone_Status.checked_into_inventory,
            Assignment_Milestone_Status.assigned,
            Assignment_Milestone_Status.in_transit,
        ],
    }