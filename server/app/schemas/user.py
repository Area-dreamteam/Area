from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    token_type: str = "bearer"
    access_token: str
