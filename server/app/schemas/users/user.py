from pydantic import BaseModel, EmailStr, Field
from pathlib import Path
from .role import Role


class UserCreate(BaseModel):
    """User registration/login schema."""
    email: EmailStr = Field(description="User email address", example="user@example.com")
    password: str = Field(min_length=8, description="User password", example="securepassword123")


class TokenResponse(BaseModel):
    """JWT token response."""
    token_type: str = Field(default="Bearer", description="Token type")
    access_token: str = Field(description="JWT access token")


class UserShortInfo(BaseModel):
    """Basic user information."""
    id: int = Field(description="User ID", example=1)
    name: str = Field(description="Username", example="johndoe")


class UserServiceGet(BaseModel):
    """User service connection status."""
    id: int = Field(description="Service ID", example=1)
    name: str = Field(description="Service name", example="GitHub")
    image_url: Path = Field(description="Service logo URL")
    color: str = Field(description="Service theme color", example="#f97316")
    connected: bool = Field(description="Connection status", example=True)


class UserIdGet(BaseModel):
    """Complete user profile information."""
    id: int = Field(description="User ID", example=1)
    name: str = Field(description="Username", example="johndoe")
    email: EmailStr = Field(description="User email", example="johndoe@example.com")
    role: Role = Field(description="User role")
    user_services: list[UserServiceGet] = Field(description="Connected services")
