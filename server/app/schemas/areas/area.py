from pydantic import BaseModel, Field
from datetime import datetime
from ..services import ActionBasicInfo, ReactionBasicInfo, CreateAreaAction, CreateAreaReaction
from ..users import UserShortInfo
from typing import Optional

class AreaGet(BaseModel):
    """Area information for owner/authenticated view."""
    id: int = Field(description="Area ID", example=1)
    name: str = Field(description="Area name", example="GitHub to Todoist")
    description: str = Field(description="Area description", example="Create task when issue opened")
    user: UserShortInfo = Field(description="Area creator")
    enable: bool = Field(description="Area active status", example=True)
    created_at: datetime = Field(description="Creation timestamp")
    color: str = Field(description="UI theme color", example="#f97316")

class AreaIdGet(BaseModel):
    """Complete area details with action and reactions."""
    area_info: AreaGet = Field(description="Basic area information")
    action: ActionBasicInfo = Field(description="Trigger action configuration")
    reactions: list[ReactionBasicInfo] = Field(description="Response reactions list")

class AreaGetPublic(BaseModel):
    """Public area information (no private details)."""
    id: int = Field(description="Area ID", example=1)
    name: str = Field(description="Area name", example="GitHub to Todoist")
    description: str = Field(description="Area description", example="Create task when issue opened")
    user: UserShortInfo = Field(description="Area creator")
    created_at: datetime = Field(description="Creation timestamp")
    color: str = Field(description="UI theme color", example="#f97316")

class AreaIdGetPublic(BaseModel):
    """Complete public area details."""
    area_info: AreaGetPublic = Field(description="Public area information")
    action: ActionBasicInfo = Field(description="Trigger action configuration")
    reactions: list[ReactionBasicInfo] = Field(description="Response reactions list")

class CreateArea(BaseModel):
    """Schema for creating new automation areas."""
    name: str = Field(min_length=1, max_length=100, description="Area name", example="GitHub to Todoist")
    description: str = Field(min_length=1, max_length=500, description="Area description", example="Create task when issue opened")
    action: CreateAreaAction = Field(description="Trigger action configuration")
    reactions: list[CreateAreaReaction] = Field(min_items=1, description="Response reactions (at least one required)")

class UpdateArea(BaseModel):
    """Schema for updating existing areas."""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Updated area name")
    description: Optional[str] = Field(None, min_length=1, max_length=500, description="Updated area description")
    action: Optional[CreateAreaAction] = Field(None, description="Updated trigger action")
    reactions: Optional[list[CreateAreaReaction]] = Field(None, min_items=1, description="Updated reactions list")
