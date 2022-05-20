from turtle import update
from baseController import BaseTimeSeriesController
import sys

sys.path.insert(0, "..")  # import parent folder

from models.models import ConsigneeEvents, TicketEvents


ticket_controller = BaseTimeSeriesController(TicketEvents)


class ConsigneeController(BaseTimeSeriesController):
    def __init__(self):
        super().__init__(model=ConsigneeEvents)
        self.model = ConsigneeEvents

    def _propagating_modify(self, ConsigneeEvents, ticketEventId, update_dict):

        """
        Definition: creates a new shippper event with the same shipperId
                    but creates a new ticketEvent with the updated ConsigneeEvents for
                    the specfic ticket which is given in context
        """

        new_shipper_event = self._modify_object(shipperEventId, update_dict)

        ticket_update_dict = {"shipperEventId": new_shipper_event.shipperEventId}

        ticket_controller._modify_object(ticketEventId, ticket_update_dict)

        return new_shipper_event
