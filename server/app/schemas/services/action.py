from pydantic import BaseModel, Field
from typing import Any
from .service import ServiceGet

class ActionIdGet(BaseModel):
    """Detailed action configuration."""
    id: int = Field(description="Action ID", example=1)
    name: str = Field(description="Action name", example="Issue Opened")
    description: str = Field(description="Action description", example="Triggers when new issue created")
    config_schema: Any = Field(description="Configuration schema for this action")
    service: ServiceGet = Field(description="Associated service details")

class ActionInfo(BaseModel):
    """Basic action information."""
    id: int = Field(description="Action ID", example=1)
    name: str = Field(description="Action name", example="Issue Opened")
    description: str = Field(description="Action description", example="Triggers when new issue created")
    service: ServiceGet = Field(description="Associated service details")
    config: Any = Field(description="Action-specific configuration parameters")

class ActionBasicInfo(BaseModel):
    """Basic action information."""
    id: int = Field(description="Action ID", example=1)
    name: str = Field(description="Action name", example="Issue Opened")
    description: str = Field(description="Action description", example="Triggers when new issue created")
    service: ServiceGet = Field(description="Associated service details")

class ActionShortInfo(BaseModel):
    id: int
    name: str
    description: str

class CreateAreaAction(BaseModel):
    """Action configuration for area creation."""
    action_id: int = Field(description="ID of the action to configure", example=1)
    config: Any = Field(description="Action-specific configuration parameters")
