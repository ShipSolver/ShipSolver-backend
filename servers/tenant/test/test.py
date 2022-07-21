from multiprocessing import managers
from pprint import pprint
import json
import random
from typing import Generic
from faker import Faker
import os
from flask import Flask, jsonify
import uuid
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
    CreationMilestonesController,
    PickupMilestonesController,
    InventoryMilestonesController,
    AssignmentMilestonesController,
    DeliveryMilestonesController,
    IncompleteDeliveryMilestonesController,
    Generic_Milestone_Status,
    Creation_Milestone_Status,
    Pickup_Milestone_Status,
    Inventory_Milestone_Status,
    Assignment_Milestone_Status,
    Delivery_Milestone_Status,
    Incomplete_Delivery_Milestone_Status,
)
from utils import alchemyConverter
from utils import AlchemyEncoder
from const.milestones import *

faker = Faker()

app = Flask(__name__)
with app.app_context():

    # Controllers
    creationMilestonesController = CreationMilestonesController()
    pickupMilestonesController = PickupMilestonesController()
    inventoryMilestonesController = InventoryMilestonesController()
    assignmentMilestonesController = AssignmentMilestonesController()
    deliveryMilestonesController = DeliveryMilestonesController()
    incompleteDeliveryMilestonesController = IncompleteDeliveryMilestonesController()

    reprocessPickupsSet = [
        Generic_Milestone_Status.unassigned_pickup,
        Generic_Milestone_Status.requested_pickup,
        Generic_Milestone_Status.accepted_pickup,
        Generic_Milestone_Status.declined_pickup,
        Generic_Milestone_Status.completed_pickup,
        Generic_Milestone_Status.incomplete_pickup
    ]

    reprocessDeliverySet = [
        Generic_Milestone_Status.checked_into_inventory,
        Generic_Milestone_Status.completed_delivery,
        Generic_Milestone_Status.incomplete_delivery,
        Generic_Milestone_Status.assigned,
        Generic_Milestone_Status.in_transit
    ]

    maxReprocess = 4

    functionMapping = {
        "Creation_Milestone_Status": creationMilestonesController._create,
        "Pickup_Milestone_Status": pickupMilestonesController._create,
        "Inventory_Milestone_Status": inventoryMilestonesController._create,
        "Assignment_Milestone_Status": assignmentMilestonesController._create,
        "Delivery_Milestone_Status": deliveryMilestonesController._create,
        "Incomplete_Delivery_Milestone_Status": incompleteDeliveryMilestonesController._create,
    }

    usersByTypeList = {
        UserType.manager: [],
        UserType.dispatch: [],
        UserType.customer: [],
        UserType.driver: [],
        UserType.worker: [],
    }

    def generate_users(scale=5):

        user_controller = UserController()

        n = len(session.query(Users).all())

        args_arr = []

        if n < scale:
            print(f"Generating {scale - n } Users")
            for _ in range(scale - n):
                firstName = faker.unique.first_name()
                lastName = faker.unique.last_name()

                userType = random.choice([ut for ut in UserType])
                userTypeValue = userType.value.lower()
                username = firstName.lower()[0] + lastName.lower()
                email = f"{username}@faker.com"
                userId = random.randint(1, 1000000000)

                usersByTypeList[userType].append(userId)

                args_arr.append(
                    {
                        "userId": userId,
                        "userType": userTypeValue,
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

    def generate_ticket_events(scale=400, users=[], customers=[]):

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
                isPickup = False
                noSignatureRequired = False
                tailgateAuthorized = False

                obj = ticket_events_controller._create_base_event(
                    {
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
                        "pieces": pieces,
                        "isPickup": isPickup,
                        "noSignatureRequired": noSignatureRequired,
                        "tailgateAuthorized": tailgateAuthorized

                    }
                )

                # for i in range(random.randrange(10, 20)):

                #     userId = random.choice(users).userId
                #     userId = random.choice(users).userId
                #     customerId = random.choice(customers).customerId
                #     barcodeNumber = random.randrange(100000000, 900000000)
                #     houseReferenceNumber = random.randrange(100000000, 900000000)
                #     orderS3Link = "s3link"
                #     weight = random.randrange(100, 200)
                #     claimedNumberOfPieces = random.randrange(1, 5)
                #     BOLNumber = random.randrange(100000000, 900000000)

                #     created_obj = ticket_events_controller._modify_latest_object(
                #         getattr(obj, TicketEvents.non_prim_identifying_column_name),
                #         {
                #             "ticketId": obj.ticketId,
                #             "userId": userId,
                #             "customerId": customerId,
                #             "barcodeNumber": barcodeNumber,
                #             "houseReferenceNumber": houseReferenceNumber,
                #             "orderS3Link": orderS3Link,
                #             "weight": weight,
                #             "claimedNumberOfPieces": claimedNumberOfPieces,
                #             "BOLNumber": BOLNumber,
                #             "specialServices": specialServices,
                #             "specialInstructions": specialInstructions,
                #         },
                #     )

                print("Created Ticket")

    def list_diff(li1, li2):
        return list(set(li1) - set(li2)) + list(set(li2) - set(li1))

    def generate_transitions(ticket, transition_list, approver_list, start_state = null):
        '''
        Generates and inserts logical state transitions into milestones DBs
        @param ticket -> ticketID
        @param transition_list -> list of stte transitions to undergo
        @param approver_list -> list of user IDs of possible approvers
        '''
        prev_state = start_state
        curr_approver = null
        curr_driver = null

        for curr_state in transition_list:
            milestone_type = type(curr_state).__name__
            curr_state = curr_state.value
            
            if milestone_type == "Creation_Milestone_Status":
                curr_approver = random.choice(approver_list)
                data = {"ticketId" : ticket, "newStatus" : curr_state, "createdByUserId" : curr_approver}
            
            elif milestone_type == "Pickup_Milestone_Status": 
                curr_approver = curr_approver if curr_approver != null and random.randrange(2) == 0 else random.choice(approver_list)
                curr_driver = random.choice(usersByTypeList[UserType.driver])
                data = {
                    "ticketId" : ticket,
                    "newStatus" : curr_state,
                    "oldStatus" : prev_state,
                    "requesterUserId" : curr_approver,
                    "requestedUserId" : curr_driver
                    }

            elif milestone_type == "Inventory_Milestone_Status":
                curr_approver = curr_approver if curr_approver != null and random.randrange(2) == 0 else random.choice(approver_list)
                data = {
                    "ticketId" : ticket,
                    "newStatus" : curr_state,
                    "oldStatus" : prev_state,
                    "approvedByUserId" : curr_approver
                    }
            
            elif milestone_type == "Assignment_Milestone_Status":
                curr_approver = curr_approver if curr_approver != null and random.randrange(2) == 0 else random.choice(approver_list)
                curr_driver = curr_driver if curr_driver != null else random.choice(usersByTypeList[UserType.driver])
                data = {
                    "ticketId" : ticket,
                    "newStatus" : curr_state,
                    "oldStatus" : prev_state,
                    "assignedByUserId" : curr_approver,
                    "assignedToUserId" : curr_driver
                    }
            
            elif milestone_type == "Delivery_Milestone_Status":
                data = {
                    "ticketId" : ticket,
                    "newStatus" : curr_state,
                    "oldStatus" : prev_state,
                    "completingUserId" : curr_driver,
                    "PODLink" : "https://www.youtube.com/watch?v=xvFZjo5PgG0",
                    "picture1Link" : "https://images.unsplash.com/flagged/photo-1572392640988-ba48d1a74457?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=464&q=80",
                    "picture2Link" : "https://images.unsplash.com/photo-1515405295579-ba7b45403062?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=880&q=80",
                    "picture3Link" : "https://images.unsplash.com/photo-1657817142233-8689b78b7f9f?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=415&q=80"
                    }
            
            elif milestone_type == "Incomplete_Delivery_Milestone_Status":
                due_to_end_shift = random.choice([True, False])
                incomplete_reason = "some reason for incompleteness" if not due_to_end_shift else "shift ended"
                data = {
                    "ticketId" : ticket,
                    "newStatus" : curr_state,
                    "oldStatus" :  prev_state,
                    "assigneeUserId" : curr_driver,
                    "reasonForIncomplete" : incomplete_reason,
                    "dueToEndedShift" : due_to_end_shift
                    }

            else:
                raise Exception(f"Logic for milsetone type {milestone_type} not found")
            
            functionMapping[milestone_type](data)
            prev_state = curr_state
    
    def generate_milestone_events(old_tickets):
        all_tickets = (
            session.query(TicketEvents)
            .with_entities(TicketEvents.ticketId)
            .distinct()
            .all()
        )
        all_tickets = [v for v, in all_tickets]

        new_tickets = list_diff(all_tickets, old_tickets)
        reprocess_pickups = []
        reprocess_deliveries = []

        approver_list = usersByTypeList[UserType.manager] + usersByTypeList[UserType.dispatch]

        for ticket in new_tickets:
            end_state = random.choice(list(Generic_Milestone_Status))
            transition_list = (
                random.choice(list(stateTable[end_state].values())) 
                if type(stateTable[end_state]) is dict
                else stateTable[end_state]
            )
            generate_transitions(ticket, transition_list, approver_list)
            if transition_list[-1] == Pickup_Milestone_Status.unassigned_pickup:
                reprocess_pickups.append((ticket, 1))
            elif (transition_list[-1] == Inventory_Milestone_Status.checked_into_inventory 
                and transition_list[-2] != Creation_Milestone_Status.ticket_created):
                reprocess_deliveries.append((ticket, 1))

        while reprocess_pickups:
            ticket, retry = reprocess_pickups.pop(0)
            end_state = random.choice(reprocessPickupsSet)
            transition_list = (
                random.choice(list(stateTable[end_state].values())) 
                if type(stateTable[end_state]) is dict
                else stateTable[end_state]
            )
            if transition_list and transition_list[0] == Creation_Milestone_Status.unassigned_pickup:
                transition_list.pop(0)
            generate_transitions(ticket, transition_list, approver_list, Pickup_Milestone_Status.unassigned_pickup.value)
            if retry < maxReprocess and transition_list and transition_list[-1] == Pickup_Milestone_Status.unassigned_pickup:
                reprocess_pickups.append((ticket, retry + 1))

        while reprocess_deliveries:
            ticket, retry = reprocess_deliveries.pop(0)
            end_state = random.choice(reprocessDeliverySet)
            transition_list = (
                random.choice(list(stateTable[end_state].values())) 
                if type(stateTable[end_state]) is dict
                else stateTable[end_state]
            )
            if transition_list and transition_list[0] == Creation_Milestone_Status.ticket_created:
                transition_list.pop(0)
            if transition_list and transition_list[0] == Inventory_Milestone_Status.checked_into_inventory:
                transition_list.pop(0)
            generate_transitions(ticket, transition_list, approver_list, Inventory_Milestone_Status.checked_into_inventory.value)
            if retry < maxReprocess and transition_list and transition_list[-1] == Inventory_Milestone_Status.checked_into_inventory:
                reprocess_deliveries.append((ticket, retry + 1))

    # def generate_generic_milestones_events(scale=50, ticket_map=[], users=[]):

    #     gen_milestone_controller = GenericMilestoneController()

    #     n = len(session.query(GenericMilestones).distinct().all())
    #     if n < scale:
    #         print(f"Generating Gen Milestones for {scale - n } Tickets")

    #         for _ in range(scale - n):

    #             ticketId = random.choice([k for k in ticket_map])

    #             for _ in range(
    #                 random.randint(4, 10)
    #             ):  # number of milestones per ticket

    #                 milestoneId = random.randint(1, 2147483645)
    #                 userId = random.choice(users).userId

    #                 ticketStatus = random.choice(
    #                     [e for e in Generic_Ticket_Status]
    #                 ).value.lower()

    #                 obj = gen_milestone_controller._create(
    #                     {
    #                         "milestoneId": milestoneId,
    #                         "ticketEventId": random.choice(ticket_map[ticketId]),
    #                         "userId": userId,
    #                         "ticketStatus": ticketStatus,
    #                     }
    #                 )

    #             print("Created Gen Milestone")

    # def generate_inventory_milestones_events(scale=50, ticket_map=[], users=[]):

    #     gen_milestone_controller = InventoryMilestoneController()

    #     n = len(session.query(InventoryMilestones).distinct().all())

    #     if n < scale:
    #         print(f"Generating Inventory Milestones for {scale - n } Tickets")

    #         for _ in range(scale - n):

    #             ticketId = random.choice([k for k in ticket_map])

    #             for _ in range(
    #                 random.randint(4, 10)
    #             ):  # number of milestones per ticket

    #                 milestoneId = random.randint(1, 2147483645)
    #                 userId = random.choice(users).userId

    #                 ticketStatus = random.choice(
    #                     [e for e in Generic_Ticket_Status]
    #                 ).value.lower()

    #                 approvalStatus = random.choice(
    #                     [e for e in Ticket_Approval_Status]
    #                 ).value.lower()

    #                 obj = gen_milestone_controller._create(
    #                     {
    #                         "milestoneId": milestoneId,
    #                         "ticketEventId": random.choice(ticket_map[ticketId]),
    #                         "userId": userId,
    #                         "ticketStatus": ticketStatus,
    #                         "approvalStatus": approvalStatus,
    #                     }
    #                 )

    #             print("Created Inventory Milestone")

    # def generate_delivery_milestones_events(scale=50, ticket_map=[], users=[]):

    #     gen_milestone_controller = DeliveryMilestoneController()

    #     n = len(session.query(DeliveryMilestones).distinct().all())

    #     if n < scale:
    #         print(f"Generating Delivery Milestones for {scale - n } Tickets")

    #         for _ in range(scale - n):

    #             ticketId = random.choice([k for k in ticket_map])

    #             for _ in range(
    #                 random.randint(4, 10)
    #             ):  # number of milestones per ticket

    #                 milestoneId = random.randint(1, 2147483645)
    #                 userId = random.choice(users).userId

    #                 ticketStatus = random.choice(
    #                     [e for e in Generic_Ticket_Status]
    #                 ).value.lower()

    #                 approvalStatus = random.choice(
    #                     [e for e in Ticket_Approval_Status]
    #                 ).value.lower()

    #                 obj = gen_milestone_controller._create(
    #                     {
    #                         "milestoneId": milestoneId,
    #                         "ticketEventId": random.choice(ticket_map[ticketId]),
    #                         "userId": userId,
    #                         "ticketStatus": ticketStatus,
    #                         "approvalStatus": approvalStatus,
    #                     }
    #                 )

    #             print("Created Delivery Milestone")

    generate_users(scale=70)
    users = session.query(Users).all()

    # print(random.choice(users))

    generate_customers(scale=100)
    customers = session.query(Customers).all()

    # pprint(alchemyConverter(users[0]))

    oldTickets = (
            session.query(TicketEvents)
            .with_entities(TicketEvents.ticketId)
            .distinct()
            .all()
        )
    oldTickets = [v for v, in oldTickets]

    generate_ticket_events(
        scale=500,
        users=users,
        customers=customers,
    )
    ticketEvents = session.query(TicketEvents).distinct().all()

    generate_milestone_events(oldTickets)

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
