from config import app
from blueprints.advanced.ticket import ticket_bp
from blueprints.basic.customers import customer_bp
from blueprints.basic.users import user_bp
from blueprints.pdf import pdf_bp

# from models.__init__ import engine, Base
# from models.models import INDEXES
from flask import Blueprint
from dotenv import load_dotenv

load_dotenv(".env", override=True)

parent = Blueprint("api", __name__, url_prefix="/api")
parent.register_blueprint(pdf_bp)
parent.register_blueprint(ticket_bp)
parent.register_blueprint(customer_bp)
parent.register_blueprint(user_bp)


# @app.before_first_request
# def instantiate_database():  # creates tables and indexes from models if not instantiated
#     try:
#         # create indexes
#         for index in INDEXES:
#             index.create(bind=engine)
#     except:
#         pass

#     # create all tables
#     Base.metadata.create_all(engine)


@app.route("/")
def hello_world():
    return "Server Started!"


if __name__ == "__main__":

    print("REGISTERING BLUEPRINT")
    app.register_blueprint(parent)

    app.run(debug=False, host="0.0.0.0", port=6767)
