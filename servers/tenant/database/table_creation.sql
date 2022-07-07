-- SQLBook: Code
declare @tablename varchar(50) set @tablename = "TENANT1";

CREATE TYPE INVENTORY_TICKET_STATUS AS ENUM('REENTRY', 'ENTRY');

CREATE TYPE TICKET_APPROVAL_STATUS AS ENUM('REENTRY', 'ENTRY');

CREATE TYPE DELIVERY_TICKET_STATUS AS ENUM('DELIVERED', 'IN_TRANSIT');

CREATE TYPE GENERIC_TICKET_STATUS AS ENUM('INVENTORY', 'ASSIGNED', 'OUT_FOR_DELIVERY');

CREATE TYPE USERTYPE AS ENUM (
    'MANAGER',
    'DISPATCH',
    'CUSTOMER',
    'DRIVER',
    'WORKER'
);

CREATE TABLE IF NOT EXISTS Customers (
    "customerId" INT,
    name VARCHAR(50),
    PRIMARY KEY("customerId")
);

CREATE TABLE IF NOT EXISTS Users (
    "userId" INT,
    "userType" USERTYPE NOT NULL,
    "username" VARCHAR(30) NOT NULL,
    "firstName" VARCHAR(30) NOT NULL,
    "lastName" VARCHAR (30) NOT NULL,
    "email" VARCHAR(30) NOT NULL,
    "createdAt" INT NOT NULL,
    "modifiedAt" INT NOT NULL,
    PRIMARY KEY("userId")
<<<<<<< HEAD
);

<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> Stefan codeazzzzzzzzzzzzzzzzzzzzzzzzzzzz
CREATE TABLE IF NOT EXISTS Documents (
    "documentId" INT,
    "timestamp" INT,
    "userId" INT,
    "customerName" INT,
    "barcodeNumber" INT,
    "houseReferenceNumber" INT,
    "orderS3Link" VARCHAR(50),
    "weight" INT,
    "claimedNumberOfPieces" INT,
    "BOLNumber" INT,
    "specialServices" VARCHAR(256),
    "specialInstructions" VARCHAR(256),
    "shipperCompany" VARCHAR(256),
    "shipperName" VARCHAR(256),
    "shipperAddress" VARCHAR(256),
    "shipperPostalCode" VARCHAR(256),
    "shipperPhoneNumber" VARCHAR(256),
    "consigneeCompany" VARCHAR(256),
    "consigneeName" VARCHAR(256),
    "consigneeAddress" VARCHAR(256),
    "consigneePostalCode" VARCHAR(256),
    "consigneePhoneNumber" VARCHAR(256),
    "pieces" VARCHAR(256),
    PRIMARY KEY("documentId")
<<<<<<< HEAD
=======
>>>>>>> push
=======
>>>>>>> Stefan codeazzzzzzzzzzzzzzzzzzzzzzzzzzzz
);

