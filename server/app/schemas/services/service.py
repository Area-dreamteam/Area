from pydantic import BaseModel
from pathlib import Path

class ServiceGet(BaseModel):
    id: int
    name: str
    image_url: Path
    category: str
    color: str

class ServiceIdGet(BaseModel):
    id: int
    name: str
    description: str
    image_url: Path
    category: str
    color: str
    oauth_required: bool
