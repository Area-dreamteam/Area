from pydantic import BaseModel
from pathlib import Path


class OauthLoginGet(BaseModel):
    name: str
    image_url: Path
    color: str
