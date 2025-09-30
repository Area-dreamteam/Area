from pydantic import BaseModel
from typing import Any
from .service import ServiceGet

class ReactionIdGet(BaseModel):
    id: int
    name: str
    description: str
    config_schema: Any
    service: ServiceGet

class ReactionBasicInfo(BaseModel):
    id: int
    name: str
    description: str
    service: ServiceGet

class ReactionShortInfo(BaseModel):
    id: int
    name: str
    description: str
