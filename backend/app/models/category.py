from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from enum import Enum

if TYPE_CHECKING:
    from .user import User
    from .transaction import Transaction
    from .budget import Budget


class CategoryType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"


class CategoryBase(SQLModel):
    name: str = Field(max_length=255)
    type: CategoryType
    icon: Optional[str] = Field(default=None, max_length=50)
    color: Optional[str] = Field(default=None, max_length=7)


class Category(CategoryBase, table=True):
    __tablename__ = "categories" # type: ignore
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    parent_id: Optional[int] = Field(default=None, foreign_key="categories.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    user: "User" = Relationship(back_populates="categories")
    parent: Optional["Category"] = Relationship(
        back_populates="children",
        sa_relationship_kwargs={"remote_side": "Category.id"}
    )
    children: list["Category"] = Relationship(back_populates="parent")
    transactions: list["Transaction"] = Relationship(back_populates="category")
    budgets: list["Budget"] = Relationship(back_populates="category")


class CategoryCreate(CategoryBase):
    user_id: int
    parent_id: Optional[int] = None


class CategoryRead(CategoryBase):
    id: int
    user_id: int
    parent_id: Optional[int]
    created_at: datetime


class CategoryUpdate(SQLModel):
    name: Optional[str] = None
    type: Optional[CategoryType] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    parent_id: Optional[int] = None