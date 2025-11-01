from typing import TYPE_CHECKING, Optional, Dict, Any
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy import JSON

if TYPE_CHECKING:
    from .user import User
    from ..services.service import Service

class UserService(SQLModel, table=True):
    __tablename__ = "user_service"
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", ondelete="CASCADE")
    service_id: int = Field(foreign_key="service.id", ondelete="CASCADE")
    access_token: str
    refresh_token: Optional[str] = None
    service_metadata: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))

    user: "User" = Relationship(back_populates="services")
    service: "Service" = Relationship(back_populates="users")
