import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_port = os.getenv("DB_PORT", "5432")
db_name = os.getenv("DB_NAME", "tenant_db")
db_username = os.getenv("DB_USERNAME", "postgres")
db_password = os.getenv("DB_PASSWORD", "password")

# TODO REMOVE
aws_access_key_id = os.getenv("aws_access_key_id")
aws_secret_access_key = os.getenv("aws_secret_access_key")
tenant = os.getenv("TENANT")
db_url = os.getenv("DB_URL", "ship-solver.ccxmktobiszx.ca-central-1.rds.amazonaws.com")
# db_url = os.getenv("DB_URL", "localhost")

cnx_string = f"postgresql://{db_username}:{db_password}@{db_url}:{db_port}/{db_name}"


Base = declarative_base()
engine = create_engine(cnx_string, echo=False)
print("connecting to db....")
Session = sessionmaker(bind=engine)
session = Session()
