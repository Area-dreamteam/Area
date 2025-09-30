from typing import Optional, TYPE_CHECKING, List
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .user_service import UserService
    from ..areas.area import Area

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: int = Field(default=None, primary_key=True)
    name: str
    email: str = Field(unique=True, index=True)
    password: Optional[str] = None
    role: str = "user"

    services: List["UserService"] = Relationship(back_populates="user")
    areas: List["Area"] = Relationship(back_populates="user")
