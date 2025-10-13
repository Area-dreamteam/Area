from pydantic import BaseModel
from pathlib import Path

class OauthLoginGet(BaseModel):
    id: int
    name: str
    image_url: Path
    color: str
