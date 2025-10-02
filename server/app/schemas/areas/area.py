from pydantic import BaseModel
from datetime import datetime
from ..services import ActionBasicInfo
from ..services import ReactionBasicInfo
from ..users import UserShortInfo

class AreaGet(BaseModel):
    id: int
    name: str
    description: str
    user: UserShortInfo
    enable: bool
    created_at: datetime
    color: str

class AreaIdGet(BaseModel):
    area_info: AreaGet
    action: ActionBasicInfo
    reactions: list[ReactionBasicInfo]

class AreaGetPublic(BaseModel):
    id: int
    name: str
    description: str
    user: UserShortInfo
    created_at: datetime
    color: str

class AreaIdGetPublic(BaseModel):
    area_info: AreaGetPublic
    action: ActionBasicInfo
    reactions: list[ReactionBasicInfo]
