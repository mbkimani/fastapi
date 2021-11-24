import psycopg2
from psycopg2.extras import RealDictCursor
import time

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

#create dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#connect to database
# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='Th3B3st.', cursor_factory=RealDictCursor) 
#         cursor = conn.cursor()
#         print("database connection was successful")
#         break;
#     except Exception as error:
#         print("connection failed. error was: ", error)
#         time.sleep(5)