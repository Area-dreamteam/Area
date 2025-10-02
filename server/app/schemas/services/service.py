from pydantic import BaseModel
from pathlib import Path

class ServiceGet(BaseModel):
    id: int
    name: str
    image_url: Path
    color: str

class ServiceIdGet(BaseModel):
    id: int
    name: str
    image_url: Path
    color: str
    connected: bool
