from baseController import (
    BaseController,
    BaseTimeSeriesController,
    BaseNestedDependencyContoller,
)
import sys

sys.path.insert(0, "..")  # import parent folder

from models.models import *


class UserController(BaseController):
    def __init__(self):
        super(Users, self).__init__()


class CustomerController(BaseController):
    def __init__(self):
        super(Customers, self).__init__()


class ShipperController(BaseNestedDependencyContoller):
    def __init__(self):
        super(ShipperEvents, self).__init__()


class ConsigneeController(BaseNestedDependencyContoller):
    def __init__(self):
        super(ConsigneeEvents, self).__init__()


class TicketController(BaseTimeSeriesController):
    def __init__(self):
        super(TicketEvents, self).__init__()


class PieceController(BaseTimeSeriesController):
    def __init__(self):
        super(PieceEvents, self).__init__()


class GenericMilestoneController(BaseTimeSeriesController):
    def __init__(self):
        super(GenericMilestones, self).__init__()


class InventoryMilestoneController(BaseTimeSeriesController):
    def __init__(self):
        super(InventoryMilestones, self).__init__()


class DeliveryMilestoneController(BaseTimeSeriesController):
    def __init__(self):
        super(DeliveryMilestones, self).__init__()
