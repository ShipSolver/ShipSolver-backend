import os
import time
from sqlalchemy import Column, ForeignKey, Integer, String, Enum, Index, Boolean, null
from sqlalchemy.orm import relationship
from enum import Enum as enum
from itertools import chain
from dataclasses import dataclass
from . import engine, Base
import sys

INDEXES = []


""" MILESTONE STATUSES BEGIIN """


class Creation_Milestone_Status(enum):
    ticket_created = "ticket_created"
    unassigned_pickup = "unassigned_pickup"


class Pickup_Milestone_Status(enum):
    unassigned_pickup = "unassigned_pickup"
    requested_pickup = "requested_pickup"
    accepted_pickup = "accepted_pickup"
    declined_pickup = "declined_pickup"
    completed_pickup = "completed_pickup"
    incomplete_pickup = "incomplete_pickup"


class Inventory_Milestone_Status(enum):
    ticket_created = "ticket_created"
    checked_into_inventory = "checked_into_inventory"
    completed_delivery = "completed_delivery"
    incomplete_delivery = "incomplete_delivery"


class Assignment_Milestone_Status(enum):
    checked_into_inventory = "checked_into_inventory"
    assigned = "assigned"
    in_transit = "in_transit"


class Delivery_Milestone_Status(enum):
    in_transit = "in_transit"
    completed_delivery = "completed_delivery"


class Incomplete_Delivery_Milestone_Status(enum):
    in_transit = "in_transit"
    incomplete_delivery = "incomplete_delivery"


class Generic_Milestone_Status(enum):
    _ignore_ = "member cls"
    cls = vars()

    for member in chain(
        list(Creation_Milestone_Status),
        list(Pickup_Milestone_Status),
        list(Inventory_Milestone_Status),
        list(Assignment_Milestone_Status),
        list(Delivery_Milestone_Status),
        list(Incomplete_Delivery_Milestone_Status),
    ):
        # print(f"Name: {member.name} | Value: {member.value}")
        if member.name not in cls:
            cls[member.name] = member.value

    # del member, cls


""" END  MILESTONE STATUSES """


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

<<<<<<< HEAD

class DocumentStatus(Base):
    __tablename__ = "documentstatus"
    documentStatusId = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    status = Column(String, nullable=False, default="PENDING")
    numPages = Column(Integer, nullable=False)


class Documents(Base):
    __tablename__ = "documents"
    documentId = Column(Integer, primary_key=True, nullable=False)
    documentStatusId = Column(Integer, nullable=False)
    success = Column(Boolean, nullable=False)
    timestamp = Column(Integer, default=int(time.time()))
    barcodeNumber = Column(String, nullable=False)
    houseReferenceNumber = Column(String, nullable=False)
    orderS3Link = Column(String, nullable=False)
    weight = Column(String, nullable=False)
    claimedNumberOfPieces = Column(Integer, nullable=False)
    BOLNumber = Column(String, nullable=False)
    specialServices = Column(String)
    specialInstructions = Column(String)
    # shipper
=======
class Documents(Base):
    __tablename__ = "documents"
    documentId = Column(Integer, primary_key=True, nullable=False)
    timestamp = Column(Integer, default=int(time.time()))
    barcodeNumber = Column(Integer, nullable=False)
    houseReferenceNumber = Column(Integer, nullable=False)
    orderS3Link = Column(String, nullable=False)
    weight = Column(Integer, nullable=False)
    claimedNumberOfPieces = Column(Integer, nullable=False)
    BOLNumber = Column(Integer, nullable=False)
    specialServices = Column(String)
    specialInstructions = Column(String)
    # shipper 
>>>>>>> 32dee55d98864ba43414c8757ab4abe2e4881f66
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
<<<<<<< HEAD
    noSignatureRequired = Column(Boolean, nullable=False)
    tailgateAuthorized = Column(Boolean, nullable=False)
    customerName = Column(String, nullable=False)


