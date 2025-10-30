from pydantic import BaseModel, Field
from typing import Any
from .service import ServiceGet

class ReactionIdGet(BaseModel):
    id: int
    name: str
    description: str
    config_schema: Any
    service: ServiceGet
    
class ReactionInfo(BaseModel):
    """Basic reaction information."""
    id: int = Field(description="Reaction ID", example=1)
    name: str = Field(description="Reaction name", example="Create Task")
    description: str = Field(description="Reaction description", example="Creates new task in project")
    service: ServiceGet = Field(description="Associated service details")
    config: Any = Field(description="Reaction-specific configuration parameters")

class ReactionBasicInfo(BaseModel):
    """Basic reaction information."""
    id: int = Field(description="Reaction ID", example=1)
    name: str = Field(description="Reaction name", example="Create Task")
    description: str = Field(description="Reaction description", example="Creates new task in project")
    service: ServiceGet = Field(description="Associated service details")

class ReactionShortInfo(BaseModel):
    id: int
    name: str
    description: str

class CreateAreaReaction(BaseModel):
    """Reaction configuration for area creation."""
    reaction_id: int = Field(description="ID of the reaction to configure", example=1)
    config: Any = Field(description="Reaction-specific configuration parameters")
