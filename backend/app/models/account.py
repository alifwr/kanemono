from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from decimal import Decimal
from enum import Enum

if TYPE_CHECKING:
    from .user import User
    from .transaction import TransactionLine
    from .recurring import RecurringLine
    from .budget import Budget


class AccountType(str, Enum):
    ASSET = "Asset"
    LIABILITY = "Liability"
    EQUITY = "Equity"
    REVENUE = "Revenue"
    EXPENSE = "Expense"


class NormalBalance(str, Enum):
    DEBIT = "Debit"
    CREDIT = "Credit"


class AccountBase(SQLModel):
    code: str = Field(max_length=20, index=True)
    name: str = Field(max_length=255)
    type: AccountType
    subtype: Optional[str] = Field(default=None, max_length=50)
    normal_balance: NormalBalance
    description: Optional[str] = None
    is_active: bool = Field(default=True)


class Account(AccountBase, table=True):
    __tablename__ = "accounts" # type: ignore
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    parent_id: Optional[int] = Field(default=None, foreign_key="accounts.id")
    balance: Decimal = Field(default=Decimal("0.00"), max_digits=15, decimal_places=2)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    user: "User" = Relationship(back_populates="accounts")
    parent: Optional["Account"] = Relationship(
        back_populates="children",
        sa_relationship_kwargs={"remote_side": "Account.id"}
    )
    children: list["Account"] = Relationship(back_populates="parent")
    transaction_lines: list["TransactionLine"] = Relationship(back_populates="account")
    recurring_lines: list["RecurringLine"] = Relationship(back_populates="account")
    budgets: list["Budget"] = Relationship(back_populates="account")


class AccountCreate(AccountBase):
    user_id: int
    parent_id: Optional[int] = None


class AccountRead(AccountBase):
    id: int
    user_id: int
    parent_id: Optional[int]
    balance: Decimal
    created_at: datetime
    updated_at: datetime


class AccountUpdate(SQLModel):
    code: Optional[str] = None
    name: Optional[str] = None
    type: Optional[AccountType] = None
    subtype: Optional[str] = None
    normal_balance: Optional[NormalBalance] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    parent_id: Optional[int] = None