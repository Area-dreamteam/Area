from pydantic import BaseModel, EmailStr
from pathlib import Path
from .role import Role

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    token_type: str = "bearer"
    access_token: str

class UserShortInfo(BaseModel):
    id: int
    name: str

class UserServiceGet(BaseModel):
    id: int
    name: str
    image_url: Path
    color: str

class UserIdGet(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: Role
    user_services: list[UserServiceGet]
