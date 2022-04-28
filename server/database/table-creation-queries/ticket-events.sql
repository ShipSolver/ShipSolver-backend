CREATE TABLE IF NOT EXISTS Users (
    userId INT, 
    userType Enum('manager','dispatch', 'customer', 'worker'),
    timestamp INT, 
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



CREATE TABLE IF NOT EXISTS GenericMilestones (
    milestoneId INT, 
    timestamp INT, 
    userId INT, 
    customerId INT,
    ticketTimeStamp INT,
    address VARCHAR(256),
    postalCode VARCHAR(7),
    phoneNumber VARCHAR(15),
    PRIMARY KEY(shipperEventId),
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
    orderS3Link VARCHAR(100),
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