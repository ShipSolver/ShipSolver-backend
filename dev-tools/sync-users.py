from dotenv import load_dotenv
load_dotenv(".env", override=True)

import os
import sys
import json
import boto3
from botocore.config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/servers/tenant"
print(BASE_PATH)
sys.path.append(BASE_PATH)

from controllers.controllerMapper import UserController
from models.models import Users, UserType

my_config = Config(
    region_name = os.getenv("AWS_REGION"),
    signature_version = 'v4',
    retries = {
        'max_attempts': 10,
        'mode': 'standard'
    }
)

client = boto3.client('cognito-idp', config=my_config)

db_port = os.getenv("DB_PORT", "5432")
db_name = os.getenv("DB_NAME", "tenant_db")
db_username = os.getenv("DB_USERNAME", "postgres")
db_password = os.getenv("DB_PASSWORD", "postgres")
db_url = os.getenv("DB_URL", "localhost")

cnx_string = f"postgresql://{db_username}:{db_password}@{db_url}:{db_port}/{db_name}"

engine = create_engine(cnx_string, echo=False)
print("connecting to db....")
Session = sessionmaker(bind=engine)
session = Session()

sync_users = []

list_users_args = {
    'UserPoolId': os.getenv("AWS_COGNITO_USER_POOL_ID"),
    'AttributesToGet': [
        'email',
        'name',
        'phone_number',
        'sub',
        'custom:UserType',
    ],
    'Limit': 2
}

# Get users from cognito
pagination = True
while pagination:
    response = client.list_users(**list_users_args)
    if "PaginationToken" in response:
        list_users_args["PaginationToken"] = response["PaginationToken"]
    else:
        pagination = False

    for user_res in response['Users']:
        usr = {}
        for att in user_res["Attributes"]:
            usr[att['Name']] = att["Value"]
        first_name = usr["name"].split(" ")[0]
        last_name = "" if len(usr["name"].split(" ")) < 2 else usr["name"].split(" ")[1]
        sync_users.append(
            {
                "userId": usr["sub"],
                "userType": usr["custom:UserType"],
                "username": usr["email"],
                "firstName": first_name,
                "lastName": last_name,
                "email": usr["email"],
                "createdAt": user_res["UserCreateDate"].strftime('%s'),
                "modifiedAt": user_res["UserLastModifiedDate"].strftime('%s')
            }
        )

user_controller = UserController()
inserted = user_controller._create_bulk(sync_users)

print(f"Successfully Synchronised {len(inserted)} Users.")
