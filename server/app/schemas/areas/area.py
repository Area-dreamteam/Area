from pydantic import BaseModel
from datetime import datetime
from ..services.action import ActionBasicInfo
from ..services.reaction import ReactionBasicInfo
from ..users.user import UserBasicInfo

class AreaGet(BaseModel):
    id: int
    name: str
    description: str
    user: UserBasicInfo
    enable: bool
    created_at: datetime
    color: str

class AreaIdGet(BaseModel):
    area_info: AreaGet
    action: ActionBasicInfo
    reaction: ReactionBasicInfo

class AreaGetPublic(BaseModel):
    id: int
    name: str
    description: str
    user: UserBasicInfo
    created_at: datetime
    color: str

class AreaIdGetPublic(BaseModel):
    area_info: AreaGetPublic
    action: ActionBasicInfo
    reaction: ReactionBasicInfo
