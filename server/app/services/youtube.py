from sqlmodel import Session
from pydantic import BaseModel
from pydantic_core import ValidationError
from sqlmodel import select
import requests
from urllib.parse import urlencode
from fastapi import HTTPException, Response, Request

from typing import Dict, Any
from core.utils import generate_state
from core.categories import ServiceCategory
from services.oauth_lib import oauth_add_link
from models import AreaAction, UserService, AreaReaction, User, Service
from core.config import settings
from services.services_classes import (
    Service as ServiceClass,
    Action,
    Reaction,
    get_component,
)
from core.logger import logger
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
            ServiceCategory.MEDIA,
            "#FF0000",
            "/images/Youtube_logo.webp",
            True,
        )

    class video_likes_above_threshold(Action):
        """Triggered when a YouTube video exceeds a certain number of likes."""

        def __init__(self):
            config_schema = [
                {"name": "Video URL", "type": "input", "values": []},
                {
                    "name": "Like threshold",
                    "type": "input",
                    "values": [],
                },
            ]
            super().__init__(
                "Triggered when a video exceeds a like threshold", config_schema
            )

        def check(self, session, area_action, user_id):
            try:
                token: str = get_user_service_token(session, user_id, self.service.name)
                video_url: str = get_component(
                    area_action.config, "Video URL", "values"
                )
                threshold_str: str = get_component(
                    area_action.config, "Like threshold", "values"
                )
                try:
                    threshold = int(threshold_str)
                except Exception:
                    raise YoutubeApiError("Invalid like threshold value")

                if "=" not in video_url:
                    raise YoutubeApiError("Invalid video URL format")
                video_id = video_url.split("=")[1]

                url = "https://www.googleapis.com/youtube/v3/videos"
                params = {"part": "statistics", "id": video_id}
                headers = {"Authorization": f"Bearer {token}"}

                r = requests.get(url, headers=headers, params=params)
                if r.status_code != 200:
                    raise YoutubeApiError(f"Failed to fetch video stats: {r.text}")

                items = r.json().get("items", [])
                if not items:
                    raise YoutubeApiError("Video not found")

                like_count = int(items[0]["statistics"].get("likeCount", 0))
                previous_state = (area_action.last_state or {}).get(
                    "previous_state", False
                )
                current_state = like_count > threshold

                area_action.last_state = {"previous_state": current_state}
                session.add(area_action)
                session.commit()

                return current_state and not previous_state
            except YoutubeApiError as e:
                logger.error(f"{self.service.name}: {e}")
            return False

    class video_likes_below_threshold(Action):
        """Triggered when a YouTube video falls below a certain number of likes."""

        def __init__(self):
            config_schema = [
                {"name": "Video URL", "type": "input", "values": []},
                {
                    "name": "Like threshold",
                    "type": "input",
                    "values": [],
                },
            ]
            super().__init__(
                "Triggered when a video is below a like threshold", config_schema
            )

        def check(self, session, area_action, user_id):
            try:
                token: str = get_user_service_token(session, user_id, self.service.name)
                video_url: str = get_component(
                    area_action.config, "Video URL", "values"
                )
                threshold_str: str = get_component(
                    area_action.config, "Like threshold", "values"
                )
                try:
                    threshold = int(threshold_str)
                except Exception:
                    raise YoutubeApiError("Invalid like threshold value")

                if "=" not in video_url:
                    raise YoutubeApiError("Invalid video URL format")
                video_id = video_url.split("=")[1]

                url = "https://www.googleapis.com/youtube/v3/videos"
                params = {"part": "statistics", "id": video_id}
                headers = {"Authorization": f"Bearer {token}"}

                r = requests.get(url, headers=headers, params=params)
                if r.status_code != 200:
                    raise YoutubeApiError(f"Failed to fetch video stats: {r.text}")

                items = r.json().get("items", [])
                if not items:
                    raise YoutubeApiError("Video not found")

                like_count = int(items[0]["statistics"].get("likeCount", 0))
                previous_state = (area_action.last_state or {}).get(
                    "previous_state", False
                )
                current_state = like_count < threshold

                area_action.last_state = {"previous_state": current_state}
                session.add(area_action)
                session.commit()

                return current_state and not previous_state
            except YoutubeApiError as e:
                logger.error(f"{self.service.name}: {e}")
            return False

    class new_liked_video(Action):
        """Triggered when you like a new video on YouTube."""

        def __init__(self):
            super().__init__("Triggered when you like a new video", [])

        def check(self, session, area_action, user_id):
            try:
                token = get_user_service_token(session, user_id, self.service.name)

                url = "https://www.googleapis.com/youtube/v3/videos"
                params = {
                    "part": "id,snippet",
                    "myRating": "like",
                    "maxResults": 1,
                }
                headers = {"Authorization": f"Bearer {token}"}

                r = requests.get(url, headers=headers, params=params)
                if r.status_code != 200:
                    raise YoutubeApiError(f"Failed to fetch liked videos: {r.text}")

                items = r.json().get("items", [])
                if not items:
                    return False

                latest_liked_video = items[0]
                return self.service._compare_data(
                    session, area_action, latest_liked_video, "id"
                )
            except YoutubeApiError as e:
                logger.error(f"{self.service.name}: {e}")
            return False

    class new_subscription(Action):
        """Triggered when the user subscribes to a new channel."""

        def __init__(self):
            super().__init__("Triggered when a new channel subscription is made", [])

        def check(self, session, area_action, user_id):
            try:
                token = get_user_service_token(session, user_id, self.service.name)

                url = "https://www.googleapis.com/youtube/v3/subscriptions"
                params = {
                    "part": "snippet",
                    "mine": "true",
                    "order": "relevance",
                    "maxResults": 1,
                }
                headers = {"Authorization": f"Bearer {token}"}

                r = requests.get(url, headers=headers, params=params)
                if r.status_code != 200:
                    raise YoutubeApiError(f"Failed to fetch subscriptions: {r.text}")

                items = r.json().get("items", [])
                if not items:
                    return False
                latest_subscription = items[0]
                return self.service._compare_data(
                    session, area_action, latest_subscription, "id"
                )
            except YoutubeApiError as e:
                logger.error(f"{self.service.name}: {e}")
            return False

    class like_video(Reaction):
        """Like a YouTube video."""

        service: "Youtube"

        def __init__(self):
            config_schema = [
                {"name": "Video URL", "type": "input", "values": []},
                {
                    "name": "Rating",
                    "type": "select",
                    "values": ["like", "dislike", "none"],
                },
            ]
            super().__init__("Like a YouTube video", config_schema)

        def execute(self, session: Session, area_reaction: AreaReaction, user_id: int):
            try:
                token: str = get_user_service_token(session, user_id, self.service.name)
                video_url: str = get_component(
                    area_reaction.config, "Video URL", "values"
                )
                rating: str = get_component(area_reaction.config, "Rating", "values")
                if "=" not in video_url:
                    raise YoutubeApiError("Invalid video URL format")
                video_id = video_url.split("=")[1]

                url = "https://www.googleapis.com/youtube/v3/videos/rate"
                params = {"id": video_id, "rating": {rating}}
                headers = {"Authorization": f"Bearer {token}"}
                r = requests.post(url, headers=headers, params=params)
                if r.status_code != 204:
                    raise YoutubeApiError(f"Failed to like video: {r.text}")
                logger.info(f"{self.service.name} - {self.name} - Rated video {video_id} with {rating} - User: {user_id}")
            except YoutubeApiError as e:
                logger.error(f"{self.service.name}: {e}")

    def _compare_data(
        self, session: Session, area_action: AreaAction, data: Dict[str, Any], key: str
    ) -> bool:
        """Check if the data is new compared to the last stored one."""
        if not area_action.last_state:
            area_action.last_state = data
            session.add(area_action)
            session.commit()
            return False

        if data and data[key] != area_action.last_state.get(key):
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
            self._get_user_channel(token)
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

    def _get_channel_by_name(self, session: Session, user_id: int, name: str) -> dict:
        token: str = get_user_service_token(session, user_id, self.name)
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "part": "snippet",
            "type": "channel",
            "q": name,
        }
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        }
        r = requests.get(url, headers=headers, params=params)
        if r.status_code != 200:
            raise YoutubeApiError(f"Failed to fetch channel: {r.text}")
        data = r.json()
        if not data.get("items"):
            raise YoutubeApiError("No channel found with that name.")
        return data["items"][0]

    def _get_user_channel(self, token: str) -> dict:
        url = "https://www.googleapis.com/youtube/v3/channels"
        params = {"part": "id,snippet", "mine": "true"}
        headers = {"Authorization": f"Bearer {token}"}
        r = requests.get(url, headers=headers, params=params)
        if r.status_code != 200:
            raise YoutubeApiError(f"Failed to get channel info: {r.text}")
        data = r.json()
        return data["items"][0]

    def oauth_link(self, state: str = None) -> str:
        """Generate Google OAuth authorization URL."""
        base_url = "https://accounts.google.com/o/oauth2/v2/auth"
        redirect = f"{settings.FRONT_URL}/callbacks/link/{self.name}"
        params = {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "redirect_uri": redirect,
            "response_type": "code",
            "scope": "https://www.googleapis.com/auth/youtube https://www.googleapis.com/auth/youtubepartner https://www.googleapis.com/auth/youtube.readonly https://www.googleapis.com/auth/youtube.force-ssl",
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
