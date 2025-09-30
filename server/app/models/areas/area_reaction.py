from typing import TYPE_CHECKING, List
from sqlmodel import SQLModel, Field, Column, JSON, Relationship

if TYPE_CHECKING:
    from .area import Area
    from ..services.reaction import Reaction
    from .reaction_condition import ReactionCondition

class AreaReaction(SQLModel, table=True):
    __tablename__ = "area_reaction"
    id: int = Field(default=None, primary_key=True)
    area_id: int = Field(foreign_key="area.id")
    reaction_id: int = Field(foreign_key="reaction.id")
    order_index: int = Field(default=0)
    delay: int = Field(default=0)
    config: dict = Field(default_factory=dict, sa_column=Column(JSON))

    area: "Area" = Relationship(back_populates="reactions")
    reaction: "Reaction" = Relationship(back_populates="area_reactions")
    conditions: List["ReactionCondition"] = Relationship(back_populates="area_reaction")
