from sqlmodel import SQLModel, Field, Relationship
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from ..users.user_oauth_login import UserOAuthLogin

class OAuthLogin(SQLModel, table=True):
    __tablename__ = "oauth_login"
    id: int = Field(primary_key=True)
    name: str = Field(unique=True, index=True)
    image_url: str
    color: str = Field(default="#000000")

    user_oauth_logins: List["UserOAuthLogin"] = Relationship(back_populates="oauth_login")
