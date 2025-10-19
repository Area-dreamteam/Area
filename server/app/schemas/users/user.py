from pydantic import BaseModel, EmailStr
from pathlib import Path
from .role import Role


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    token_type: str = "Bearer"
    access_token: str


class UserShortInfo(BaseModel):
    id: int
    name: str


class UserOauthLoginGet(BaseModel):
    id: int
    name: str
    image_url: Path
    color: str
    connected: bool


class UserIdGet(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: Role
    oauth_login: list[UserOauthLoginGet]

class UserUpdate(BaseModel):
    name: str
    email: EmailStr
    password: str
