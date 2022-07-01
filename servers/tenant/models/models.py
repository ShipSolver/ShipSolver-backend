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
    manager = "MANAGER"
    dispatch = "DISPATCH"
    customer = "CUSTOMER"
    brooker = "BROOKER"
    worker = "WORKER"


class Customers(Base):
    __tablename__ = "customers"
    customerId = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    def __repr__(self):
        return f"< Customers:: customerId: {self.customerId}, name: {self.name}>"


class Users(Base):
    __tablename__ = "users"
    userId = Column(Integer, primary_key=True, autoincrement=True)
    userType = Column(Enum(UserType), nullable=False)
    username = Column(String, nullable=False)
    firstName = Column(String, nullable=False)
    lastName = Column(String, nullable=False)
    email = Column(String, nullable=False)
    createdAt = Column(Integer, nullable=False, default=int(time.time()))
    modifiedAt = Column(Integer, nullable=False, default=int(time.time()))

    def __repr__(self):
        return f"< Users:: userId: {self.userId}>"


class ShipperEvents(Base):
    __tablename__ = "shipperevents"
    non_prim_identifying_column_name = "shipperId"
    shipperEventId = Column(Integer, primary_key=True, autoincrement=True)
    shipperId = Column(Integer, nullable=False)
    timestamp = Column(Integer, default=int(time.time()))
    userId = Column(Integer, ForeignKey(Users.userId))
    companyName = Column(String, nullable=False)
    address = Column(String, nullable=False)
    postalCode = Column(String, nullable=False)
    phoneNumber = Column(String, nullable=False, default=int(time.time()))

    user = relationship("Users")

    def __repr__(self):
        return f"<ShipperEvents:: shipperEventId: {self.shipperEventId}>"


class ConsigneeEvents(Base):
    __tablename__ = "consigneeevents"
    non_prim_identifying_column_name = "consigneeId"
    consigneeEventId = Column(Integer, primary_key=True, autoincrement=True)
    consigneeId = Column(Integer, nullable=False)
    timestamp = Column(Integer, default=int(time.time()))
    userId = Column(Integer, ForeignKey(Users.userId))
    companyName = Column(String, nullable=False)
    address = Column(String, nullable=False)
    postalCode = Column(String, nullable=False)
    phoneNumber = Column(String, nullable=False)

    user = relationship("Users")


class TicketEvents(Base):
    __tablename__ = "ticketevents"
    non_prim_identifying_column_name = "ticketId"
    ticketEventId = Column(Integer, primary_key=True, autoincrement=True)
    ticketId = Column(Integer, nullable=False)
    timestamp = Column(Integer, default=int(time.time()))
    shipperEventId = Column(
        Integer, ForeignKey(ShipperEvents.shipperEventId), nullable=False
    )
    consigneeEventId = Column(
        Integer, ForeignKey(ConsigneeEvents.consigneeEventId), nullable=False
    )
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

    shipperEvent = relationship("ShipperEvents")
    consigneeEvent = relationship("ConsigneeEvents")
    user = relationship("Users")
    customer = relationship("Customers")
    pieces = relationship(
        "PieceEvents",
        # lazy="dynamic",
        primaryjoin="TicketEvents.ticketEventId == PieceEvents.ticketEventId",
    )


class PieceEvents(Base):
    __tablename__ = "piecesevents"
    non_prim_identifying_column_name = "piecesId"
    piecesEventId = Column(Integer, primary_key=True, autoincrement=True)
    piecesId = Column(Integer, nullable=False)
    timestamp = Column(Integer, default=int(time.time()))
    ticketEventId = Column(Integer, ForeignKey(TicketEvents.ticketEventId))
    # customerId = Column(Integer, ForeignKey(Customers.customerId))
    userId = Column(Integer, ForeignKey(Users.userId))
    pieceDescription = Column(String)

    user = relationship("Users")  # represents user which created / modified object
    # customer = relationship("Customers")
    ticketEvents = relationship("TicketEvents", viewonly=True)


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


if __name__ == "__main__":
    shipperId_timestamp_idx = Index(
        "shipperId_timestamp_idx", ShipperEvents.shipperId, ShipperEvents.timestamp
    )

    INDEXES.append(shipperId_timestamp_idx)

    consigneeId_timestamp_idx = Index(
        "consigneeId_timestamp_idx", ConsigneeEvents.consigneeId, ConsigneeEvents.timestamp
    )

    INDEXES.append(consigneeId_timestamp_idx)

    ticketId_timestamp_idx = Index(
        "ticketId_timestamp_idx", TicketEvents.ticketId, TicketEvents.timestamp
    )

    INDEXES.append(ticketId_timestamp_idx)


    ticket_userId_idx = Index("ticket_userId_idx", TicketEvents.userId)

    INDEXES.append(ticket_userId_idx)


    ticket_customerId_idx = Index("ticket_customerId_idx", TicketEvents.customerId)

    INDEXES.append(ticket_customerId_idx)


    ticket_shippperId_idx = Index("ticket_shippperId_idx", TicketEvents.shipperEventId)

    INDEXES.append(ticket_shippperId_idx)


    ticket_consigneeId_idx = Index("ticket_consigneeId_idx", TicketEvents.consigneeEventId)

    INDEXES.append(ticket_consigneeId_idx)

    piecesId_timestamp_idx = Index(
        "piecesId_timestamp_idx", PieceEvents.piecesId, PieceEvents.timestamp
    )

    INDEXES.append(piecesId_timestamp_idx)

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
