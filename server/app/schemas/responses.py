from pydantic import BaseModel, Field

class MessageResponse(BaseModel):
    """Generic message response."""
    message: str = Field(description="Response message")

class UserRegistrationResponse(BaseModel):
    """User registration success response."""
    message: str = Field(description="Registration success message")
    id: int = Field(description="New user ID", example=1)
    email: str = Field(description="Registered email", example="user@example.com")

class UserDeletionResponse(BaseModel):
    """User deletion confirmation response."""
    message: str = Field(description="Deletion confirmation message")
    user_id: int = Field(description="ID of deleted user", example=1)

class AreaDeletionResponse(BaseModel):
    """Area deletion confirmation response."""
    message: str = Field(description="Deletion confirmation message")
    area_id: int = Field(description="ID of deleted area", example=1)
    user_id: int = Field(description="ID of area owner", example=1)

class ErrorResponse(BaseModel):
    """Error response model."""
    detail: str = Field(description="Error description", example="Resource not found")