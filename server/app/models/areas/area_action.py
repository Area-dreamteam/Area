from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Column, JSON, Relationship

if TYPE_CHECKING:
    from .area import Area
    from ..services.action import Action

class AreaAction(SQLModel, table=True):
    __tablename__ = "area_action"
    id: int = Field(default=None, primary_key=True)
    area_id: int = Field(foreign_key="area.id", ondelete="CASCADE")
    action_id: int = Field(foreign_key="action.id", ondelete="CASCADE")
    config: dict = Field(default_factory=dict, sa_column=Column(JSON))
    last_state: Optional[dict] = Field(default=None, sa_column=Column(JSON))

    area: "Area" = Relationship(back_populates="actions")
    action: "Action" = Relationship(back_populates="areas")
