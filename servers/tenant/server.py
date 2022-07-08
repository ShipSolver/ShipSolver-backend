<<<<<<< HEAD
import os
from flask import Flask, Blueprint, jsonify, session
# from config import app
=======
from tenant.config import app
>>>>>>> Fixed celery pipeline
from blueprints.event_driven.ticket import ticket_bp
from blueprints.simple.customers import customer_bp
from blueprints.simple.users import user_bp
<<<<<<< HEAD
<<<<<<< HEAD
from blueprints.simple.milestones import milestone_bp
from blueprints.simple.driver import driver_bp

from flask_cors import CORS
from flask_cognito_lib import CognitoAuth
=======
from servers.tenant.blueprints.simple.pdf import pdf_bp  # TODO: Move this in seperate microservice
>>>>>>> modifying db schema
=======
from flask_cors import cross_origin
<<<<<<< HEAD
from servers.tenant.blueprints.simple.document import pdf_bp  # TODO: Move this in seperate microservice
>>>>>>> Stefan codeazzzzzzzzzzzzzzzzzzzzzzzzzzzz

# from models.__init__ import engine, Base
# from models.models import INDEXES
=======
from tenant.blueprints.simple.document import document_bp  # TODO: Move this in seperate microservice
from flask import Blueprint
>>>>>>> Fixed celery pipeline
from dotenv import load_dotenv

load_dotenv(".env", override=True)

app = Flask(__name__)

app.config["AWS_REGION"] = os.environ["AWS_REGION"]
app.config["AWS_COGNITO_USER_POOL_ID"] = os.environ["AWS_COGNITO_USER_POOL_ID"]
app.config["AWS_COGNITO_USER_POOL_CLIENT_ID"] = os.environ["AWS_COGNITO_USER_POOL_CLIENT_ID"]
app.config["AWS_COGNITO_DOMAIN"] = os.environ["AWS_COGNITO_DOMAIN"]

auth = CognitoAuth(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

parent = Blueprint("api", __name__, url_prefix="/api")
<<<<<<< HEAD
=======
parent.register_blueprint(document_bp)
>>>>>>> Fixed celery pipeline
parent.register_blueprint(ticket_bp)
parent.register_blueprint(customer_bp)
parent.register_blueprint(user_bp)
parent.register_blueprint(milestone_bp)
parent.register_blueprint(driver_bp)


<<<<<<< HEAD
=======

@app.route("/")
def hello_world():
    return "Server Started!"

>>>>>>> Fixed celery pipeline

if __name__ == "__main__":

    print("REGISTERING BLUEPRINT")
    app.register_blueprint(parent)

    app.run(debug=True, host="0.0.0.0", port=5000)
