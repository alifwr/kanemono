from typing import Union, Annotated
from sqlmodel import Session
from fastapi import Depends, FastAPI

from app.services.database import create_db_and_tables
from app.routes.user_route import router as user_router

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(user_router, prefix="/api")