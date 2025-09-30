from pydantic import BaseModel
from typing import Any
from .service import ServiceGet

class ActionIdGet(BaseModel):
    id: int
    name: str
    description: str
    config_schema: Any
    service: ServiceGet

class ActionBasicInfo(BaseModel):
    id: int
    name: str
    description: str
    service: ServiceGet

class ActionShortInfo(BaseModel):
    id: int
    name: str
    description: str
