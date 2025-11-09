from fastapi import FastAPI
from app.database import create_db_and_tables
from app.models import *  # Import all models to register them

app = FastAPI(title="Accounting API", version="1.0.0")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def root():
    return {"message": "Accounting API is running"}

# Import routers here later
# from app.routers import users, accounts, transactions
# app.include_router(users.router)
# app.include_router(accounts.router)
# app.include_router(transactions.router)