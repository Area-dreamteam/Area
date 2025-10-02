from typing import TYPE_CHECKING, List, Optional
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .user import User
    from ..services.service import Service

class UserService(SQLModel, table=True):
    __tablename__ = "user_service"
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    service_id: int = Field(foreign_key="service.id")
    access_token: str
    refresh_token: Optional[str] = None

    user: "User" = Relationship(back_populates="services")
    service: "Service" = Relationship(back_populates="users")
