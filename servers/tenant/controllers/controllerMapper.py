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


class TicketController(BaseTimeSeriesController):
    def __init__(self):
        super().__init__(TicketEvents)


""" MILESTONES """


class CreationMilestonesController(BaseController):
    def __init__(self):
        super().__init__(CreationMilestones)


class PickupMilestonesController(BaseController):
    def __init__(self):
        super().__init__(PickupMilestones)


class InventoryMilestonesController(BaseController):
    def __init__(self):
        super().__init__(InventoryMilestones)


class AssignmentMilestonesController(BaseController):
    def __init__(self):
        super().__init__(AssignmentMilestones)


class IncompleteDeliveryMilestonesController(BaseController):
    def __init__(self):
        super().__init__(IncompleteDeliveryMilestones)


class DeliveryMilestonesController(BaseController):
    def __init__(self):
        super().__init__(DeliveryMilestones)
