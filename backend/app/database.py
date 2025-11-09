from sqlmodel import create_engine, Session, SQLModel, text
from typing import Generator
from app.core.config import settings

# Create database engine
# echo=True will print all SQL queries (useful for debugging, disable in production)
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # Show SQL queries in console when DEBUG=True
    pool_pre_ping=True,   # Verify connections before using them
    pool_size=10,         # Number of connections to keep in pool
    max_overflow=20       # Maximum overflow connections
)


def create_db_and_tables():
    """
    Create all database tables based on SQLModel models
    This should be called on application startup
    """
    # Import all models here to ensure they are registered with SQLModel
    from app.models.user import User
    from app.models.account import Account
    from app.models.category import Category
    from app.models.transaction import Transaction, TransactionLine
    from app.models.recurring import Recurring, RecurringLine
    from app.models.attachment import Attachment
    from app.models.budget import Budget
    
    # Create all tables
    SQLModel.metadata.create_all(engine)
    print("✅ Database tables created successfully!")


def get_session() -> Generator[Session, None, None]:
    """
    Dependency function to get database session
    Usage in FastAPI endpoints: session: Session = Depends(get_session)
    """
    with Session(engine) as session:
        yield session


def drop_all_tables():
    """
    Drop all database tables
    WARNING: This will delete all data!
    Only use this in development/testing
    """
    SQLModel.metadata.drop_all(engine)
    print("⚠️ All database tables dropped!")


def reset_database():
    """
    Drop and recreate all tables
    WARNING: This will delete all data!
    Only use this in development/testing
    """
    drop_all_tables()
    create_db_and_tables()
    print("🔄 Database reset complete!")


# Optional: Initialize database with seed data
def seed_database():
    """
    Seed database with initial data
    This can be called after create_db_and_tables()
    """
    from app.models.user import User
    from app.core.security import hash_password
    
    with Session(engine) as session:
        # Check if any users exist
        from sqlmodel import select
        statement = select(User)
        existing_users = session.exec(statement).first()
        
        if not existing_users:
            # Create a demo user
            demo_user = User(
                email="demo@example.com",
                name="Demo User",
                password_hash=hash_password("demo123456")
            )
            session.add(demo_user)
            session.commit()
            print("✅ Demo user created: demo@example.com / demo123456")


# Test database connection
def test_connection():
    """
    Test database connection
    """
    try:
        with Session(engine) as session:
            # Try to execute a simple query
            session.execute(text("SELECT 1"))
            print("✅ Database connection successful!")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False