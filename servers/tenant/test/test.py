from pprint import pprint
import json
import random
from typing import Generic
from faker import Faker
import os
from flask import Flask, jsonify

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sys

sys.path.insert(0, "..")  # import parent folder

from models.__init__ import session
from models.models import *
from controllers.controllerMapper import (
    UserController,
    CustomerController,
    ShipperController,
    ConsigneeController,
    TicketController,
    PieceController,
    GenericMilestoneController,
    InventoryMilestoneController,
    DeliveryMilestoneController,
)
from utils import alchemyConverter
from utils import AlchemyEncoder

faker = Faker()

app = Flask(__name__)
with app.app_context():

    def generate_users(scale=100):

        user_controller = UserController()

        n = len(session.query(Users).all())

        args_arr = []

        if n < scale:
            print(f"Generating {scale - n } Users")
            for _ in range(scale - n):
                firstName = faker.unique.first_name()
                lastName = faker.unique.last_name()

                userType = random.choice([ut for ut in UserType]).value.lower()
                username = firstName.lower()[0] + lastName.lower()
                email = f"{username}@faker.com"

                args_arr.append(
                    {
                        "userType": userType,
                        "username": username,
                        "firstName": firstName,
                        "lastName": lastName,
                        "email": email,
                    }
                )

                print(f"Generating {scale - n } Users")

        return user_controller._create_bulk(args_arr)

    def generate_customers(scale=100):

        customer_controller = CustomerController()

        n = len(session.query(Customers).all())

        args_arr = []

        if n < scale:
            print(f"Generating {scale - n } Customers")
            for _ in range(scale - n):
                company_name = faker.company()

                args_arr.append({"name": company_name})

                print(f"Generating {scale - n } Customers")

        return customer_controller._create_bulk(args_arr)

    def generate_shipper_events(scale=50, users=[]):

        shipper_events_controller = ShipperController()

        n = len(
            session.query(ShipperEvents)
            .filter(ShipperEvents.shipperEventId == ShipperEvents.shipperId)
            .distinct()
            .all()
        )

        if n < scale:
            print(f"Generating {scale - n } Shippers")

            for _ in range(scale - n):
                shipperId = random.randint(1, 2147483645)
                userId = random.choice(users).userId
                companyName = faker.company()
                address = faker.address()
                postalCode = faker.zipcode()
                phoneNumber = faker.phone_number()

                obj = shipper_events_controller._create_base_event(
                    {
                        "shipperId": shipperId,
                        "userId": userId,
                        "companyName": companyName,
                        "address": address,
                        "postalCode": postalCode,
                        "phoneNumber": phoneNumber,
                    }
                )

                # created_ids.append(obj.shipperEventId)

                for i in range(random.randrange(10, 20)):

                    userId = random.choice(users).userId

                    if i % 4 == 0:
                        companyName = faker.company()
                    elif i % 4 == 1:
                        address = faker.address()
                    elif i % 4 == 2:
                        postalCode = faker.zipcode()
                    elif i % 4 == 3:
                        phoneNumber = faker.phone_number()

                    # companyName = faker.company()
                    # address = faker.address()
                    # postalCode = faker.zipcode()
                    # phoneNumber = faker.phone_number()

                    created_obj = shipper_events_controller._modify_latest_object(
                        getattr(obj, ShipperEvents.non_prim_identifying_column_name),
                        {
                            "userId": userId,
                            "companyName": companyName,
                            "address": address,
                            "postalCode": postalCode,
                            "phoneNumber": phoneNumber,
                        },
                    )

                    print("Created Shipper")
                    # created_ids.append(created_obj.shipperEventId)

    def generate_consignee_events(scale=20, users=[]):

        shipper_events_controller = ConsigneeController()

        n = len(
            session.query(ConsigneeEvents)
            .filter(ConsigneeEvents.consigneeEventId == ConsigneeEvents.consigneeId)
            .distinct()
            .all()
        )

        if n < scale:
            print(f"Generating {scale - n } Consignee")

            for _ in range(scale - n):
                consigneeId = random.randint(1, 2147483645)
                userId = random.choice(users).userId
                companyName = faker.company()
                address = faker.address()
                postalCode = faker.zipcode()
                phoneNumber = faker.phone_number()

                obj = shipper_events_controller._create_base_event(
                    {
                        "consigneeId": consigneeId,
                        "userId": userId,
                        "companyName": companyName,
                        "address": address,
                        "postalCode": postalCode,
                        "phoneNumber": phoneNumber,
                    }
                )

                # created_ids.append(obj.shipperEventId)

                for i in range(random.randrange(10, 20)):

                    userId = random.choice(users).userId

                    if i % 4 == 0:
                        companyName = faker.company()
                    elif i % 4 == 1:
                        address = faker.address()
                    elif i % 4 == 2:
                        postalCode = faker.zipcode()
                    elif i % 4 == 3:
                        phoneNumber = faker.phone_number()

                    companyName = faker.company()
                    address = faker.address()
                    postalCode = faker.zipcode()
                    phoneNumber = faker.phone_number()

                    created_obj = shipper_events_controller._modify_latest_object(
                        getattr(obj, ConsigneeEvents.non_prim_identifying_column_name),
                        {
                            "userId": userId,
                            "companyName": companyName,
                            "address": address,
                            "postalCode": postalCode,
                            "phoneNumber": phoneNumber,
                        },
                    )

                    # created_ids.append(created_obj.shipperEventId)

                print("Created Consignee")

    def generate_ticket_events(
        scale=20, shipperEvents=[], consigneeEvents=[], users=[], customers=[]
    ):

        ticket_events_controller = TicketController()

        n = len(
            session.query(TicketEvents)
            .filter(TicketEvents.ticketEventId == TicketEvents.ticketId)
            .distinct()
            .all()
        )

        if n < scale:
            print(f"Generating {scale - n } Tickets")

            for _ in range(scale - n):
                shipperEventId = random.choice(shipperEvents).shipperEventId
                consigneeEventId = random.choice(consigneeEvents).consigneeEventId
                userId = random.choice(users).userId
                customerId = random.choice(customers).customerId
                barcodeNumber = random.randrange(100000000, 900000000)
                houseReferenceNumber = random.randrange(100000000, 900000000)
                orderS3Link = "s3link"
                weight = random.randrange(100, 200)
                claimedNumberOfPieces = random.randrange(1, 5)
                BOLNumber = random.randrange(100000000, 900000000)
                specialServices = ""
                specialInstructions = ""

                obj = ticket_events_controller._create_base_event(
                    {
                        "shipperEventId": shipperEventId,
                        "consigneeEventId": consigneeEventId,
                        "userId": userId,
                        "customerId": customerId,
                        "barcodeNumber": barcodeNumber,
                        "houseReferenceNumber": houseReferenceNumber,
                        "orderS3Link": orderS3Link,
                        "weight": weight,
                        "claimedNumberOfPieces": claimedNumberOfPieces,
                        "BOLNumber": BOLNumber,
                        "specialServices": specialServices,
                        "specialInstructions": specialInstructions,
                    }
                )

                for i in range(random.randrange(10, 20)):

                    userId = random.choice(users).userId
                    shipperEventId = random.choice(shipperEvents).shipperEventId
                    consigneeEventId = random.choice(consigneeEvents).consigneeEventId
                    userId = random.choice(users).userId
                    customerId = random.choice(customers).customerId
                    barcodeNumber = random.randrange(100000000, 900000000)
                    houseReferenceNumber = random.randrange(100000000, 900000000)
                    orderS3Link = "s3link"
                    weight = random.randrange(100, 200)
                    claimedNumberOfPieces = random.randrange(1, 5)
                    BOLNumber = random.randrange(100000000, 900000000)

                    created_obj = ticket_events_controller._modify_latest_object(
                        getattr(obj, TicketEvents.non_prim_identifying_column_name),
                        {
                            "ticketId": obj.ticketId,
                            "shipperEventId": shipperEventId,
                            "consigneeEventId": consigneeEventId,
                            "userId": userId,
                            "customerId": customerId,
                            "barcodeNumber": barcodeNumber,
                            "houseReferenceNumber": houseReferenceNumber,
                            "orderS3Link": orderS3Link,
                            "weight": weight,
                            "claimedNumberOfPieces": claimedNumberOfPieces,
                            "BOLNumber": BOLNumber,
                            "specialServices": specialServices,
                            "specialInstructions": specialInstructions,
                        },
                    )

                print("Created Ticket")

    def generate_pieces_events(scale=20, ticketEvents=[], customers=[], users=[]):

        pieces_events_controller = PieceController()

        n = len(
            session.query(PieceEvents)
            .filter(PieceEvents.piecesEventId == PieceEvents.piecesId)
            .distinct()
            .all()
        )

        if n < scale:
            print(f"Generating {scale - n } Pieces")

            for _ in range(scale - n):

                ticketEventId = random.choice(ticketEvents).ticketEventId

                for _ in range(1, 5):
                    piecesId = random.randint(1, 2147483645)
                    customerId = random.choice(customers).customerId
                    userId = random.choice(users).userId
                    pieceDescription = ""

                    obj = pieces_events_controller._create_base_event(
                        {
                            "piecesId": piecesId,
                            "ticketEventId": ticketEventId,
                            "customerId": customerId,
                            "userId": userId,
                            "pieceDescription": pieceDescription,
                        }
                    )

                    for i in range(random.randrange(1, 3)):

                        ticketEventId = random.choice(ticketEvents).ticketEventId
                        customerId = random.choice(customers).customerId
                        userId = random.choice(users).userId

                        created_obj = pieces_events_controller._modify_latest_object(
                            getattr(obj, PieceEvents.non_prim_identifying_column_name),
                            {
                                "piecesId": piecesId,
                                "ticketEventId": ticketEventId,
                                "customerId": customerId,
                                "userId": userId,
                                "pieceDescription": pieceDescription,
                            },
                        )

                print("Created Piece")

    def generate_generic_milestones_events(scale=200, ticket_map=[], users=[]):

        gen_milestone_controller = GenericMilestoneController()

        n = len(session.query(GenericMilestones).distinct().all())
        if n < scale:
            print(f"Generating Gen Milestones for {scale - n } Tickets")

            for _ in range(scale - n):

                ticketId = random.choice([k for k in ticket_map])

                for _ in range(
                    random.randint(4, 10)
                ):  # number of milestones per ticket

                    milestoneId = random.randint(1, 2147483645)
                    userId = random.choice(users).userId

                    ticketStatus = random.choice(
                        [e for e in Generic_Ticket_Status]
                    ).value.lower()

                    obj = gen_milestone_controller._create(
                        {
                            "milestoneId": milestoneId,
                            "ticketEventId": random.choice(ticket_map[ticketId]),
                            "userId": userId,
                            "ticketStatus": ticketStatus,
                        }
                    )

                print("Created Gen Milestone")

    def generate_inventory_milestones_events(scale=200, ticket_map=[], users=[]):

        gen_milestone_controller = InventoryMilestoneController()

        n = len(session.query(InventoryMilestones).distinct().all())

        if n < scale:
            print(f"Generating Inventory Milestones for {scale - n } Tickets")

            for _ in range(scale - n):

                ticketId = random.choice([k for k in ticket_map])

                for _ in range(
                    random.randint(4, 10)
                ):  # number of milestones per ticket

                    milestoneId = random.randint(1, 2147483645)
                    userId = random.choice(users).userId

                    ticketStatus = random.choice(
                        [e for e in Generic_Ticket_Status]
                    ).value.lower()

                    approvalStatus = random.choice(
                        [e for e in Ticket_Approval_Status]
                    ).value.lower()

                    obj = gen_milestone_controller._create(
                        {
                            "milestoneId": milestoneId,
                            "ticketEventId": random.choice(ticket_map[ticketId]),
                            "userId": userId,
                            "ticketStatus": ticketStatus,
                            "approvalStatus": approvalStatus,
                        }
                    )

                print("Created Inventory Milestone")

    def generate_delivery_milestones_events(scale=200, ticket_map=[], users=[]):

        gen_milestone_controller = DeliveryMilestoneController()

        n = len(session.query(DeliveryMilestones).distinct().all())

        if n < scale:
            print(f"Generating Delivery Milestones for {scale - n } Tickets")

            for _ in range(scale - n):

                ticketId = random.choice([k for k in ticket_map])

                for _ in range(
                    random.randint(4, 10)
                ):  # number of milestones per ticket

                    milestoneId = random.randint(1, 2147483645)
                    userId = random.choice(users).userId

                    ticketStatus = random.choice(
                        [e for e in Generic_Ticket_Status]
                    ).value.lower()

                    approvalStatus = random.choice(
                        [e for e in Ticket_Approval_Status]
                    ).value.lower()

                    obj = gen_milestone_controller._create(
                        {
                            "milestoneId": milestoneId,
                            "ticketEventId": random.choice(ticket_map[ticketId]),
                            "userId": userId,
                            "ticketStatus": ticketStatus,
                            "approvalStatus": approvalStatus,
                        }
                    )

                print("Created Delivery Milestone")

    generate_users(scale=10)
    users = session.query(Users).all()

    generate_customers(scale=5)
    customers = session.query(Customers).all()

    generate_shipper_events(scale=10, users=users)
    shipperEvents = session.query(ShipperEvents).limit(200).all()

    generate_consignee_events(scale=10, users=users)
    consigneeEvents = session.query(ConsigneeEvents).limit(200).all()

    generate_ticket_events(
        scale=20,
        shipperEvents=shipperEvents,
        consigneeEvents=consigneeEvents,
        users=users,
        customers=customers,
    )
    ticketEvents = session.query(TicketEvents).distinct().all()

    generate_pieces_events(
        scale=20, ticketEvents=ticketEvents, customers=customers, users=users
    )

    ticketIds = (
        session.query(TicketEvents.ticketId, TicketEvents.ticketEventId)
        # .limit(2000)
        .all()
    )

    ticket_map = {}
    for tid, teid in ticketIds:
        if tid not in ticket_map:
            ticket_map[tid] = []
        ticket_map[tid].append(teid)

    generate_generic_milestones_events(scale=20, ticket_map=ticket_map, users=users)

    generate_inventory_milestones_events(scale=20, ticket_map=ticket_map, users=users)

    generate_delivery_milestones_events(scale=20, ticket_map=ticket_map, users=users)

    ticketEvents = session.query(TicketEvents).filter(TicketEvents.ticketEventId).all()

    res = alchemyConverter(random.choice(ticketEvents))
    pprint(res)
