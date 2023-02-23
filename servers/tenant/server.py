import os
import ssl
from flask import Flask, Blueprint, jsonify, session
from flask_session import Session
from config import app
from blueprints.event_driven.ticket import ticket_bp
from blueprints.simple.customers import customer_bp
from blueprints.simple.users import user_bp
from blueprints.simple.milestones import milestone_bp
from blueprints.simple.driver import driver_bp
from blueprints.simple.document import document_bp

# Module import to create global controller instances
import controllers as Controllers

from flask_cors import CORS
from flask_cognito_lib import CognitoAuth
from flask_caching import Cache

# from models.__init__ import engine, Base
# from models.models import INDEXES
from dotenv import load_dotenv

ssl._create_default_https_context = ssl._create_unverified_context

load_dotenv("tenant/.env", override=True)

cache_config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}
cache = Cache(app)

app.config["AWS_REGION"] = os.environ["AWS_REGION"]
app.config["AWS_COGNITO_USER_POOL_ID"] = os.environ["AWS_COGNITO_USER_POOL_ID"]
app.config["AWS_COGNITO_USER_POOL_CLIENT_ID"] = os.environ["AWS_COGNITO_USER_POOL_CLIENT_ID"]
app.config["AWS_COGNITO_DOMAIN"] = os.environ["AWS_COGNITO_DOMAIN"]
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

auth = CognitoAuth(app)
ses = Session(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

parent = Blueprint("api", __name__, url_prefix="/api")
parent.register_blueprint(ticket_bp)
parent.register_blueprint(customer_bp)
parent.register_blueprint(user_bp)
parent.register_blueprint(milestone_bp)
parent.register_blueprint(driver_bp)
parent.register_blueprint(document_bp)

# @app.errorhandler(Exception)
# def handle_exception(e):
#     print('\033[91m' + "===> An Exception Occurred") # red color
#     print(e)
#     print('\033[0m') # end color
#     return jsonify(
#         exception_type=e.__class__.__name__,
#         exception_string=str(e)
#     ), 500

if __name__ == "__main__":

    print("REGISTERING BLUEPRINT")
    app.register_blueprint(parent)

    app.run(debug=True, host="0.0.0.0", port=6767)
