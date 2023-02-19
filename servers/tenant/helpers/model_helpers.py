from models.models import (
    AssignmentMilestones,
    CreationMilestones,
    Customers,
    DeliveryMilestones,
    DocumentStatus,
    Documents,
    IncompleteDeliveryMilestones,
    InventoryMilestones,
    PickupMilestones,
    TicketEvents,
    TicketStatus,
    Users,
)

'''
NOTE: Ensure all Model names are strictly unique. Where Name == name.
So ensure uniqueness when capitalization is ignored.
'''
_name_to_model_map = {
    Customers.__name__.lower() : Customers,
    Users.__name__.lower() : Users,
    DocumentStatus.__name__.lower() : DocumentStatus,
    Documents.__name__.lower() : Documents,
    TicketStatus.__name__.lower() : TicketStatus,
    TicketEvents.__name__.lower() : TicketEvents,
    CreationMilestones.__name__.lower() : CreationMilestones,
    PickupMilestones.__name__.lower() : PickupMilestones,
    InventoryMilestones.__name__.lower() : InventoryMilestones,
    AssignmentMilestones.__name__.lower() : AssignmentMilestones,
    IncompleteDeliveryMilestones.__name__.lower() : IncompleteDeliveryMilestones,
    DeliveryMilestones.__name__.lower() : DeliveryMilestones,
}

def get_model_by_name(name: str):
    if name.lower() in _name_to_model_map:
        return _name_to_model_map[name.lower()]
    return None

def get_all_models():
    return _name_to_model_map.values()

