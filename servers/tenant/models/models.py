import os
import time
from sqlalchemy import Column, ForeignKey, Integer, String, Enum, Index
from sqlalchemy.orm import relationship
from enum import Enum as enum
from dataclasses import dataclass
from . import engine, Base

INDEXES = []


class Inventory_Ticket_Status(enum):
    reentry = "REENTRY"
    entry = "ENTRY"


class Ticket_Approval_Status(enum):
    reentry = "REENTRY"
    entry = "ENTRY"


class Delivery_Ticket_Status(enum):
    delivered = "DELIVERED"
    in_transit = "IN_TRANSIT"


class Generic_Ticket_Status(enum):
    inventory = "INVENTORY"
    assigned = "ASSIGNED"
    out_for_delivery = "OUT_FOR_DELIVERY"


class UserType(enum):
    manager = "manager"
    dispatch = "dispatch"
    customer = "customer"
    driver = "driver"
    worker = "worker"


class Customers(Base):
    __tablename__ = "customers"
    customerId = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    def __repr__(self):
        return f"< Customers:: customerId: {self.customerId}, name: {self.name}>"


class Users(Base):
    __tablename__ = "users"
    userId = Column(Integer, primary_key=True, autoincrement=True)
    userType = Column(String, nullable=False)
    username = Column(String, nullable=False)
    firstName = Column(String, nullable=False)
    lastName = Column(String, nullable=False)
    email = Column(String, nullable=False)
    createdAt = Column(Integer, nullable=False, default=int(time.time()))
    modifiedAt = Column(Integer, nullable=False, default=int(time.time()))

    def __repr__(self):
        return f"< Users:: userId: {self.userId}>"

class Documents(Base):
    __tablename__ = "documents"
    documentId = Column(Integer, nullable=False)
    timestamp = Column(Integer, default=int(time.time()))
    userId = Column(Integer, ForeignKey(Users.userId), nullable=False)
    customerId = Column(Integer, ForeignKey(Customers.customerId), nullable=False)
    barcodeNumber = Column(Integer, nullable=False)
    houseReferenceNumber = Column(Integer, nullable=False)
    orderS3Link = Column(String, nullable=False)
    weight = Column(Integer, nullable=False)
    claimedNumberOfPieces = Column(Integer, nullable=False)
    BOLNumber = Column(Integer, nullable=False)
    specialServices = Column(String)
    specialInstructions = Column(String)
    # shipper 
    shipperCompany = Column(String, nullable=False)
    shipperName = Column(String, nullable=False)
    shipperAddress = Column(String, nullable=False)
    shipperPostalCode = Column(String, nullable=False)
    shipperPhoneNumber = Column(String, nullable=False)
    # consignee
    consigneeCompany = Column(String, nullable=False)
    consigneeName = Column(String, nullable=False)
    consigneeAddress = Column(String, nullable=False)
    consigneePostalCode = Column(String, nullable=False)
    consigneePhoneNumber = Column(String, nullable=False)
    # pieces
    pieces = Column(String, nullable=False)

    
class TicketEvents(Base):
    __tablename__ = "ticketevents"
    non_prim_identifying_column_name = "ticketId"
    ticketEventId = Column(Integer, primary_key=True, autoincrement=True)
    ticketId = Column(Integer, nullable=False)
    timestamp = Column(Integer, default=int(time.time()))
    userId = Column(Integer, ForeignKey(Users.userId), nullable=False)
    customerId = Column(Integer, ForeignKey(Customers.customerId), nullable=False)
    barcodeNumber = Column(Integer, nullable=False)
    houseReferenceNumber = Column(Integer, nullable=False)
    orderS3Link = Column(String, nullable=False)
    weight = Column(Integer, nullable=False)
    claimedNumberOfPieces = Column(Integer, nullable=False)
    BOLNumber = Column(Integer, nullable=False)
    specialServices = Column(String)
    specialInstructions = Column(String)
    # shipper 
    shipperCompany = Column(String, nullable=False)
    shipperName = Column(String, nullable=False)
    shipperAddress = Column(String, nullable=False)
    shipperPostalCode = Column(String, nullable=False)
    shipperPhoneNumber = Column(String, nullable=False)
    # consignee
    consigneeCompany = Column(String, nullable=False)
    consigneeName = Column(String, nullable=False)
    consigneeAddress = Column(String, nullable=False)
    consigneePostalCode = Column(String, nullable=False)
    consigneePhoneNumber = Column(String, nullable=False)
    # pieces
    pieces = Column(String, nullable=False)
    user = relationship("Users")
    customer = relationship("Customers")


class GenericMilestones(Base):
    __tablename__ = "genericmilestones"
    milestoneId = Column(Integer, primary_key=True, autoincrement=True)
    ticketEventId = Column(
        Integer, ForeignKey(TicketEvents.ticketEventId), nullable=False
    )
    userId = Column(Integer, ForeignKey(Users.userId))
    ticketStatus = Column(Enum(Generic_Ticket_Status))
    createdAt = Column(Integer, nullable=False, default=int(time.time()))
    modifiedAt = Column(Integer, nullable=False, default=int(time.time()))

    user = relationship("Users")


class InventoryMilestones(Base):
    __tablename__ = "inventorymilestones"
    milestoneId = Column(Integer, primary_key=True, autoincrement=True)
    ticketEventId = Column(
        Integer, ForeignKey(TicketEvents.ticketEventId), nullable=False
    )
    userId = Column(Integer, ForeignKey(Users.userId))
    ticketStatus = Column(Enum(Generic_Ticket_Status))
    approvalStatus = Column(Enum(Ticket_Approval_Status))
    createdAt = Column(Integer, nullable=False, default=int(time.time()))
    modifiedAt = Column(Integer, nullable=False, default=int(time.time()))

    user = relationship("Users")


class DeliveryMilestones(Base):
    __tablename__ = "deliverymilestones"
    milestoneId = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(Integer, default=int(time.time()))
    ticketEventId = Column(
        Integer, ForeignKey(TicketEvents.ticketEventId), nullable=False
    )
    userId = Column(Integer, ForeignKey(Users.userId))
    ticketStatus = Column(Enum(Generic_Ticket_Status))
    approvalStatus = Column(Enum(Ticket_Approval_Status))
    PODLink = Column(String)
    picture1Link = Column(String)
    picture2Link = Column(String)
    picture3Link = Column(String)

    user = relationship("Users")


ticketId_timestamp_idx = Index(
    "ticketId_timestamp_idx", TicketEvents.ticketId, TicketEvents.timestamp
)

INDEXES.append(ticketId_timestamp_idx)


ticket_userId_idx = Index("ticket_userId_idx", TicketEvents.userId)

INDEXES.append(ticket_userId_idx)

ticket_customerId_idx = Index("ticket_customerId_idx", TicketEvents.customerId)

INDEXES.append(ticket_customerId_idx)

gen_milestoneId_idx = Index("gen_milestoneId_idx", GenericMilestones.milestoneId)

INDEXES.append(gen_milestoneId_idx)

inv_milestoneId_idx = Index("inv_milestoneId_idx", InventoryMilestones.milestoneId)

INDEXES.append(inv_milestoneId_idx)

del_milestoneId_idx = Index("del_milestoneId_idx", DeliveryMilestones.milestoneId)

INDEXES.append(del_milestoneId_idx)

print("Configuring DB ...")
Base.metadata.create_all(engine)
try:
    # create indexes
    for index in INDEXES:
        index.create(bind=engine)
except:
    pass
