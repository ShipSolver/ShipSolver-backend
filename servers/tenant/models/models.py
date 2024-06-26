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


class Creation_Milestone_Status(str, enum):
    ticket_created = "ticket_created"
    unassigned_pickup = "unassigned_pickup"


class Pickup_Milestone_Status(str, enum):
    unassigned_pickup = "unassigned_pickup"
    requested_pickup = "requested_pickup"
    accepted_pickup = "accepted_pickup"
    declined_pickup = "declined_pickup"
    completed_pickup = "completed_pickup"
    incomplete_pickup = "incomplete_pickup"


class Inventory_Milestone_Status(str, enum):
    ticket_created = "ticket_created"
    checked_into_inventory = "checked_into_inventory"
    completed_delivery = "completed_delivery"
    incomplete_delivery = "incomplete_delivery"


class Assignment_Milestone_Status(str, enum):
    checked_into_inventory = "checked_into_inventory"
    assigned = "assigned"
    in_transit = "in_transit"


class Delivery_Milestone_Status(str, enum):
    in_transit = "in_transit"
    completed_delivery = "completed_delivery"


class Incomplete_Delivery_Milestone_Status(str, enum):
    in_transit = "in_transit"
    incomplete_delivery = "incomplete_delivery"


class Generic_Milestone_Status(str, enum):
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

GenericMilestonesType: Enum = Enum(
    Generic_Milestone_Status,
    name="generic_milestones_type",
    create_constraint=True,
    metadata=Base.metadata,
    validate_strings=True,
)


""" END  MILESTONE STATUSES """


class UserType(str, enum):
    manager = "manager"
    dispatch = "dispatch"
    customer = "customer"
    driver = "driver"
    worker = "worker"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_ 


class Customers(Base):
    __tablename__ = "customers"
    customerId = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    def __repr__(self):
        return f"< Customers:: customerId: {self.customerId}, name: {self.name}>"


class Users(Base):
    __tablename__ = "users"
    userId = Column(String, primary_key=True)
    userType = Column(String, nullable=False)
    username = Column(String, nullable=False)
    firstName = Column(String, nullable=False)
    lastName = Column(String, nullable=False)
    email = Column(String, nullable=False)
    createdAt = Column(Integer, nullable=False, default=int(time.time()*1000))
    modifiedAt = Column(Integer, nullable=False, default=int(time.time()*1000))

    def __repr__(self):
        return f"< Users:: userId: {self.userId}>"


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
    timestamp = Column(Integer, default=int(time.time()*1000))
    customerName = Column(String, nullable=False)
    barcodeNumber = Column(String, nullable=False)
    houseReferenceNumber = Column(String, nullable=False)
    orderS3Link = Column(String, nullable=False)
    orderS3Path = Column(String, nullable=False)
    weight = Column(String, nullable=False)
    claimedNumberOfPieces = Column(Integer, nullable=False)
    BOLNumber = Column(String, nullable=False)
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
    noSignatureRequired = Column(Boolean, nullable=False)
    tailgateAuthorized = Column(Boolean, nullable=False)


class TicketStatus(Base):
    __tablename__ = "ticketstatus"
    ticketId = Column(Integer, primary_key=True, autoincrement=True)
    currentStatus = Column(GenericMilestonesType, nullable=False)
    assignedTo = Column(String, ForeignKey(Users.userId), nullable=True, index=True)

    user = relationship("Users")


class TicketEvents(Base):
    __tablename__ = "ticketevents"
    non_prim_identifying_column_name = "ticketId"
    ticketEventId = Column(Integer, primary_key=True, autoincrement=True)
    ticketId = Column(Integer, ForeignKey(TicketStatus.ticketId))
    timestamp = Column(Integer, default=int(time.time()*1000))
    userId = Column(String, ForeignKey(Users.userId), nullable=False, index=True)

    # TODO: forgein key customer ID
    customerName = Column(String, nullable=False)
    barcodeNumber = Column(String, nullable=False)
    houseReferenceNumber = Column(String, nullable=False)
    orderS3Link = Column(String, nullable=True)
    weight = Column(String, nullable=False)
    claimedNumberOfPieces = Column(Integer, nullable=False)
    BOLNumber = Column(String, nullable=False)
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
    isPickup = Column(Boolean, nullable=False)
    noSignatureRequired = Column(Boolean, nullable=False)
    tailgateAuthorized = Column(Boolean, nullable=False)
    ticketStatus = relationship("TicketStatus")
    user = relationship("Users")
    # customer = relationship("Customers")


