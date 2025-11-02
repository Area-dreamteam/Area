from pydantic import BaseModel, EmailStr, Field, field_validator
from pathlib import Path
from .role import Role
import re


class UserCreate(BaseModel):
    """User registration/login schema."""
    email: EmailStr = Field(description="User email address", example="user@example.com")
    password: str = Field(min_length=8, description="User password", example="securepassword123")

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate password meets security requirements."""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[!@#$%^&*]', v):
            raise ValueError('Password must contain at least one special character (!@#$%^&*)')
        return v


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


class UserOauthLoginGet(BaseModel):
    """OAuth login service information."""
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
    oauth_login: list[UserOauthLoginGet] = Field(description="Connected OAuth services")


class UserUpdate(BaseModel):
    """User profile update schema."""
    name: str = Field(description="Updated username", example="johndoe")
    email: EmailStr = Field(description="Updated email", example="johndoe@example.com")

class UserUpdatePassword(BaseModel):
    """User profile update password schema."""
    current_password: str = Field(min_length=8, description="Current password", example="currentsecurepassword123")
    new_password: str = Field(min_length=8, description="Updated password", example="newsecurepassword123")

    @field_validator('new_password')
    @classmethod
    def validate_new_password(cls, v: str) -> str:
        """Validate new password meets security requirements."""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[!@#$%^&*]', v):
            raise ValueError('Password must contain at least one special character (!@#$%^&*)')
        return v
