from typing import Optional, TYPE_CHECKING, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

if TYPE_CHECKING:
    from ..users.user import User
    from .area_action import AreaAction
    from .area_reaction import AreaReaction

class Area(SQLModel, table=True):
    __tablename__ = "area"
    id: int = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    name: str
    description: Optional[str] = None
    enable: bool = Field(default=False)
    created_at: datetime
    is_public: bool = Field(default=False)

    user: Optional["User"] = Relationship(back_populates="areas")
    actions: List["AreaAction"] = Relationship(back_populates="area")
    reactions: List["AreaReaction"] = Relationship(back_populates="area")
