from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, date
from typing import Optional, TYPE_CHECKING
from decimal import Decimal
from enum import Enum

if TYPE_CHECKING:
    from .user import User
    from .category import Category
    from .account import Account
    from .recurring import Recurring
    from .attachment import Attachment


class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"
    TRANSFER = "transfer"
    ADJUSTMENT = "adjustment"


class LineType(str, Enum):
    DEBIT = "Debit"
    CREDIT = "Credit"


# Transaction Header
class TransactionBase(SQLModel):
    date: date
    type: TransactionType
    description: Optional[str] = None
    reference: Optional[str] = Field(default=None, max_length=100)
    notes: Optional[str] = None
    is_posted: bool = Field(default=True)


class Transaction(TransactionBase, table=True):
    __tablename__ = "transactions" # type: ignore
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    number: Optional[str] = Field(default=None, max_length=50)
    category_id: Optional[int] = Field(default=None, foreign_key="categories.id")
    recurring_id: Optional[int] = Field(default=None, foreign_key="recurring.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    user: "User" = Relationship(back_populates="transactions")
    category: Optional["Category"] = Relationship(back_populates="transactions")
    recurring: Optional["Recurring"] = Relationship(back_populates="transactions")
    lines: list["TransactionLine"] = Relationship(back_populates="transaction", cascade_delete=True)
    attachments: list["Attachment"] = Relationship(back_populates="transaction", cascade_delete=True)


# Transaction Line (Debit/Credit)
class TransactionLineBase(SQLModel):
    type: LineType
    amount: Decimal = Field(ge=0, max_digits=15, decimal_places=2)
    description: Optional[str] = None


class TransactionLine(TransactionLineBase, table=True):
    __tablename__ = "transaction_lines" # type: ignore
    
    id: Optional[int] = Field(default=None, primary_key=True)
    transaction_id: int = Field(foreign_key="transactions.id", index=True)
    account_id: int = Field(foreign_key="accounts.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    transaction: Transaction = Relationship(back_populates="lines")
    account: "Account" = Relationship(back_populates="transaction_lines")


# Create schemas
class TransactionLineCreate(TransactionLineBase):
    account_id: int


class TransactionCreate(TransactionBase):
    user_id: int
    category_id: Optional[int] = None
    lines: list[TransactionLineCreate]


# Read schemas
class TransactionLineRead(TransactionLineBase):
    id: int
    transaction_id: int
    account_id: int
    created_at: datetime


class TransactionRead(TransactionBase):
    id: int
    user_id: int
    number: Optional[str]
    category_id: Optional[int]
    recurring_id: Optional[int]
    created_at: datetime
    updated_at: datetime
    lines: list[TransactionLineRead] = []


# Update schemas
class TransactionLineUpdate(SQLModel):
    account_id: Optional[int] = None
    type: Optional[LineType] = None
    amount: Optional[Decimal] = None
    description: Optional[str] = None


class TransactionUpdate(SQLModel):
    date: Optional[date] = None
    type: Optional[TransactionType] = None
    category_id: Optional[int] = None
    description: Optional[str] = None
    reference: Optional[str] = None
    notes: Optional[str] = None
    is_posted: Optional[bool] = None