class TicketStatus(Base):
    __tablename__ = "ticketstatus"
    ticketId = Column(Integer, primary_key=True, autoincrement=True)
    currentStatus = Column(Enum(Generic_Milestone_Status), nullable=False)
    assignedTo = Column(Integer, ForeignKey(Users.userId), nullable=True, index=True)
=======
    customerName = Column(String, nullable=False)
>>>>>>> 32dee55d98864ba43414c8757ab4abe2e4881f66



class TicketEvents(Base):
    __tablename__ = "ticketevents"
    non_prim_identifying_column_name = "ticketId"
    ticketEventId = Column(Integer, primary_key=True, autoincrement=True)
    # TODO: forgein key
    ticketId = Column(Integer, ForeignKey(TicketStatus.ticketId))
    timestamp = Column(Integer, default=int(time.time()))
<<<<<<< HEAD
    userId = Column(Integer, ForeignKey(Users.userId), nullable=False, index=True)
    customerId = Column(
        Integer, ForeignKey(Customers.customerId), nullable=False, index=True
    )
    barcodeNumber = Column(String, nullable=False)
    houseReferenceNumber = Column(String, nullable=False)
=======
    userId = Column(Integer, ForeignKey(Users.userId), nullable=False)
    customerId = Column(Integer, ForeignKey(Customers.customerId), nullable=False)
    barcodeNumber = Column(Integer, nullable=False)
    houseReferenceNumber = Column(Integer, nullable=False)
>>>>>>> 32dee55d98864ba43414c8757ab4abe2e4881f66
    orderS3Link = Column(String, nullable=False)
    weight = Column(String, nullable=False)
    claimedNumberOfPieces = Column(Integer, nullable=False)
    BOLNumber = Column(String, nullable=False)
    specialServices = Column(String)
    specialInstructions = Column(String)
<<<<<<< HEAD
    # shipper
=======
    # shipper 
>>>>>>> 32dee55d98864ba43414c8757ab4abe2e4881f66
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
<<<<<<< HEAD
    isPickup = Column(Boolean, nullable=False)
    noSignatureRequired = Column(Boolean, nullable=False)
    tailgateAuthorized = Column(Boolean, nullable=False)
    ticketStatus = relationship("TicketStatus")
    user = relationship("Users")
    customer = relationship("Customers")


class CreationMilestones(Base):
    __tablename__ = "creationmilestones"

    milestoneId = Column(Integer, primary_key=True, autoincrement=True)
    ticketId = Column(
        Integer, ForeignKey(TicketStatus.ticketId), nullable=False, index=True
    )
=======
    user = relationship("Users")
    customer = relationship("Customers")
>>>>>>> 32dee55d98864ba43414c8757ab4abe2e4881f66

    newStatus = Column(Enum(Creation_Milestone_Status), nullable=False)

    createdByUserId = Column(
        Integer, ForeignKey(Users.userId), nullable=False, index=True
    )
    createdAt = Column(Integer, nullable=False, default=int(time.time()))
    createdByUser = relationship("Users")


class PickupMilestones(Base):
    __tablename__ = "pickupmilestones"

    milestoneId = Column(Integer, primary_key=True, autoincrement=True)
    ticketId = Column(
        Integer, ForeignKey(TicketStatus.ticketId), nullable=False, index=True
    )

    requestedUserId = Column(
        Integer, ForeignKey(Users.userId), nullable=False, index=True
    )
    requesterUserId = Column(
        Integer, ForeignKey(Users.userId), nullable=False, index=True
    )

    oldStatus = Column(Enum(Generic_Milestone_Status), nullable=False)
    newStatus = Column(Enum(Pickup_Milestone_Status), nullable=False)
    timestamp = Column(Integer, nullable=False, default=int(time.time()))

    requesterUser = relationship("Users", foreign_keys=[requesterUserId])
    requestedUser = relationship("Users", foreign_keys=[requestedUserId])


class InventoryMilestones(Base):
    __tablename__ = "inventorymilestones"

