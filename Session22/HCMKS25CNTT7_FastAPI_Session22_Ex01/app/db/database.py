"""db/database.py"""

import pymysql
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:12345678@localhost:3306/devConnect_db"

temp_conn = pymysql.connect(user="root", host="localhost", password="12345678")

try:
    with temp_conn.cursor() as cursor:
        cursor.execute("CREATE DATABASE IF NOT EXISTS devConnect_db")
finally:
    cursor.close()

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
