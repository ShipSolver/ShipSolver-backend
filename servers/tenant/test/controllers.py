from controllers.controllerMapper import (
    UserController,
    CreationMilestonesController,
    PickupMilestonesController,
    InventoryMilestonesController,
    AssignmentMilestonesController,
    DeliveryMilestonesController,
    TicketController,
    IncompleteDeliveryMilestonesController,
    CustomerController
)
creationMilestonesController = CreationMilestonesController()
pickupMilestonesController = PickupMilestonesController()
inventoryMilestonesController = InventoryMilestonesController()
assignmentMilestonesController = AssignmentMilestonesController()
deliveryMilestonesController = DeliveryMilestonesController()
incompleteDeliveryMilestonesController = IncompleteDeliveryMilestonesController()
user_controller = UserController()
ticket_events_controller = TicketController()
customer_controller = CustomerController()