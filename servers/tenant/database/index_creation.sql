<<<<<<< HEAD
-- SQLBook: Code
=======
>>>>>>> modifying db schema
CREATE INDEX idx_ticketEvents_comp ON TicketEvents(ticketEventId, timestamp);

CREATE INDEX idx_ticketEvents_ts ON TicketEvents(timestamp);

CREATE INDEX idx_genericMilestones_comp ON GenericMilestones(milestoneId, timestamp);

CREATE INDEX idx_genericMilestones_ts ON GenericMilestones(timestamp);

CREATE INDEX idx_inventoryMilestones_comp ON InventoryMilestones(milestoneId, timestamp);

CREATE INDEX idx_inventoryMilestones_ts ON InventoryMilestones(timestamp);

CREATE INDEX idx_deliveryMilestones_comp ON DeliveryMilestones(milestoneId, timestamp);

CREATE INDEX idx_deliveryMilestones_ts ON DeliveryMilestones(timestamp);

