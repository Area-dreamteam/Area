from pydantic import BaseModel, Field
from pathlib import Path

class ServiceGet(BaseModel):
    """Basic service information."""
    id: int = Field(description="Service ID", example=1)
    name: str = Field(description="Service name", example="GitHub")
    image_url: Path = Field(description="Service logo URL")
    category: str = Field(description="Service category", example="Development")
    color: str = Field(description="Service theme color", example="#f97316")

class ServiceIdGet(BaseModel):
    """Detailed service information."""
    id: int = Field(description="Service ID", example=1)
    name: str = Field(description="Service name", example="GitHub")
    description: str = Field(description="Service description", example="Code repository platform")
    image_url: Path = Field(description="Service logo URL")
    category: str = Field(description="Service category", example="Development")
    color: str = Field(description="Service theme color", example="#f97316")
    oauth_required: bool = Field(description="Requires OAuth authentication", example=True)
