from sqlmodel import create_engine, Session, SQLModel
from typing import Generator

# Database URL - adjust as needed
DATABASE_URL = "postgresql://username:password@localhost:5432/accounting_db"

# Create engine
engine = create_engine(DATABASE_URL, echo=True)

# Dependency for database sessions
def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

# Create all tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)