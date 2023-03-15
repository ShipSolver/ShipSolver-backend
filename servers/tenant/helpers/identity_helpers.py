from flask import session
import os
import boto3
from botocore.config import Config

class IdentityHelper:

    @staticmethod
    def get_logged_in_userId():
        claims = session.get("claims")
        if claims and "sub" in claims:
            return claims["sub"]
        return None

    @staticmethod
    def get_cognito_users():
        cognito_users = []

        my_config = Config(
            region_name = os.getenv("AWS_REGION"),
            signature_version = 'v4',
            retries = {
                'max_attempts': 10,
                'mode': 'standard'
            }
        )

        client = boto3.client('cognito-idp', config=my_config, 
            aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        )

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
                cognito_users.append(
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
        
        return cognito_users