class CreationMilestones(Base):
    __tablename__ = "creationmilestones"

    milestoneId = Column(Integer, primary_key=True, autoincrement=True)
    ticketId = Column(
        Integer, ForeignKey(TicketStatus.ticketId), nullable=False, index=True
    )

    newStatus = Column(Enum(Creation_Milestone_Status), nullable=False)

    createdByUserId = Column(
        String, ForeignKey(Users.userId), nullable=False, index=True
    )
    createdAt = Column(Integer, nullable=False, default=int(time.time()*1000))
    createdByUser = relationship("Users")


class PickupMilestones(Base):
    __tablename__ = "pickupmilestones"

    milestoneId = Column(Integer, primary_key=True, autoincrement=True)
    ticketId = Column(
        Integer, ForeignKey(TicketStatus.ticketId), nullable=False, index=True
    )

    requestedUserId = Column(
        String, ForeignKey(Users.userId), nullable=False, index=True
    )
    requesterUserId = Column(
        String, ForeignKey(Users.userId), nullable=False, index=True
    )

    oldStatus = Column(GenericMilestonesType, nullable=False)
    newStatus = Column(Enum(Pickup_Milestone_Status), nullable=False)
    timestamp = Column(Integer, nullable=False, default=int(time.time()*1000))

    requesterUser = relationship("Users", foreign_keys=[requesterUserId])
    requestedUser = relationship("Users", foreign_keys=[requestedUserId])


class InventoryMilestones(Base):
    __tablename__ = "inventorymilestones"

    milestoneId = Column(Integer, primary_key=True, autoincrement=True)
    ticketId = Column(
        Integer, ForeignKey(TicketStatus.ticketId), nullable=False, index=True
    )

    approvedByUserId = Column(
        String, ForeignKey(Users.userId), nullable=False, index=True
    )

    oldStatus = Column(GenericMilestonesType, nullable=False)
    newStatus = Column(Enum(Inventory_Milestone_Status), nullable=False)
    timestamp = Column(Integer, nullable=False, default=int(time.time()*1000))

    approvedByUser = relationship("Users")


class AssignmentMilestones(Base):
    __tablename__ = "assignmentmilestones"

    milestoneId = Column(Integer, primary_key=True, autoincrement=True)
    ticketId = Column(
        Integer, ForeignKey(TicketStatus.ticketId), nullable=False, index=True
    )
    assignedByUserId = Column(
        String, ForeignKey(Users.userId), nullable=False, index=True
    )
    assignedToUserId = Column(
        String, ForeignKey(Users.userId), nullable=False, index=True
    )

    oldStatus = Column(GenericMilestonesType, nullable=False)
    newStatus = Column(Enum(Assignment_Milestone_Status), nullable=False)
    timestamp = Column(Integer, nullable=False, default=int(time.time()*1000))

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
        GenericMilestonesType,
        default=Generic_Milestone_Status.in_transit.value,
    )
    assigneeUserId = Column(
        String, ForeignKey(Users.userId), nullable=False, index=True
    )
    reasonForIncomplete = Column(String, nullable=False)
    dueToEndedShift = Column(Boolean, default=False)
    timestamp = Column(Integer, nullable=False, default=int(time.time()*1000))

    assigneeUser = relationship("Users")


class DeliveryMilestones(Base):

    class FileTypes(enum):
        PODLink = "POD.jpeg"
        picture1Link = "Picture1.jpeg"
        picture2Link = "Picture2.jpeg"
        picture3Link = "Picture3.jpeg"

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
        GenericMilestonesType,
        default=Generic_Milestone_Status.in_transit.value,
    )

    completingUserId = Column(
        String, ForeignKey(Users.userId), nullable=False, index=True
    )
    
    PODLink = Column(String, nullable=False)
    picture1Link = Column(String, nullable=False) # this pod is mandatory
    picture2Link = Column(String, nullable=True)
    picture3Link = Column(String, nullable=True)

    timestamp = Column(Integer, nullable=False, default=int(time.time()*1000))

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


