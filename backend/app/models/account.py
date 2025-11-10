from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from decimal import Decimal
from enum import Enum
from pydantic import field_validator

if TYPE_CHECKING:
    from .user import User
    from .transaction import TransactionLine
    from .recurring import RecurringLine
    from .budget import Budget


# ============================================
# ENUMS
# ============================================

class AccountType(str, Enum):
    ASSET = "Asset"
    LIABILITY = "Liability"
    EQUITY = "Equity"
    REVENUE = "Revenue"
    EXPENSE = "Expense"


class NormalBalance(str, Enum):
    DEBIT = "Debit"
    CREDIT = "Credit"


# ============================================
# BASE & TABLE MODEL
# ============================================

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


# ============================================
# API SCHEMAS
# ============================================

class AccountCreate(AccountBase):
    """Schema for creating a new account"""
    parent_id: Optional[int] = Field(None, description="Parent account ID for hierarchy")
    
    @field_validator('code')
    def validate_code_format(cls, v):
        if not v.isdigit():
            raise ValueError('Account code must contain only digits')
        if len(v) < 4:
            raise ValueError('Account code must be at least 4 digits')
        return v


class AccountUpdate(SQLModel):
    """Schema for updating an account"""
    code: Optional[str] = Field(None, max_length=20)
    name: Optional[str] = Field(None, max_length=255)
    type: Optional[AccountType] = None
    subtype: Optional[str] = Field(None, max_length=50)
    normal_balance: Optional[NormalBalance] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    parent_id: Optional[int] = None


class AccountRead(AccountBase):
    """Schema for account response"""
    id: int
    user_id: int
    parent_id: Optional[int]
    balance: Decimal
    created_at: datetime
    updated_at: datetime
    
    # class Config:
    #     from_attributes = True


class AccountDetail(AccountRead):
    """Schema for detailed account view with relationships"""
    parent: Optional[AccountRead] = None
    children: List[AccountRead] = []
    
    # class Config:
    #     from_attributes = True


class AccountTree(SQLModel):
    """Schema for hierarchical account tree"""
    id: int
    code: str
    name: str
    type: AccountType
    balance: Decimal
    is_active: bool
    children: List['AccountTree'] = []
    
    # class Config:
    #     from_attributes = True


class AccountListResponse(SQLModel):
    """Schema for paginated account list"""
    total: int
    page: int
    page_size: int
    accounts: List[AccountRead]


class AccountSummary(SQLModel):
    """Schema for account statistics summary"""
    total_accounts: int
    assets_count: int
    liabilities_count: int
    equity_count: int
    revenue_count: int
    expense_count: int
    total_assets: Decimal
    total_liabilities: Decimal
    total_equity: Decimal
    total_revenue: Decimal
    total_expenses: Decimal