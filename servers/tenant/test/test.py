# NOTE: If you haven't run the sync-users tool yet found in dev-tools folder, run that first

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

############# SET YOUR USER ID HERE #############
MANAGER_USER = ""

if not MANAGER_USER:
    print("SET YOUR MANAGER USER ID IN TEST.PY LINE 46")
    exit()

############# SET TO FLASE ONLY IF YOU WANT OTHER MANAGER USERS TO APPROVE TICKETS ############
APPROVER_ONLY_SELF = True

############# GENERATION VALUES ###############
GENERATE_CUSTOMERS = 10
GENERATE_TICKET_EVENTS = 30

app = Flask(__name__)
with app.app_context():

    # Controllers
    creationMilestonesController = CreationMilestonesController()
    pickupMilestonesController = PickupMilestonesController()
    inventoryMilestonesController = InventoryMilestonesController()
    assignmentMilestonesController = AssignmentMilestonesController()
    deliveryMilestonesController = DeliveryMilestonesController()
    incompleteDeliveryMilestonesController = IncompleteDeliveryMilestonesController()

    maxReprocess = 4

    # Convenience hack to condence written code
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

    # Depricated Do not Call
    def _generate_users(scale=5):
        '''
        DEPRICATED
        Generates fake users and inserts into users table

        Do Not Use. Instead genuinely create real users via the cognito flow
        @param scale -> desired number of users to exist in table
        '''

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
        '''
        Generates fake customers and inserts into customers table
        @param scale -> desired number of customers to exist in table
        '''

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

    def generate_ticket_events(scale=400, customers=[]):
        '''
        Generates new Ticket Events. Randomizes generation of pickup tickets and delivery tickets
        @param scale -> desired number of ticket events to exist in table
        @param customers -> list of customers found in customer table
        '''

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
                creator_userID = MANAGER_USER if APPROVER_ONLY_SELF else random.choice(usersByTypeList[UserType.manager])
                customerName = customers[random.randrange(0, len(customers))].name
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
                isPickup = random.choice([False, True])
                noSignatureRequired = False
                tailgateAuthorized = False

                obj = ticket_events_controller._create_base_event(
                    {
                        "userId": creator_userID,
                        "customerName": customerName,
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

    def list_diff(li1, li2):
        '''
        Returns a list which is the set difference between 2 lists.
        '''
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
                curr_approver = curr_approver if curr_approver != null and len(approver_list) < 2 and random.randrange(2) == 0 else random.choice(approver_list)
                curr_driver = random.choice(usersByTypeList[UserType.driver])
                data = {
                    "ticketId" : ticket,
                    "newStatus" : curr_state,
                    "oldStatus" : prev_state,
                    "requesterUserId" : curr_approver,
                    "requestedUserId" : curr_driver
                    }

            elif milestone_type == "Inventory_Milestone_Status":
                curr_approver = curr_approver if curr_approver != null and len(approver_list) < 2 and random.randrange(2) == 0 else random.choice(approver_list)
                data = {
                    "ticketId" : ticket,
                    "newStatus" : curr_state,
                    "oldStatus" : prev_state,
                    "approvedByUserId" : curr_approver
                    }
            
            elif milestone_type == "Assignment_Milestone_Status":
                curr_approver = curr_approver if curr_approver != null and len(approver_list) < 2 and random.randrange(2) == 0 else random.choice(approver_list)
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
    
    def generate_milestone_events(old_tickets, curr_user_only=True):
        '''
        Iterates over all newly generated tickets by this run of the test class and
        applies state transitions on them in a semirandom fashion which adheres to the
        state transition constraints defined in statetable in milestones constants.

        @param old_tickets -> list of old tickets. Data in the form of tuples [(ticketId, isPickup)]
        @param curr_user_only -> boolean value of if only MANAGER_USER should be used as approver
        '''

        # Fetch all existing tickets
        all_tickets = (
            session.query(TicketEvents)
            .with_entities(TicketEvents.ticketId, TicketEvents.isPickup)
            .distinct()
            .all()
        )

        # Segregate newly generated pickup tickets and delivery tickets
        new_tickets = list_diff(all_tickets, old_tickets)
        pickup_tickets = [v for v,p in new_tickets if p]
        delivery_tickets = [v for v,p in new_tickets if not p]

        reprocess_pickups = []
        reprocess_deliveries = []

        approver_list = usersByTypeList[UserType.manager] + usersByTypeList[UserType.dispatch]
        if curr_user_only:
            approver_list = [MANAGER_USER]

        # Iterate over all new pickup tickets and generate state transitions (milestones)
        for ticket in pickup_tickets:
            end_state = random.choice(pickupMilestones)
            transition_list = (
                random.choice(list(stateTable[end_state].values())) 
                if type(stateTable[end_state]) is dict
                else stateTable[end_state]
            )
            generate_transitions(ticket, transition_list, approver_list, Pickup_Milestone_Status.unassigned_pickup.value)
            if len(transition_list) > 0 and transition_list[-1] == Pickup_Milestone_Status.unassigned_pickup:
                reprocess_pickups.append((ticket, 1))
        
        # Iterate over all new delivery tickets and generate state transitions (milestones)
        for ticket in delivery_tickets:
            end_state = random.choice(deliveryMilestones)
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
            if (len(transition_list) > 1 and transition_list[-1] == Inventory_Milestone_Status.checked_into_inventory 
                and transition_list[-2] != Creation_Milestone_Status.ticket_created):
                reprocess_deliveries.append((ticket, 1))

        # Iterate over all pickup tickets that happened to land back into a 'start' state (failure route)
        # and once again generate state transitions (milestones) for a second pass through the system
        while reprocess_pickups:
            ticket, retry = reprocess_pickups.pop(0)
            end_state = random.choice(pickupMilestones)
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

        # Iterate over all delivery tickets that happened to land back into a 'start' state (failure route)
        # and once again generate state transitions (milestones) for a second pass through the system
        while reprocess_deliveries:
            ticket, retry = reprocess_deliveries.pop(0)
            end_state = random.choice(deliveryMilestones)
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



    ################################################################################################
    ################################ MAIN SECTION OF CODE BEGIN ####################################
    ################################################################################################


    # Get all Users in Database
    # If you haven't run the sync tool yet found in dev-tools folder, run that first
    users = session.query(Users).with_entities(Users.userId, Users.userType).all()

    # each entry in list is tuple ("userid", "usertype")
    # Building up User by Type Dictionary
    for user in users:
        usersByTypeList[UserType(user[1])].append(user[0])

    
    # Generating Fake Customers. Customers are Businesses. 
    # These Customers are not added to the Users Table
    generate_customers(GENERATE_CUSTOMERS)
    customers = session.query(Customers).all()

    # Fetch Old Tickets so as not to make state Transitions for Already processed existing tickets
    # Fetch here before creating new tickets
    oldTickets = (
            session.query(TicketEvents)
            .with_entities(TicketEvents.ticketId, TicketEvents.isPickup)
            .distinct()
            .all()
        )

    # Generate new tickets where num_new_tickets = (scale - |Old Tickets|)
    # Has a bunch of fake data, but uses customers in customer table and real Users as creator
    # Sets userID to the MANAGER_USER constant if APPROVER_ONLY_SELF = True, otherwise it randomizes
    # over available Manager Type Users
    generate_ticket_events(
        scale=GENERATE_TICKET_EVENTS,
        customers=customers,
    )
    ticketEvents = session.query(TicketEvents).distinct().all()

    # Programatically apply state transitions according to statetable constraints to generate milestone events
    generate_milestone_events(oldTickets, APPROVER_ONLY_SELF)
    exit()
