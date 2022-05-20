CREATE INDEX idx_shipperEvents_comp ON ShipperEvents(shipperId, timestamp);

CREATE INDEX idx_shipperEvents_ts ON ShipperEvents(timestamp);

CREATE INDEX idx_consigneeEvents_comp ON ConsigneeEvents(consigneeId, timestamp);

CREATE INDEX idx_consigneeEvents_ts ON ConsigneeEvents(timestamp);

CREATE INDEX idx_ticketEvents_comp ON TicketEvents(ticketEventId, timestamp);

CREATE INDEX idx_ticketEvents_ts ON TicketEvents(timestamp);

CREATE INDEX idx_genericMilestones_comp ON GenericMilestones(milestoneId, timestamp);

CREATE INDEX idx_genericMilestones_ts ON GenericMilestones(timestamp);

CREATE INDEX idx_inventoryMilestones_comp ON InventoryMilestones(milestoneId, timestamp);

CREATE INDEX idx_inventoryMilestones_ts ON InventoryMilestones(timestamp);

CREATE INDEX idx_deliveryMilestones_comp ON DeliveryMilestones(milestoneId, timestamp);

CREATE INDEX idx_deliveryMilestones_ts ON DeliveryMilestones(timestamp);

CREATE INDEX idx_PieceEvents_comp ON PieceEvents(piecesEventId, timestamp);

CREATE INDEX idx_PieceEvents_ts ON PieceEvents(timestamp);