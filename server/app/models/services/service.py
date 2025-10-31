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
    category: str
    color: str = "#000000"
    oauth_required: bool

    actions: List["Action"] = Relationship(back_populates="service", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    reactions: List["Reaction"] = Relationship(back_populates="service", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    users: List["UserService"] = Relationship(back_populates="service", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
