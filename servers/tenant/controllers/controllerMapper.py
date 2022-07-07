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


class TicketController(BaseTimeSeriesController):
    def __init__(self):
        super().__init__(TicketEvents)



class GenericMilestoneController(BaseTimeSeriesController):
    def __init__(self):
        super().__init__(GenericMilestones)


class InventoryMilestoneController(BaseTimeSeriesController):
    def __init__(self):
        super().__init__(InventoryMilestones)


class DeliveryMilestoneController(BaseTimeSeriesController):
    def __init__(self):
        super().__init__(DeliveryMilestones)


class UserController(DocumentController):
    def __init__(self):
        super().__init__(Documents)
