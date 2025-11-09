from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, date
from typing import Optional, TYPE_CHECKING
from decimal import Decimal
from enum import Enum

if TYPE_CHECKING:
    from .user import User
    from .category import Category
    from .account import Account
    from .transaction import Transaction


class Frequency(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"


# Recurring Transaction Template
class RecurringBase(SQLModel):
    name: str = Field(max_length=255)
    type: str = Field(max_length=50)
    description: Optional[str] = None
    frequency: Frequency
    interval: int = Field(default=1, ge=1)
    start_date: date
    end_date: Optional[date] = None
    is_active: bool = Field(default=True)


class Recurring(RecurringBase, table=True):
    __tablename__ = "recurring" # type: ignore
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    category_id: Optional[int] = Field(default=None, foreign_key="categories.id")
    next_date: Optional[date] = None
    last_date: Optional[date] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    user: "User" = Relationship(back_populates="recurring")
    category: Optional["Category"] = Relationship()
    lines: list["RecurringLine"] = Relationship(back_populates="recurring", cascade_delete=True)
    transactions: list["Transaction"] = Relationship(back_populates="recurring")


# Recurring Line Template
class RecurringLineBase(SQLModel):
    type: str = Field(max_length=10)  # Debit/Credit
    amount: Decimal = Field(ge=0, max_digits=15, decimal_places=2)
    description: Optional[str] = None


class RecurringLine(RecurringLineBase, table=True):
    __tablename__ = "recurring_lines" # type: ignore
    
    id: Optional[int] = Field(default=None, primary_key=True)
    recurring_id: int = Field(foreign_key="recurring.id", index=True)
    account_id: int = Field(foreign_key="accounts.id", index=True)
    
    # Relationships
    recurring: Recurring = Relationship(back_populates="lines")
    account: "Account" = Relationship(back_populates="recurring_lines")


# Create schemas
class RecurringLineCreate(RecurringLineBase):
    account_id: int


class RecurringCreate(RecurringBase):
    user_id: int
    category_id: Optional[int] = None
    lines: list[RecurringLineCreate]


# Read schemas
class RecurringLineRead(RecurringLineBase):
    id: int
    recurring_id: int
    account_id: int


class RecurringRead(RecurringBase):
    id: int
    user_id: int
    category_id: Optional[int]
    next_date: Optional[date]
    last_date: Optional[date]
    created_at: datetime
    updated_at: datetime
    lines: list[RecurringLineRead] = []


# Update schemas
class RecurringUpdate(SQLModel):
    name: Optional[str] = None
    type: Optional[str] = None
    category_id: Optional[int] = None
    description: Optional[str] = None
    frequency: Optional[Frequency] = None
    interval: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_active: Optional[bool] = None