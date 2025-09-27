from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .area_reaction import AreaReaction

class ReactionCondition(SQLModel, table=True):
    __tablename__ = "reaction_condition"
    id: int = Field(default=None, primary_key=True)
    area_reaction_id: int = Field(foreign_key="area_reaction.id")
    field: str
    operator: str
    value: str

    area_reaction: "AreaReaction" = Relationship(back_populates="conditions")
