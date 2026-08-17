"""main.py"""

from app.db.database import Base, engine
from fastapi import FastAPI
from app.router import auth

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