<<<<<<< HEAD
    milestoneId = Column(Integer, primary_key=True, autoincrement=True)
    ticketId = Column(
        Integer, ForeignKey(TicketStatus.ticketId), nullable=False, index=True
    )

    approvedByUserId = Column(
        Integer, ForeignKey(Users.userId), nullable=False, index=True
    )

    oldStatus = Column(Enum(Generic_Milestone_Status), nullable=False)
    newStatus = Column(Enum(Inventory_Milestone_Status), nullable=False)
    timestamp = Column(Integer, nullable=False, default=int(time.time()))

    approvedByUser = relationship("Users")


class AssignmentMilestones(Base):
    __tablename__ = "assignmentmilestones"

    milestoneId = Column(Integer, primary_key=True, autoincrement=True)
    ticketId = Column(
        Integer, ForeignKey(TicketStatus.ticketId), nullable=False, index=True
    )
    assignedByUserId = Column(
        Integer, ForeignKey(Users.userId), nullable=False, index=True
    )
    assignedToUserId = Column(
        Integer, ForeignKey(Users.userId), nullable=False, index=True
    )

    oldStatus = Column(Enum(Generic_Milestone_Status), nullable=False)
    newStatus = Column(Enum(Assignment_Milestone_Status), nullable=False)
    timestamp = Column(Integer, nullable=False, default=int(time.time()))

    requesterUser = relationship("Users", foreign_keys=[assignedByUserId])
    requestedUser = relationship("Users", foreign_keys=[assignedToUserId])


class IncompleteDeliveryMilestones(Base):
    __tablename__ = "inconpletedeliverymilestones"

    milestoneId = Column(Integer, primary_key=True, autoincrement=True)
    ticketId = Column(
        Integer, ForeignKey(TicketStatus.ticketId), nullable=False, index=True
    )
    newStatus = Column(
        Enum(Incomplete_Delivery_Milestone_Status),
        default=Incomplete_Delivery_Milestone_Status.incomplete_delivery.value,
    )
    oldStatus = Column(
        Enum(Generic_Milestone_Status),
        default=Generic_Milestone_Status.in_transit.value,
    )
    assigneeUserId = Column(
        Integer, ForeignKey(Users.userId), nullable=False, index=True
    )
    reasonForIncomplete = Column(String, nullable=False)
    dueToEndedShift = Column(Boolean, default=False)
    timestamp = Column(Integer, nullable=False, default=int(time.time()))

    assigneeUser = relationship("Users")


class DeliveryMilestones(Base):
    __tablename__ = "deliverymilestones"

    milestoneId = Column(Integer, primary_key=True, autoincrement=True)
    ticketId = Column(
        Integer, ForeignKey(TicketStatus.ticketId), nullable=False, index=True
    )
    newStatus = Column(
        Enum(Delivery_Milestone_Status),
        default=Delivery_Milestone_Status.completed_delivery.value,
    )

    oldStatus = Column(
        Enum(Generic_Milestone_Status),
        default=Generic_Milestone_Status.in_transit.value,
    )

    completingUserId = Column(
        Integer, ForeignKey(Users.userId), nullable=False, index=True
    )
    PODLink = Column(String, nullable=False)
    picture1Link = Column(String, nullable=False)
    picture2Link = Column(String, nullable=False)
    picture3Link = Column(String, nullable=False)

    timestamp = Column(Integer, nullable=False, default=int(time.time()))

    completingUser = relationship("Users")


ticketId_timestamp_idx = Index(
    "ticketId_timestamp_idx", TicketEvents.ticketId, TicketEvents.timestamp
)

INDEXES.append(ticketId_timestamp_idx)

print("Configuring DB ...")
Base.metadata.create_all(engine)
try:
    # create indexes
    for index in INDEXES:
        index.create(bind=engine)
except:
    pass


=======
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
>>>>>>> 32dee55d98864ba43414c8757ab4abe2e4881f66
