DROP TYPE TEST_INVENTORY_TICKET_STATUS;
CREATE TYPE TEST_INVENTORY_TICKET_STATUS AS ENUM('SCANNED_INTO_WAREHOUSE', 'TICKET_CREATED', 'CHECKED_INTO_INVENTORY', 'INCOMPLETE_DELIVERY', 'COMPLETE_DELIVERY', 'APPROVED_POD');

CREATE TYPE TEST_TICKET_APPROVAL_STATUS AS ENUM('REENTRY', 'ENTRY');

CREATE TYPE TEST_PICKUP_TICKET_STATUS AS ENUM('UNASSIGNED', 'REQUESTED', 'ACCEPTED', 'DECLINED', 'COMPLETED','INCOMPLETE');


-- Test Check enum values
SELECT enum_range(NULL::TEST_PICKUP_TICKET_STATUS);

-- ------------------- --
-- INVENTORY MILESTONE --
-- ------------------- --
DROP TABLE TestInventoryMilestones;
CREATE TABLE IF NOT EXISTS TestInventoryMilestones (
    "milestoneId" INT,
    timestamp INT,
    "userId" INT,
    "ticketEventId" INT,
    "previousTicketStatus" TEST_INVENTORY_TICKET_STATUS,
    "currentTicketStatus" TEST_INVENTORY_TICKET_STATUS,
    "approvalStatus" TICKET_APPROVAL_STATUS,
    PRIMARY KEY("milestoneId"),
    CONSTRAINT "fk_ticketEventId" FOREIGN KEY ("ticketEventId") REFERENCES TicketEvents("ticketEventId")
);

-- Test add a TestInventoryMilestones
INSERT INTO TestInventoryMilestones ("milestoneId", timestamp, "userId", "ticketEventId", "previousTicketStatus", "currentTicketStatus", "approvalStatus")
VALUES (1, 123456, 1, 1, 'SCANNED_INTO_WAREHOUSE', 'TICKET_CREATED', NULL);

-- ---------------- --
-- PICKUP MILESTONE --
-- ---------------- --
DROP TABLE TestPickupMilestones;
CREATE TABLE IF NOT EXISTS TestPickupMilestones (
    "milestoneId" INT,
    timestamp INT,
    "ticketEventId" INT,
    "requesterId" INT,
    "requesteeId" INT,
    "reasonForDecline" VARCHAR(50),
    "previousTicketStatus" TEST_PICKUP_TICKET_STATUS,
    "currentTicketStatus" TEST_PICKUP_TICKET_STATUS,
    "approvalStatus" TICKET_APPROVAL_STATUS,
    PRIMARY KEY("milestoneId"),
    CONSTRAINT "fk_ticketEventId" FOREIGN KEY ("ticketEventId") REFERENCES TicketEvents("ticketEventId")
);

-- Test add a TestPickupMilestone
INSERT INTO TestPickupMilestones ("milestoneId", timestamp, "ticketEventId", "requesterId", "requesteeId", "reasonForDecline", "previousTicketStatus", "currentTicketStatus", "approvalStatus")
VALUES (1, 123456, 1, 123, 321, NULL, 'UNASSIGNED', 'REQUESTED', NULL);

-- ------------------ --
-- DELIVERY MILESTONE --
-- ------------------ --
CREATE TYPE TEST_DELIVERY_TICKET_STATUS AS ENUM('COMPLETED_DELIVERY', 'IN_TRANSIT');
DROP TABLE TestDeliveryMilestones;
CREATE TABLE IF NOT EXISTS TestDeliveryMilestones (
    "milestoneId" INT,
    timestamp INT,
    "ticketEventId" INT,
    "userId" INT,
    "previousTicketStatus" TEST_PICKUP_TICKET_STATUS,
    "currentTicketStatus" TEST_PICKUP_TICKET_STATUS,
    "approvalStatus" TICKET_APPROVAL_STATUS,
    "PODLink" VARCHAR(50),
    "signatureLink" VARCHAR(50),
    "picture1Link" VARCHAR(50),
    "picture2Link" VARCHAR(50),
    "picture3Link" VARCHAR(50),
    PRIMARY KEY("milestoneId"),
    CONSTRAINT "fk_ticketEventId" FOREIGN KEY ("ticketEventId") REFERENCES TicketEvents("ticketEventId")
);

