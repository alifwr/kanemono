from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, date
from typing import Optional, TYPE_CHECKING
from decimal import Decimal
from enum import Enum

if TYPE_CHECKING:
    from .user import User
    from .account import Account
    from .category import Category


class Period(str, Enum):
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"


class BudgetBase(SQLModel):
    amount: Decimal = Field(ge=0, max_digits=15, decimal_places=2)
    period: Period
    start_date: date
    end_date: Optional[date] = None
    is_active: bool = Field(default=True)


class Budget(BudgetBase, table=True):
    __tablename__ = "budgets" # type: ignore
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    account_id: int = Field(foreign_key="accounts.id", index=True)
    category_id: Optional[int] = Field(default=None, foreign_key="categories.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    user: "User" = Relationship(back_populates="budgets")
    account: "Account" = Relationship(back_populates="budgets")
    category: Optional["Category"] = Relationship(back_populates="budgets")


class BudgetCreate(BudgetBase):
    user_id: int
    account_id: int
    category_id: Optional[int] = None


class BudgetRead(BudgetBase):
    id: int
    user_id: int
    account_id: int
    category_id: Optional[int]
    created_at: datetime
    updated_at: datetime


class BudgetUpdate(SQLModel):
    amount: Optional[Decimal] = None
    period: Optional[Period] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_active: Optional[bool] = None
    account_id: Optional[int] = None
    category_id: Optional[int] = None