from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from pydantic import EmailStr

if TYPE_CHECKING:
    from .account import Account
    from .category import Category
    from .transaction import Transaction
    from .recurring import Recurring
    from .budget import Budget


# ============================================
# BASE & TABLE MODEL
# ============================================

class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    name: str = Field(max_length=255)


class User(UserBase, table=True):
    __tablename__ = "users" # type: ignore
    
    id: Optional[int] = Field(default=None, primary_key=True)
    password_hash: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    accounts: list["Account"] = Relationship(back_populates="user", cascade_delete=True)
    categories: list["Category"] = Relationship(back_populates="user", cascade_delete=True)
    transactions: list["Transaction"] = Relationship(back_populates="user", cascade_delete=True)
    recurring: list["Recurring"] = Relationship(back_populates="user", cascade_delete=True)
    budgets: list["Budget"] = Relationship(back_populates="user", cascade_delete=True)


# ============================================
# API SCHEMAS
# ============================================

class UserCreate(UserBase):
    """Schema for user registration"""
    password: str = Field(min_length=8, max_length=128)


class UserRead(UserBase):
    """Schema for user profile response"""
    id: int
    created_at: datetime
    updated_at: datetime


class UserUpdate(SQLModel):
    """Schema for updating user profile"""
    email: Optional[EmailStr] = None
    name: Optional[str] = None


class UserLogin(SQLModel):
    """Schema for login request"""
    email: EmailStr
    password: str = Field(max_length=128)


class TokenResponse(SQLModel):
    """Schema for token response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(SQLModel):
    """Schema for refresh token request"""
    refresh_token: str


class ChangePasswordRequest(SQLModel):
    """Schema for changing password"""
    current_password: str = Field(max_length=128)
    new_password: str = Field(min_length=8, max_length=128)


class UserProfile(SQLModel):
    """Schema for user profile (alias for UserRead)"""
    id: int
    email: str
    name: str