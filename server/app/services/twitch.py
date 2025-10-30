import requests
from urllib.parse import urlencode
from sqlmodel import Session, select
from fastapi import HTTPException, Response, Request
from typing import Dict, Any, List
import json
from pydantic import BaseModel
from datetime import datetime, timezone

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


class TwitchOAuthTokenRes(BaseModel):
    """Twitch OAuth token response format."""

    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str


class TwitchApiError(Exception):
    """Twitch API-specific errors."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class Twitch(ServiceClass):
    """Twitch automation service."""

    def __init__(self) -> None:
        super().__init__("Twitch", "music", "#6441a5", "images/Twitch_logo.webp", True)

    class new_follower_on_channel(Action):
        """Triggered when you have a new follow."""

        service: "Twitch"

        def __init__(self):
            config_schema = []
            super().__init__("Triggered when you have a new follow", config_schema)

        def check(self, session, area_action, user_id):
            token = get_user_service_token(session, user_id, self.service.name)
            user_info = self.service._get_user_info(token)
            logger.error(user_info)
            broadcaster_id: int = user_info.get("id")
            url = "https://api.twitch.tv/helix/channels/followers"
            headers = {
                "Authorization": f"Bearer {token}",
                "Client-Id": settings.TWITCH_CLIENT_ID,
            }
            params = {"broadcaster_id": broadcaster_id}
            r = requests.get(url, headers=headers, params=params)
            if r.status_code != 200:
                raise TwitchApiError("Failed to fetch followers")

            nb_followed = {"total": r.json().get("total")} if r.json() else None
            return self.service._compare_data(session, area_action, nb_followed)

    class you_follow_new_channel(Action):
        """Triggered when you follow a new channel."""

        service: "Twitch"

        def __init__(self):
            config_schema = []
            super().__init__("Triggered when you follow a new channel", config_schema)

        def check(self, session, area_action, user_id):
            token = get_user_service_token(session, user_id, self.service.name)
            user_info = self.service._get_user_info(token)
            user_id: int = user_info.get("id")
            url = "https://api.twitch.tv/helix/channels/followed"
            headers = {
                "Authorization": f"Bearer {token}",
                "Client-Id": settings.TWITCH_CLIENT_ID,
            }
            params = {"user_id": user_id}
            r = requests.get(url, headers=headers, params=params)
            if r.status_code != 200:
                raise TwitchApiError("Failed to fetch followed")

            nb_followed = {"total": r.json().get("total")} if r.json() else None
            return self.service._compare_data(session, area_action, nb_followed)

    class is_in_top_games(Action):
        """Triggered when your game is in Top 10 Games this day."""

        service: "Twitch"

        def __init__(self):
            config_schema = [{"name": "game", "type": "input", "values": []}]
            super().__init__("Triggered when your game is in Top 10 Games this day", config_schema, "* * 1 * *")

        def check(self, session, area_action, user_id):
            token = get_user_service_token(session, user_id, self.service.name)
            game_name = get_component(area_action.config, "game", "values")
            url = "https://api.twitch.tv/helix/games/top"
            headers = {
                "Authorization": f"Bearer {token}",
                "Client-Id": settings.TWITCH_CLIENT_ID,
            }
            params = {"first": 10}
            r = requests.get(url, headers=headers, params=params)
            if r.status_code != 200:
                raise TwitchApiError("Failed to fetch followed")

            games: Dict[str, Any] = r.json().get("data")
            logger.error(games)
            for game_info in games:
                if game_name.lower() in game_info.get("name").lower():
                    return True
            return False

    def _compare_data(
        self, session: Session, area_action: AreaAction, data: Dict[str, Any]
    ) -> bool:
        """Check if the data is new compared to the last stored one."""
        if not area_action.last_state:
            area_action.last_state = data
            session.add(area_action)
            session.commit()
            return False

        if data and data.get("total") > area_action.last_state.get("total"):
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
        except TwitchApiError:
            return False

    def oauth_link(self, state: str = None) -> str:
        base_url = "https://id.twitch.tv/oauth2/authorize"
        redirect = f"{settings.FRONT_URL}/callbacks/link/{self.name}"
        params = {
            "client_id": settings.TWITCH_CLIENT_ID,
            "response_type": "code",
            "state": state if state else generate_state(),
            "redirect_uri": redirect,
            "approval_prompt": "auto",
            "scope": "user:read:email user:read:follows moderator:read:followers",
        }
        return f"{base_url}?{urlencode(params)}"

    def _get_token(self, code: str) -> TwitchOAuthTokenRes:
        url = "https://id.twitch.tv/oauth2/token"
        redirect = f"{settings.FRONT_URL}/callbacks/link/{self.name}"
        data = {
            "client_id": settings.TWITCH_CLIENT_ID,
            "client_secret": settings.TWITCH_CLIENT_SECRET,
            "code": code,
            "redirect_uri": redirect,
            "grant_type": "authorization_code",
        }
        r = requests.post(url, data=data)
        if r.status_code != 200:
            logger.error(f"Twitch token error: {r.text}")
            raise TwitchApiError(f"Failed to get Twitch token: {r.text}")
        return TwitchOAuthTokenRes(**r.json())

    def _get_user_info(self, token: str) -> Dict[str, Any]:
        url = "https://api.twitch.tv/helix/users"
        headers = {
            "Authorization": f"Bearer {token}",
            "Client-Id": settings.TWITCH_CLIENT_ID,
        }
        r = requests.get(url, headers=headers)
        if r.status_code != 200:
            raise TwitchApiError(f"Failed to get Twitch user info: {r.text}")
        return r.json().get("data")[0]

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
        except TwitchApiError as e:
            raise HTTPException(status_code=400, detail=e.message)

        return oauth_add_link(session, self.name, user, token_res.access_token)
