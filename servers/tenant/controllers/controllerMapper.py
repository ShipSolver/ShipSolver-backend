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


class ShipperController(BaseNestedDependencyContoller):
    def __init__(self):
        super().__init__(ShipperEvents)


class ConsigneeController(BaseNestedDependencyContoller):
    def __init__(self):
        super().__init__(ConsigneeEvents)


class TicketController(BaseTimeSeriesController):
    def __init__(self):
        super().__init__(TicketEvents)


class PieceController(BaseTimeSeriesController):
    def __init__(self):
        super().__init__(PieceEvents)


class GenericMilestoneController(BaseTimeSeriesController):
    def __init__(self):
        super().__init__(GenericMilestones)


class InventoryMilestoneController(BaseTimeSeriesController):
    def __init__(self):
        super().__init__(InventoryMilestones)


class DeliveryMilestoneController(BaseTimeSeriesController):
    def __init__(self):
        super().__init__(DeliveryMilestones)
