declare @tablename varchar(50) set @tablename = "TENANT1";

CREATE TYPE INVENTORY_TICKET_STATUS AS ENUM('REENTRY', 'ENTRY');

CREATE TYPE TICKET_APPROVAL_STATUS AS ENUM('REENTRY', 'ENTRY');

CREATE TYPE DELIVERY_TICKET_STATUS AS ENUM('DELIVERED', 'IN_TRANSIT');

CREATE TYPE GENERIC_TICKET_STATUS AS ENUM('INVENTORY', 'ASSIGNED', 'OUT_FOR_DELIVERY');

CREATE TYPE USERTYPE AS ENUM (
    'MANAGER',
    'DISPATCH',
    'CUSTOMER',
    'BROKER',
    'WORKER'
);

CREATE TABLE IF NOT EXISTS Customers (
    customerId INT,
    name VARCHAR(50),
    PRIMARY KEY(customerId)
);

CREATE TABLE IF NOT EXISTS Users (
    userId INT,
    userType USERTYPE NOT NULL,
    username VARCHAR(30) NOT NULL,
    firstName VARCHAR(30) NOT NULL,
    lastName VARCHAR (30) NOT NULL,
    email VARCHAR(30) NOT NULL,
    createdAt INT NOT NULL,
    modifiedAt INT NOT NULL,
    PRIMARY KEY(userId)
);

CREATE TABLE IF NOT EXISTS ShipperEvents (
    shipperEventId INT,
    shipperId INT NOT NULL,
    timestamp INT NOT NULL,
    userId INT NOT NULL,
    companyName VARCHAR(256) NOT NULL,
    address VARCHAR(256) NOT NULL,
    postalCode VARCHAR(7) NOT NULL,
    phoneNumber VARCHAR(15) NOT NULL,
    PRIMARY KEY(shipperEventId),
    CONSTRAINT fk_userId FOREIGN KEY (userId) REFERENCES Users(userId)
);

CREATE TABLE IF NOT EXISTS ConsigneeEvents (
    consigneeEventId INT NOT NULL,
    consigneeId INT NOT NULL,
    timestamp INT NOT NULL,
    userId INT NOT NULL,
    company VARCHAR(256) NOT NULL,
    name VARCHAR(256) NOT NULL,
    address VARCHAR(256) NOT NULL,
    postalCode VARCHAR(7) NOT NULL,
    phoneNumber VARCHAR(15) NOT NULL,
    PRIMARY KEY(consigneeEventId) NOT NULL,
    CONSTRAINT fk_userId FOREIGN KEY (userId) REFERENCES Users(userId)
);

CREATE TABLE IF NOT EXISTS TicketEvents (
    ticketEventId INT,
    ticketId INT,
    timestamp INT,
    shipperEventId INT,
    consigneeEventId INT,
    userId INT,
    customerId INT,
    barcodeNumber INT,
    houseReferenceNumber INT,
    orderS3Link VARCHAR(50),
    weight INT,
    claimedNumberOfPieces INT,
    BOLNumber INT,
    specialServices VARCHAR(256),
    specialInstructions VARCHAR(256),
    PRIMARY KEY(ticketEventId),
    CONSTRAINT fk_shipperId FOREIGN KEY (shipperEventId) REFERENCES ShipperEvents(shipperEventId),
    CONSTRAINT fk_consigneeId FOREIGN KEY (consigneeEventId) REFERENCES ConsigneeEvents(consigneeEventId),
    CONSTRAINT fk_customerId FOREIGN KEY (customerId) REFERENCES Customers(customerId),
    CONSTRAINT fk_userId FOREIGN KEY (userId) REFERENCES Users(userId)
);

CREATE TABLE IF NOT EXISTS GenericMilestones (
    milestoneId INT,
    timestamp INT,
    ticketEventId INT,
    customerId INT,
    userId INT,
    ticketStatus GENERIC_TICKET_STATUS,
    PRIMARY KEY(milestoneId),
    CONSTRAINT fk_ticketEventId FOREIGN KEY (ticketEventId) REFERENCES TicketEvents(ticketEventId),
    CONSTRAINT fk_customerId FOREIGN KEY (customerId) REFERENCES Customers(customerId),
    CONSTRAINT fk_userId FOREIGN KEY (userId) REFERENCES Users(userId)
);

CREATE TABLE IF NOT EXISTS InventoryMilestones (
    milestoneId INT,
    timestamp INT,
    ticketEventId INT,
    customerId INT,
    userId INT,
    ticketStatus INVENTORY_TICKET_STATUS,
    approvalStatus TICKET_APPROVAL_STATUS,
    PRIMARY KEY(milestoneId),
    CONSTRAINT fk_ticketEventId FOREIGN KEY (ticketEventId) REFERENCES TicketEvents(ticketEventId),
    CONSTRAINT fk_customerId FOREIGN KEY (customerId) REFERENCES Customers(customerId),
    CONSTRAINT fk_userId FOREIGN KEY (userId) REFERENCES Users(userId)
);

CREATE TABLE IF NOT EXISTS DeliveryMilestones (
    milestoneId INT,
    timestamp INT,
    ticketEventId INT,
    customerId INT,
    userId INT,
    ticketStatus DELIVERY_TICKET_STATUS,
    approvalStatus TICKET_APPROVAL_STATUS,
    PODLink VARCHAR(50),
    signatureLink VARCHAR(50),
    picture1Link VARCHAR(50),
    picture2Link VARCHAR(50),
    picture3Link VARCHAR(50),
    PRIMARY KEY(milestoneId),
    CONSTRAINT fk_ticketEventId FOREIGN KEY (ticketEventId) REFERENCES TicketEvents(ticketEventId),
    CONSTRAINT fk_customerId FOREIGN KEY (customerId) REFERENCES Customers(customerId),
    CONSTRAINT fk_userId FOREIGN KEY (userId) REFERENCES Users(userId)
);

CREATE TABLE IF NOT EXISTS PieceEvents (
    piecesEventId INT,
    piecesId INT,
    timestamp INT,
    ticketEventId INT,
    userId INT,
    pieceDescription VARCHAR(256),
    PRIMARY KEY(piecesEventId),
    CONSTRAINT fk_ticketId FOREIGN KEY (ticketEventId) REFERENCES TicketEvents(ticketEventId),
    CONSTRAINT fk_userId FOREIGN KEY (userId) REFERENCES Users(userId)
);