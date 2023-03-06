import os
import ssl
from flask import Flask, Blueprint, jsonify, session, g
from flask_session import Session
from config import app
from blueprints.event_driven.ticket import ticket_bp
from blueprints.simple.customers import customer_bp
from blueprints.simple.users import user_bp
from blueprints.simple.milestones import milestone_bp
from blueprints.simple.driver import driver_bp
from blueprints.simple.document import document_bp
from sqlalchemy.exc import IllegalStateChangeError
from sqlalchemy.orm import close_all_sessions

# Module import to create global controller instances
import controllers as Controllers

from flask_cors import CORS
from flask_cognito_lib import CognitoAuth

# from models.__init__ import engine, Base
import models
import atexit
from dotenv import load_dotenv

ssl._create_default_https_context = ssl._create_unverified_context

load_dotenv("tenant/.env", override=True)


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


@app.errorhandler(Exception)
def handle_sqlAlch_isce_exception(e: Exception):
    sql_session = models.session
    if 'sql_session' in g:
            sql_session = g.sql_session
    if sql_session:
        sql_session.rollback()
        sql_session.close()
    models.engine.dispose()
    raise(e)
    return jsonify(
        exception_type=e.__class__.__name__,
        exception_string="Invalid State Change Error"
    ), 500

@app.teardown_appcontext
def teardown_db(exception):
    print("App Context Dispose")
    sql_session = g.pop('sql_session', None)

    if sql_session is not None:
        sql_session.commit()
        sql_session.close()
        models.engine.dispose()

def atExitHandler():
    print("Running Exit Handler")
    if models.session:
        models.session.commit()
        models.session.close()
    close_all_sessions()
    models.engine.dispose()

def startupCleanupHandler():
    print("Running Startup Cleanup Handler")
    models.session.commit()
    models.session.close()
    # Will not be using the global sql_alchemy session beyond this point. Set to null.
    models.session = None
    models.engine.dispose()

if __name__ == "__main__":

    print("REGISTERING BLUEPRINT")
    app.register_blueprint(parent)

    # Register exit handler to cleanly close sql alchemy session
    atexit.register(atExitHandler)
    startupCleanupHandler()

    app.run(debug=True, host="0.0.0.0", port=6767)
