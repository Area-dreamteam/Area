from sqlmodel import Session
from pydantic import BaseModel
from pydantic_core import ValidationError
from sqlmodel import select
import requests
from urllib.parse import urlencode
from fastapi import HTTPException, Response, Request
from typing import Dict, Any, List
import base64
from email.mime.text import MIMEText

from core.utils import generate_state
from services.oauth_lib import oauth_add_link, oauth_add_login
from models import AreaAction, UserService, AreaReaction, User, Service
from core.config import settings
from services.services_classes import (
    Service as ServiceClass,
    Action,
    Reaction,
    get_component,
)
from core.logger import logger
from services.services_classes import oauth_service
from api.users.db import get_user_service_token


class GoogleOAuthTokenRes(BaseModel):
    """Google OAuth token response format."""

    access_token: str
    token_type: str
    refresh_token: str
    expires_in: int


class YoutubeApiError(Exception):
    """Google API-specific errors."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class Youtube(ServiceClass):

    def __init__(self) -> None:
        super().__init__(
            "Service youtube de Google",
            "medias",
            "#CC1717",
            "/images/Youtube_logo.webp",
            True,
        )

    def is_connected(self, session: Session, user_id: int) -> bool:
        user_service: UserService = session.exec(
            select(UserService)
            .join(Service, Service.id == UserService.service_id)
            .where(
                UserService.user_id == user_id,
                Service.name == self.name,
            )
        ).first()
        if not user_service:
            return False
        if self._is_token_valid(user_service.access_token):
            return True
        if user_service.refresh_token is None:
            return False
        # refresh le token
        return True

    # def _refresh_token(self, refresh_token: str) -> GoogleOAuthTokenRes:
    #     """Refresh Google OAuth token using refresh_token."""
    #     base_url = "https://oauth2.googleapis.com/token"
    #     params = {
    #         "client_id": settings.GOOGLE_CLIENT_ID,
    #         "client_secret": settings.GOOGLE_CLIENT_SECRET,
    #         "refresh_token": refresh_token,
    #         "grant_type": "refresh_token",
    #     }
    #     r = requests.post(base_url, data=params)
    #     if r.status_code != 200:
    #         raise YoutubeApiError("Failed to refresh Google access token")
    #     try:
    #         return GoogleOAuthTokenRes(**r.json())
    #     except ValidationError:
    #         raise YoutubeApiError("Invalid Google refresh token response")

    def _is_token_valid(self, token: str) -> bool:
        try:
            self._get_user_info(token)
            return True
        except YoutubeApiError:
            return False

    def _get_token(self, code: str) -> GoogleOAuthTokenRes:
        base_url = "https://oauth2.googleapis.com/token"
        redirect = f"{settings.FRONT_URL}/callbacks/link/{self.name}"
        params = {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": redirect,
        }
        r = requests.post(base_url, data=params)
        if r.status_code != 200:
            raise YoutubeApiError("Failed to retrieve Google token")
        try:
            return GoogleOAuthTokenRes(**r.json())
        except ValidationError:
            raise YoutubeApiError("Invalid Google OAuth response")

    def _get_user_info(self, token: str) -> Dict[str, Any]:
        url = "https://www.googleapis.com/oauth2/v2/userinfo"
        r = requests.get(url, headers={"Authorization": f"Bearer {token}"})
        if r.status_code != 200:
            raise YoutubeApiError("Failed to fetch user info")
        return r.json()

    def oauth_link(self, state: str = None) -> str:
        """Generate Google OAuth authorization URL."""
        base_url = "https://accounts.google.com/o/oauth2/v2/auth"
        redirect = f"{settings.FRONT_URL}/callbacks/link/{self.name}"
        params = {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "redirect_uri": redirect,
            "response_type": "code",
            "scope": "https://www.googleapis.com/auth/gmail.send https://www.googleapis.com/auth/gmail.readonly https://www.googleapis.com/auth/userinfo.email",
            "access_type": "offline",
            "state": state if state else generate_state(),
            "prompt": "consent",
        }
        return f"{base_url}?{urlencode(params)}"

    def oauth_callback(
        self,
        session: Session,
        code: str,
        user: User | None,
        request: Request = None,
        is_mobile: bool = False,
    ) -> Response:
        try:
            token_res = self._get_token(code)
        except YoutubeApiError as e:
            raise HTTPException(status_code=400, detail=e.message)

        return oauth_add_link(
            session, self.name, user, token_res.access_token, request, is_mobile
        )
