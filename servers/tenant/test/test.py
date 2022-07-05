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
    TicketController,
    GenericMilestoneController,
    InventoryMilestoneController,
    DeliveryMilestoneController,
)
from utils import alchemyConverter
from utils import AlchemyEncoder

faker = Faker()

app = Flask(__name__)
with app.app_context():

    def generate_users(scale=5):

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

    def generate_customers(scale=2):

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


    def generate_ticket_events(
        scale=20, users=[], customers=[]
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
                userId = random.choice(users).userId
                customerId = random.choice(customers).customerId
                barcodeNumber = random.randrange(100000000, 900000000)
                houseReferenceNumber = random.randrange(100000000, 900000000)
                orderS3Link = "s3link"
                weight = random.randrange(100, 200)
                claimedNumberOfPieces = random.randrange(1, 5)
                BOLNumber = random.randrange(100000000, 900000000)
                specialServices = faker.sentence()
                specialInstructions = faker.sentence()
                shipperCompany = faker.company()
                shipperName = faker.name()
                shipperAddress = faker.address()
                shipperPostalCode = faker.zipcode()
                shipperPhoneNumber = faker.phone_number()
                consigneeCompany = faker.company()
                consigneeName = faker.name()
                consigneeAddress = faker.address()
                consigneePostalCode = faker.zipcode()
                consigneePhoneNumber = faker.phone_number()
                pieces = faker.sentence()

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
                        "shipperCompany": shipperCompany,
                        "shipperName": shipperName,
                        "shipperAddress": shipperAddress,
                        "shipperPostalCode": shipperPostalCode,
                        "shipperPhoneNumber": shipperPhoneNumber,
                        "consigneeCompany": consigneeCompany,
                        "consigneeName": consigneeName,
                        "consigneeAddress": consigneeAddress,
                        "consigneePostalCode": consigneePostalCode,
                        "consigneePhoneNumber": consigneePhoneNumber,
                        "pieces": pieces
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


    def generate_generic_milestones_events(scale=50, ticket_map=[], users=[]):

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

    def generate_inventory_milestones_events(scale=50, ticket_map=[], users=[]):

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

    def generate_delivery_milestones_events(scale=50, ticket_map=[], users=[]):

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

    # print(random.choice(users))

    generate_customers(scale=5)
    customers = session.query(Customers).all()

    # pprint(alchemyConverter(users[0]))

    generate_ticket_events(
        scale=20,
        users=users,
        customers=customers,
    )
    ticketEvents = session.query(TicketEvents).distinct().all()


    # pprint(alchemyConverter(ticketEvents[0]))

    # exit()


    pprint(alchemyConverter(ticketEvents[0]))

    exit()



    ticketIds = (
        session.query(TicketEvents.ticketId, TicketEvents.ticketEventId)
        # .limit(2000)
        .all()
    )

    # ticket_map = {}
    # for tid, teid in ticketIds:
    #     if tid not in ticket_map:
    #         ticket_map[tid] = []
    #     ticket_map[tid].append(teid)

    # generate_generic_milestones_events(scale=20, ticket_map=ticket_map, users=users)

    # generate_inventory_milestones_events(scale=20, ticket_map=ticket_map, users=users)

    # generate_delivery_milestones_events(scale=20, ticket_map=ticket_map, users=users)

    # ticketEvents = session.query(TicketEvents.ticketEventId).filter().all()

    # res = alchemyConverter(random.choice(ticketEvents))