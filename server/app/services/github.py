"""GitHub OAuth integration service.

Provides OAuth login functionality for GitHub accounts.
Allows users to authenticate using their GitHub credentials.
"""

from services.oauth_lib import oauth_add_login
from core.security import sign_jwt
import requests
from urllib.parse import urlencode
from models.oauth.oauth_login import OAuthLogin
from models.users.user_oauth_login import UserOAuthLogin
from models.users.user import User
from sqlmodel import select
from fastapi import HTTPException, Response
from fastapi.responses import HTMLResponse
from core.config import settings

from pydantic import BaseModel
from services.services_classes import oauth_service
from sqlmodel import Session
from pydantic_core import ValidationError


class GithubOAuthTokenRes(BaseModel):
    """GitHub OAuth token response format."""
    access_token: str
    token_type: str
    scope: str


class GithubApiError(Exception):
    """GitHub API-specific errors."""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class github_oauth(oauth_service):
    """GitHub OAuth service for user authentication."""
    def __init__(self) -> None:
        super().__init__()

    def _get_token(self, client_id, client_secret, code):
        """Exchange authorization code for access token."""
        base_url = "https://github.com/login/oauth/access_token"
        params = {"client_id": client_id, "client_secret": client_secret, "code": code}

        r = requests.post(
            f"{base_url}?{urlencode(params)}", headers={"Accept": "application/json"}
        )

        if r.status_code != 200:
            raise GithubApiError("Invalid code or failed to retrieve token")

        try:
            return GithubOAuthTokenRes(**r.json())
        except ValidationError:
            raise GithubApiError("Invalid OAuth response")

    def _get_email(self, token):
        """Fetch user email from GitHub API."""
        base_url = "https://api.github.com/user/emails"
        email_r = requests.get(
            f"{base_url}",
            headers={"Authorization": f"token {token}", "Accept": "application/json"},
        )

        if email_r.status_code != 200:
            raise GithubApiError("Failed to retrieve mail")

        return email_r.json()

    def oauth_link(self) -> str:
        """Generate GitHub OAuth authorization URL."""
        base_url = "https://github.com/login/oauth/authorize"
        redirect = f"{settings.FRONT_URL}/callbacks/login/github_oauth"
        params = {
            "client_id": settings.GITHUB_CLIENT_ID,
            "redirect_uri": redirect,
            "prompt": "select_account",
            "allow_signup": "true",
            "scope": "user",
            "login": "",
            "force_verify": "true",
        }
        return f"{base_url}?{urlencode(params)}"

    def oauth_callback(
        self, session: Session, code: str, user: User | None
    ) -> Response:
        """Handle GitHub OAuth callback and create/authenticate user."""
        try:
            token_res = self._get_token(
                settings.GITHUB_CLIENT_ID, settings.GITHUB_CLIENT_SECRET, code
            )
        except GithubApiError as e:
            raise HTTPException(status_code=400, detail=e.message)
        try:
            user_info = self._get_email(token_res.access_token)[0]
        except GithubApiError as e:
            return HTTPException(status_code=400, detail=e.message)
        return oauth_add_login(
            session, self.name, user, token_res.access_token, user_info["email"]
        )
