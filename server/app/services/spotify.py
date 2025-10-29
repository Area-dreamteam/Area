import requests
from urllib.parse import urlencode
from sqlmodel import Session, select
from fastapi import HTTPException, Response, Request
from typing import Dict, Any, List
import json
from pydantic import BaseModel
from datetime import datetime, timezone
import base64

from core.config import settings
from core.utils import generate_state
from core.logger import logger
from services.oauth_lib import oauth_add_link
from services.services_classes import (
    Service as ServiceClass,
    Action,
    Reaction,
    get_component,
)
from models import AreaAction, AreaReaction, UserService, Service, User
from api.users.db import get_user_service_token


class SpotifyOAuthTokenRes(BaseModel):
    """Spotify OAuth token response format."""

    access_token: str
    token_type: str
    scope: str
    expires_in: int
    refresh_token: str


class SpotifyApiError(Exception):
    """Spotify API-specific errors."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class Spotify(ServiceClass):
    """Spotify automation service."""

    def __init__(self) -> None:
        super().__init__("Spotify", "music", "#1DB954", "", True)

    class new_album(Action):
        """Triggered when a new activity is uploaded."""

        service: "Spotify"

        def __init__(self):
            config_schema = []
            super().__init__("Triggered when a new activity is recorded", config_schema)

        def check(self, session, area_action, user_id):
            token = get_user_service_token(session, user_id, self.service.name)
            url = "https://www.strava.com/api/v3/athlete/activities"
            params = {"per_page": 1}
            r = requests.get(
                url, headers={"Authorization": f"Bearer {token}"}, params=params
            )
            if r.status_code != 200:
                raise SpotifyApiError("Failed to fetch activities")

            activity = r.json()[0] if r.json() else None
            return self.service._compare_data(session, area_action, activity)

    def _compare_data(
        self, session: Session, area_action: AreaAction, data: Dict[str, Any]
    ) -> bool:
        """Check if the data is new compared to the last stored one."""
        if not area_action.last_state:
            area_action.last_state = data
            session.add(area_action)
            session.commit()
            return False

        if data and data["id"] != area_action.last_state.get("id"):
            area_action.last_state = data
            session.add(area_action)
            session.commit()
            return True
        return False

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

    def _is_token_valid(self, token: str) -> bool:
        try:
            self._get_user_info(token)
            return True
        except SpotifyApiError:
            return False

    def oauth_link(self, state: str = None) -> str:
        base_url = "https://accounts.spotify.com/authorize"
        redirect = f"http://127.0.0.1:3000/callbacks/link/{self.name}"
        params = {
            "client_id": settings.SPOTIFY_CLIENT_ID,
            "response_type": "code",
            "state": state if state else generate_state(),
            "redirect_uri": redirect,
            "show_dialog": "false",
            "scope": "user-read-email user-library-read playlist-modify-public playlist-modify-private",
        }
        return f"{base_url}?{urlencode(params)}"

    def _get_token(self, code: str) -> SpotifyOAuthTokenRes:
        url = "https://accounts.spotify.com/api/token"
        redirect = f"http://127.0.0.1:3000/callbacks/link/{self.name}"

        auth_str = f"{settings.SPOTIFY_CLIENT_ID}:{settings.SPOTIFY_CLIENT_SECRET}"
        b64_auth = base64.b64encode(auth_str.encode()).decode()
        headers = {
            "content-type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {b64_auth}",
        }
        data = {
            "code": code,
            "redirect_uri": redirect,
            "grant_type": "authorization_code",
        }
        r = requests.post(url, data=data, headers=headers)
        if r.status_code != 200:
            logger.error(f"Spotify token error: {r.text}")
            raise SpotifyApiError(f"Failed to get Spotify token: {r.text}")
        return SpotifyOAuthTokenRes(**r.json())

    def _get_user_info(self, token: str) -> Dict[str, Any]:
        url = "https://api.spotify.com/v1/me"
        headers = {"Authorization": f"Bearer {token}"}
        r = requests.get(url, headers=headers)
        if r.status_code != 200:
            raise SpotifyApiError(f"Failed to get Spotify user info: {r.text}")
        return r.json()

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
        except SpotifyApiError as e:
            raise HTTPException(status_code=400, detail=e.message)

        return oauth_add_link(session, self.name, user, token_res.access_token)
