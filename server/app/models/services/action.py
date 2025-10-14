from typing import Optional, TYPE_CHECKING, List
from sqlmodel import SQLModel, Field, Column, JSON, UniqueConstraint, Relationship

if TYPE_CHECKING:
    from .service import Service
    from ..areas.area_action import AreaAction

class Action(SQLModel, table=True):
    __tablename__ = "action"
    id: int = Field(default=None, primary_key=True)
    service_id: int = Field(foreign_key="service.id", ondelete="CASCADE")
    name: str
    interval: str
    description: Optional[str] = None
    config_schema: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    __table_args__ = (UniqueConstraint("service_id", "name", name="uq_action_service_name"),)

    service: "Service" = Relationship(back_populates="actions")
    areas: List["AreaAction"] = Relationship(back_populates="action")