CREATE TABLE IF NOT EXISTS TicketEvents (
    "ticketEventId" INT,
    "ticketId" INT,
    "timestamp" INT,
<<<<<<< HEAD
    "userId" INT,
    "customerId" INT,
    "barcodeNumber" INT,
    "houseReferenceNumber" INT,
    "orderS3Link" VARCHAR(50),
    "weight" INT,
    "claimedNumberOfPieces" INT,
    "BOLNumber" INT,
    "specialServices" VARCHAR(256),
    "specialInstructions" VARCHAR(256),
    "shipperCompany" VARCHAR(256),
    "shipperName" VARCHAR(256),
    "shipperAddress" VARCHAR(256),
    "shipperPostalCode" VARCHAR(256),
    "shipperPhoneNumber" VARCHAR(256),
    "consigneeCompany" VARCHAR(256),
    "consigneeName" VARCHAR(256),
    "consigneeAddress" VARCHAR(256),
    "consigneePostalCode" VARCHAR(256),
    "consigneePhoneNumber" VARCHAR(256),
    "pieces" VARCHAR(256),
    PRIMARY KEY("ticketEventId"),
    CONSTRAINT "fk_customerId" FOREIGN KEY ("customerId") REFERENCES Customers("customerId"),
    CONSTRAINT "fk_userId" FOREIGN KEY ("userId") REFERENCES Users("userId")
=======

CREATE TABLE IF NOT EXISTS TicketEvents (
<<<<<<< HEAD
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
    shipperCompany VARCHAR(256),
    shipperName VARCHAR(256),
    shipperAddress VARCHAR(256),
    shipperPostalCode VARCHAR(256),
    shipperPhoneNumber VARCHAR(256),
    consigneeCompany VARCHAR(256),
    consigneeName VARCHAR(256),
    consigneeAddress VARCHAR(256),
    consigneePostalCode VARCHAR(256),
    consigneePhoneNumber VARCHAR(256),
    pieces VARCHAR(256),
    PRIMARY KEY(ticketEventId),
    CONSTRAINT fk_customerId FOREIGN KEY (customerId) REFERENCES Customers(customerId),
    CONSTRAINT fk_userId FOREIGN KEY (userId) REFERENCES Users(userId)
>>>>>>> modifying db schema
=======
    "ticketEventId" INT,
    "ticketId" INT,
    "timestamp" INT,
    "shipperEventId" INT,
    "consigneeEventId" INT,
=======
>>>>>>> Stefan codeazzzzzzzzzzzzzzzzzzzzzzzzzzzz
    "userId" INT,
    "customerId" INT,
    "barcodeNumber" INT,
    "houseReferenceNumber" INT,
    "orderS3Link" VARCHAR(50),
    "weight" INT,
    "claimedNumberOfPieces" INT,
    "BOLNumber" INT,
    "specialServices" VARCHAR(256),
    "specialInstructions" VARCHAR(256),
    "shipperCompany" VARCHAR(256),
    "shipperName" VARCHAR(256),
    "shipperAddress" VARCHAR(256),
    "shipperPostalCode" VARCHAR(256),
    "shipperPhoneNumber" VARCHAR(256),
    "consigneeCompany" VARCHAR(256),
    "consigneeName" VARCHAR(256),
    "consigneeAddress" VARCHAR(256),
    "consigneePostalCode" VARCHAR(256),
    "consigneePhoneNumber" VARCHAR(256),
    "pieces" VARCHAR(256),
    PRIMARY KEY("ticketEventId"),
    CONSTRAINT "fk_customerId" FOREIGN KEY ("customerId") REFERENCES Customers("customerId"),
    CONSTRAINT "fk_userId" FOREIGN KEY ("userId") REFERENCES Users("userId")
>>>>>>> push
);

CREATE TABLE IF NOT EXISTS GenericMilestones (
    "milestoneId" INT,
    timestamp INT,
    "ticketEventId" INT,
    "customerId" INT,
    "userId" INT,
    "ticketStatus" GENERIC_TICKET_STATUS,
    PRIMARY KEY("milestoneId"),
    CONSTRAINT "fk_ticketEventId" FOREIGN KEY ("ticketEventId") REFERENCES TicketEvents("ticketEventId"),
    CONSTRAINT "fk_customerId" FOREIGN KEY ("customerId") REFERENCES Customers("customerId"),
    CONSTRAINT "fk_userId" FOREIGN KEY ("userId") REFERENCES Users("userId")
);

CREATE TABLE IF NOT EXISTS InventoryMilestones (
    "milestoneId" INT,
    timestamp INT,
    "ticketEventId" INT,
    "customerId" INT,
    "userId" INT,
    "ticketStatus" INVENTORY_TICKET_STATUS,
    "approvalStatus" TICKET_APPROVAL_STATUS,
    PRIMARY KEY("milestoneId"),
    CONSTRAINT "fk_ticketEventId" FOREIGN KEY ("ticketEventId") REFERENCES TicketEvents("ticketEventId"),
    CONSTRAINT "fk_customerId" FOREIGN KEY ("customerId") REFERENCES Customers("customerId"),
    CONSTRAINT "fk_userId" FOREIGN KEY ("userId") REFERENCES Users("userId")
);

CREATE TABLE IF NOT EXISTS DeliveryMilestones (
<<<<<<< HEAD
<<<<<<< HEAD
    "milestoneId" INT,
    timestamp INT,
    "ticketEventId" INT,
    "customerId" INT,
    "userId" INT,
    "ticketStatus" DELIVERY_TICKET_STATUS,
    "approvalStatus" TICKET_APPROVAL_STATUS,
    "PODLink" VARCHAR(50),
    "signatureLink" VARCHAR(50),
    "picture1Link" VARCHAR(50),
    "picture2Link" VARCHAR(50),
    "picture3Link" VARCHAR(50),
    PRIMARY KEY("milestoneId"),
    CONSTRAINT "fk_ticketEventId" FOREIGN KEY ("ticketEventId") REFERENCES TicketEvents("ticketEventId"),
    CONSTRAINT "fk_customerId" FOREIGN KEY ("customerId") REFERENCES Customers("customerId"),
    CONSTRAINT "fk_userId" FOREIGN KEY ("userId") REFERENCES Users("userId")
=======
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
>>>>>>> modifying db schema
=======
    "milestoneId" INT,
    timestamp INT,
    "ticketEventId" INT,
    "customerId" INT,
    "userId" INT,
    "ticketStatus" DELIVERY_TICKET_STATUS,
    "approvalStatus" TICKET_APPROVAL_STATUS,
    "PODLink" VARCHAR(50),
    "signatureLink" VARCHAR(50),
    "picture1Link" VARCHAR(50),
    "picture2Link" VARCHAR(50),
    "picture3Link" VARCHAR(50),
    PRIMARY KEY("milestoneId"),
    CONSTRAINT "fk_ticketEventId" FOREIGN KEY ("ticketEventId") REFERENCES TicketEvents("ticketEventId"),
    CONSTRAINT "fk_customerId" FOREIGN KEY ("customerId") REFERENCES Customers("customerId"),
    CONSTRAINT "fk_userId" FOREIGN KEY ("userId") REFERENCES Users("userId")
>>>>>>> push
);