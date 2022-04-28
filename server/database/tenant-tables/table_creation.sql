
declare @tablename varchar(50)
set @tablename = "TENANT1"

CREATE TABLE IF NOT EXISTS Customers (
    customerId INT, 
    name VARCHAR(50),
    PRIMARY KEY(customerId)
);


CREATE TABLE IF NOT EXISTS Users (
    userId INT, 
    userType Enum('MANAGER', 'DISPATCH', 'CUSTOMER', 'BROKER', 'WORKER'),
    username VARCHAR(30),
    firstName VARCHAR(30),
    lastName VARCHAR (30),
    email VARCHAR(30),
    createdAt INT,
    modifiedAt INT,
    PRIMARY KEY(userId)
);


CREATE TABLE IF NOT EXISTS ShipperEvents (
    shipperEventId INT, 
    shipperId INT, 
    timestamp INT, 
    userId INT, 
    company VARCHAR(256),
    name VARCHAR(256),
    address VARCHAR(256),
    postalCode VARCHAR(7),
    phoneNumber VARCHAR(15),
    PRIMARY KEY(shipperEventId),
    CONSTRAINT fk_userId FOREIGN KEY (userId) REFERENCES Users(userId)
); 


CREATE TABLE IF NOT EXISTS ConsigneeEvents (
    consigneeEventId INT, 
    consigneeId INT, 
    timestamp INT, 
    userId INT,
    company VARCHAR(256),
    name VARCHAR(256),
    address VARCHAR(256),
    postalCode VARCHAR(7),
    phoneNumber VARCHAR(15),
    PRIMARY KEY(consigneeEventId),
    CONSTRAINT fk_userId FOREIGN KEY (userId) REFERENCES Users(userId)
); 

CREATE TABLE IF NOT EXISTS TicketEvents  (
    ticketEventId INT,
    ticketId INT,
    timestamp INT,
    shipperId INT,
    consignee INT,
    userId INT,
    barcodeNumber INT,
    houseReferenceNumber INT,
    orderS3Link VARCHAR(50),
    weight INT,
    claimedNumberOfPieces INT,
    BOLNumber INT,
    specialServices VARCHAR(256),
    specialInstructions VARCHAR(256),
    PRIMARY KEY(ticketEventId),
    CONSTRAINT fk_shipperId FOREIGN KEY (shipperId) REFERENCES ShipperEvents(shipperId),
    CONSTRAINT fk_consigneeId FOREIGN KEY (consigneeId) REFERENCES ConsigneeEvents(consigneeId),
    CONSTRAINT fk_userId FOREIGN KEY (userId) REFERENCES Users(userId)
);


CREATE TABLE IF NOT EXISTS GenericMilestones (
    milestoneId INT, 
    timestamp INT, 
    ticketEventId INT,
    customerId INT, 
    userId INT, 
    ticketStatus Enum('INVENTORY', 'ASSIGNED', 'OUT_FOR_DELIVERY'),
    PRIMARY KEY(milestoneId),
    CONSTRAINT fk_ticketEventId FOREIGN KEY (ticketEventId) REFERENCES TicketEvents(ticketEventId),
    CONSTRAINT fk_customerId FOREIGN KEY (customerId) REFERENCES Customers(customerId)
    CONSTRAINT fk_userId FOREIGN KEY (userId) REFERENCES Users(userId)
); 



CREATE TABLE IF NOT EXISTS InventoryMilestones (
    milestoneId INT, 
    timestamp INT, 
    ticketEventId INT,
    customerId INT, 
    userId INT, 
    ticketStatus Enum('REENTRY', 'ENTRY'),
    approvalStatus Enum('APPROVED', 'PENDING', 'REJECTED'),
    PRIMARY KEY(milestoneId),
    CONSTRAINT fk_ticketEventId FOREIGN KEY (ticketEventId) REFERENCES TicketEvents(ticketEventId),
    CONSTRAINT fk_customerId FOREIGN KEY (customerId) REFERENCES Customers(customerId)
    CONSTRAINT fk_userId FOREIGN KEY (userId) REFERENCES Users(userId)
); 


CREATE TABLE IF NOT EXISTS DeliveryMilestones (
    milestoneId INT, 
    timestamp INT, 
    ticketEventId INT,  
    customerId INT, 
    userId INT, 
    ticketStatus Enum('DELIVERED'),
    approvalStatus Enum('APPROVED', 'PENDING', 'REJECTED'),
    PODLink VARCHAR(50),
    signatureLink VARCHAR(50),
    picture1Link VARCHAR(50), 
    picture2Link VARCHAR(50), 
    picture3Link VARCHAR(50), 
    PRIMARY KEY(milestoneId),
    CONSTRAINT fk_ticketEventId FOREIGN KEY (ticketEventId) REFERENCES TicketEvents(ticketEventId),
    CONSTRAINT fk_customerId FOREIGN KEY (customerId) REFERENCES Customers(customerId)
    CONSTRAINT fk_userId FOREIGN KEY (userId) REFERENCES Users(userId)
); 


CREATE TABLE IF NOT EXISTS PiecesEvents (
    piecesEventId INT, 
    piecesId INT, 
    timestamp INT, 
    ticketId INT,
    userId INT, 
    pieceDescription VARCHAR(256),
    PRIMARY KEY(piecesEventId),
    CONSTRAINT fk_ticketId FOREIGN KEY (ticketId) REFERENCES TicketEvents(ticketId)
    CONSTRAINT fk_userId FOREIGN KEY (userId) REFERENCES Users(userId)
);

