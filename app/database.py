# basicaly followed FastAPI's guide to connect with SQl
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

SQLALCHEMY_DATABASE_URL = {settings.database_url}

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# this is the base model that we will extend to create our own models(tables)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# # Used if we want to talk to the database using raw SQL
# # try helps to connect with the database incase the connection falls off
# # cursor_factory is used to get the name od the colms bcuz by default colm number in returned.
# while True:
#     try:
#         conn = psycopg2.connect(host='127.0.0.1', database='social_media_api',
#                                 user='postgres', password='Pranit1234', cursor_factory=RealDictCursor)
#         # cursor is the one that actually executes the code
#         cursor = conn.cursor()
#         print("Database connection was successful")
#         break

#     # we are storing the error in the error var
#     except Exception as error:
#         print("Connection to database failed")
#         print("Error: ", error)
#         time.sleep(2)