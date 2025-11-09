from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .transaction import Transaction


class AttachmentBase(SQLModel):
    name: str = Field(max_length=255)
    path: str = Field(max_length=500)
    type: Optional[str] = Field(default=None, max_length=50)
    size: Optional[int] = None


class Attachment(AttachmentBase, table=True):
    __tablename__ = "attachments" # type: ignore
    
    id: Optional[int] = Field(default=None, primary_key=True)
    transaction_id: int = Field(foreign_key="transactions.id", index=True)
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    transaction: "Transaction" = Relationship(back_populates="attachments")


class AttachmentCreate(AttachmentBase):
    transaction_id: int


class AttachmentRead(AttachmentBase):
    id: int
    transaction_id: int
    uploaded_at: datetime


class AttachmentUpdate(SQLModel):
    name: Optional[str] = None