from typing import Optional, TYPE_CHECKING, List
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .action import Action
    from .reaction import Reaction
    from ..users.user_service import UserService

class Service(SQLModel, table=True):
    __tablename__ = "service"
    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True, nullable=False)
    description: Optional[str] = None
    image_url: str

    actions: List["Action"] = Relationship(back_populates="service")
    reactions: List["Reaction"] = Relationship(back_populates="service")
    users: List["UserService"] = Relationship(back_populates="service")
