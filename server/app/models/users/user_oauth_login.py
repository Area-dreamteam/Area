from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING


if TYPE_CHECKING:
    from .user import User
    from ..oauth.oauth_login import OAuthLogin

class UserOAuthLogin(SQLModel, table=True):
    __tablename__ = "user_oauth_login"
    
    id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="users.id", ondelete="CASCADE")
    oauth_login_id: int = Field(foreign_key="oauth_login.id", ondelete="CASCADE")
    access_token: str
    refresh_token: Optional[str] = None
    
    oauth_login: "OAuthLogin" = Relationship(back_populates="user_oauth_logins")
    user: "User" = Relationship(back_populates="oauth_logins")
