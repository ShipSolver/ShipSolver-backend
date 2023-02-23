import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_port = os.getenv("DB_PORT", "5432")
db_name = os.getenv("DB_NAME", "tenant_db")
db_username = os.getenv("DB_USERNAME", "postgres")
db_password = os.getenv("DB_PASSWORD", "postgres")
db_url = os.getenv("DB_URL", "postgres_c")

cnx_string = f"postgresql://{db_username}:{db_password}@{db_url}:{db_port}/{db_name}"


Base = declarative_base()
engine = create_engine(cnx_string, echo=False)
print("connecting to db....")
Session = sessionmaker(bind=engine)
session = Session()
