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
        super().__init__(
            "Spotify", "music", "#1DB954", "images/Spotify_logo.webp", True
        )

    class device_connect_to_spotify(Action):
        """Triggered once when a specific Spotify device becomes active."""

        service: "Spotify"

        def __init__(self):
            config_schema = [{"name": "Device name", "type": "input", "values": []}]
            super().__init__(
                "Triggered once when a specific Spotify device becomes active.",
                config_schema,
            )

        def check(self, session, area_action, user_id):
            token = get_user_service_token(session, user_id, self.service.name)
            device_name = get_component(area_action.config, "Device name", "values")

            url = "https://api.spotify.com/v1/me/player"
            r = requests.get(url, headers={"Authorization": f"Bearer {token}"})

            if r.status_code == 204:
                current_active: bool = False
            elif r.status_code != 200:
                raise SpotifyApiError("Failed to fetch connect devices")
            else:
                data: Dict[str, Any] = r.json()
                current_device: str = data.get("device", {}).get("name", "").lower()
                current_active: bool = (
                    device_name.lower() in current_device
                    and data.get("is_playing", False)
                )
            previous_state: bool = (area_action.last_state or {}).get(
                "previous_state", False
            )
            area_action.last_state = {"previous_state": current_active}
            session.add(area_action)
            session.commit()

            return current_active and not previous_state

    class something_is_currently_playing(Action):
        """Triggered when something is currently playing."""

        service: "Spotify"

        def __init__(self):
            config_schema = []
            super().__init__(
                "Triggered when something is currently playing", config_schema
            )

        def check(self, session, area_action, user_id):
            token = get_user_service_token(session, user_id, self.service.name)

            url = "https://api.spotify.com/v1/me/player"
            r = requests.get(url, headers={"Authorization": f"Bearer {token}"})
            if r.status_code == 204:
                current_active: bool = False
            elif r.status_code != 200:
                raise SpotifyApiError("Failed to fetch player status info")
            else:
                current_active: bool = r.json().get("is_playing", False)

            previous_state: bool = (area_action.last_state or {}).get(
                "previous_state", False
            )
            area_action.last_state = {"previous_state": current_active}
            session.add(area_action)
            session.commit()

            return current_active and not previous_state

    class volume_above_threshold(Action):
        """Triggered when the Spotify player volume is above a certain threshold."""

        service: "Spotify"

        def __init__(self):
            config_schema = [
                {
                    "name": "Threshold",
                    "type": "select",
                    "values": [
                        "00",
                        "10",
                        "20",
                        "30",
                        "40",
                        "50",
                        "60",
                        "70",
                        "80",
                        "90",
                        "100",
                    ],
                }
            ]
            super().__init__(
                "Triggered when volume is above a threshold", config_schema
            )

        def check(self, session, area_action, user_id):
            token = get_user_service_token(session, user_id, self.service.name)
            try:
                threshold = int(
                    get_component(area_action.config, "Threshold", "values")
                )
            except Exception:
                raise SpotifyApiError("Incorrect threshold value")

            url = "https://api.spotify.com/v1/me/player"
            r = requests.get(url, headers={"Authorization": f"Bearer {token}"})
            if r.status_code == 204:
                return False
            if r.status_code != 200:
                raise SpotifyApiError(f"Failed to fetch player info: {r.text}")

            volume: float = r.json().get("device", {}).get("volume_percent", 0)
            previous_state: bool = (area_action.last_state or {}).get(
                "previous_state", False
            )
            current_state: bool = volume > threshold

            area_action.last_state = {"previous_state": current_state}
            session.add(area_action)
            session.commit()
            logger.error(f"volume above  {current_state}")
            return current_state and not previous_state

    class volume_below_threshold(Action):
        """Triggered when the Spotify player volume is below a certain threshold."""

        service: "Spotify"

        def __init__(self):
            config_schema = [
                {
                    "name": "Threshold",
                    "type": "select",
                    "values": [
                        "00",
                        "10",
                        "20",
                        "30",
                        "40",
                        "50",
                        "60",
                        "70",
                        "80",
                        "90",
                        "100",
                    ],
                }
            ]
            super().__init__(
                "Triggered when volume is below a threshold", config_schema
            )

        def check(self, session, area_action, user_id):
            token = get_user_service_token(session, user_id, self.service.name)
            try:
                threshold = int(
                    get_component(area_action.config, "Threshold", "values")
                )
            except Exception:
                raise SpotifyApiError("Incorrect threshold value")
            url = "https://api.spotify.com/v1/me/player"
            r = requests.get(url, headers={"Authorization": f"Bearer {token}"})
            if r.status_code == 204:
                return False
            if r.status_code != 200:
                raise SpotifyApiError(f"Failed to fetch player info: {r.text}")
            volume = r.json().get("device", {}).get("volume_percent", 0)
            previous_state: bool = (area_action.last_state or {}).get(
                "previous_state", False
            )
            current_state: bool = volume < threshold
            area_action.last_state = {"previous_state": current_state}
            session.add(area_action)
            session.commit()
            logger.error(f"volume below  {current_state}")
            return current_state and not previous_state

    class set_volume(Reaction):
        """Set Spotify player volume to a specific value."""

        service: "Spotify"

        def __init__(self):
            config_schema = [
                {
                    "name": "Volume percent",
                    "type": "select",
                    "values": [
                        "00",
                        "10",
                        "20",
                        "30",
                        "40",
                        "50",
                        "60",
                        "70",
                        "80",
                        "90",
                        "100",
                    ],
                }
            ]
            super().__init__("Set player volume", config_schema)

        def execute(self, session, area_action, user_id):
            token = get_user_service_token(session, user_id, self.service.name)
            try:
                volume_percent = int(
                    get_component(area_action.config, "Volume percent", "values")
                )
            except Exception:
                raise SpotifyApiError("Incorrect volume value")

            url = "https://api.spotify.com/v1/me/player/volume"
            params = {"volume_percent": volume_percent}
            r = requests.put(
                url, headers={"Authorization": f"Bearer {token}"}, params=params
            )
            if r.status_code != 204:
                logger.error(f"Spotify volume set error: {r.text}")
                raise SpotifyApiError("Failed to set volume")
            logger.debug(f"Spotify: volume set to {volume_percent}% for user {user_id}")

    class set_repeat(Reaction):
        """Set the repeat mode for the user's playback."""

        service: "Spotify"

        def __init__(self):
            config_schema = [
                {
                    "name": "State",
                    "type": "select",
                    "values": ["track", "context", "off"],
                },
            ]
            super().__init__(
                "Set the repeat mode for the user's playback.", config_schema
            )

        def execute(self, session, area_action, user_id):
            token = get_user_service_token(session, user_id, self.service.name)
            state = get_component(area_action.config, "State", "values")

            url = "https://api.spotify.com/v1/me/player/repeat"
            params = {"state": state}
            r = requests.put(
                url, headers={"Authorization": f"Bearer {token}"}, params=params
            )
            if r.status_code == 404:
                logger.debug(
                    f"Spotify {self.name}: no active playback for user {user_id}"
                )
                return
            if r.status_code != 200:
                logger.error(f"Spotify repeat error: {r.text}")
                raise SpotifyApiError("Failed to set repeat mode")
            logger.debug(f"Spotify: repeat mode set to {state} for user {user_id}")

    class skip_to_next(Reaction):
        """Skips to next track in the user's queue on Spotify."""

        service: "Spotify"

        def __init__(self):
            config_schema = []
            super().__init__(
                "Skips to next track in the user's queue on Spotify", config_schema
            )

        def execute(self, session, area_reaction, user_id):
            token = get_user_service_token(session, user_id, self.service.name)
            url = "https://api.spotify.com/v1/me/player/next"
            r = requests.post(url, headers={"Authorization": f"Bearer {token}"})
            if r.status_code == 404:
                logger.debug(
                    f"Spotify {self.name}: no active playback for user {user_id}"
                )
                return
            if r.status_code != 200:
                logger.error(f"Spotify post error: {r.text}")
                raise SpotifyApiError(f"Failed to skip to next track: {r.text}")
            logger.debug("Spotify: Skip to next track  for user {user_id}")

    class skip_to_previous(Reaction):
        """Skips to previous track in the user's queue on Spotify."""

        service: "Spotify"

        def __init__(self):
            config_schema = []
            super().__init__(
                "Skips to previous track in the user's queue on Spotify", config_schema
            )

        def execute(self, session, area_reaction, user_id):
            token = get_user_service_token(session, user_id, self.service.name)
            url = "https://api.spotify.com/v1/me/player/previous"
            r = requests.post(url, headers={"Authorization": f"Bearer {token}"})
            if r.status_code == 404:
                logger.debug(
                    f"Spotify {self.name}: no active playback for user {user_id}"
                )
                return
            if r.status_code != 200:
                logger.error(f"Spotify post error: {r.text}")
                raise SpotifyApiError(f"Failed to skip to previous track: {r.text}")
            logger.debug("Spotify: Skip to previous track for user {user_id}")

    class pause_playback(Reaction):
        """Pause playback on the user's account."""

        service: "Spotify"

        def __init__(self):
            config_schema = []
            super().__init__("Pause playback on the user's account", config_schema)

        def execute(self, session, area_reaction, user_id):
            token = get_user_service_token(session, user_id, self.service.name)
            url = "https://api.spotify.com/v1/me/player/pause"
            r = requests.put(url, headers={"Authorization": f"Bearer {token}"})
            if r.status_code == 404:
                logger.error(f"Spotify {self.name}: no active playback")
                return
            if r.status_code != 200:
                logger.debug(f"Spotify post error: {r.status_code} for user {user_id}")
                raise SpotifyApiError(f"Failed to pause playback: {r.text}")
            logger.debug("Spotify: Pause playback for user {user_id}")

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
        localhost_domain: str = settings.FRONT_URL.find("localhost")
        redirect_domain: str = settings.FRONT_URL
        if localhost_domain > -1:
            redirect_domain = "http://127.0.0.1:3000"
        redirect = f"{redirect_domain}/callbacks/link/{self.name}"

        params = {
            "client_id": settings.SPOTIFY_CLIENT_ID,
            "response_type": "code",
            "state": state if state else generate_state(),
            "redirect_uri": redirect,
            "show_dialog": "false",
            "scope": "user-read-email user-library-read playlist-modify-public playlist-modify-private app-remote-control streaming, user-read-playback-state user-read-currently-playing user-modify-playback-state",
        }
        return f"{base_url}?{urlencode(params)}"

    def _get_token(self, code: str) -> SpotifyOAuthTokenRes:
        url = "https://accounts.spotify.com/api/token"
        localhost_domain: str = settings.FRONT_URL.find("localhost")
        redirect_domain: str = settings.FRONT_URL
        if localhost_domain > -1:
            redirect_domain = "http://127.0.0.1:3000"
        redirect = f"{redirect_domain}/callbacks/link/{self.name}"

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
