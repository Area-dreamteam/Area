import requests
from urllib.parse import urlencode
from sqlmodel import Session, select
from fastapi import HTTPException, Response, Request
from typing import Dict, Any
import json
from pydantic import BaseModel

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


class RedditOAuthTokenRes(BaseModel):
    """Reddit OAuth token response format."""

    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str
    scope: str


class RedditApiError(Exception):
    """Reddit API-specific errors."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class Reddit(ServiceClass):
    """Reddit automation service."""

    def __init__(self) -> None:
        super().__init__("Reddit", "social", "#FF4500", "/images/Reddit_logo.webp", True)

    class new_post(Action):
        """Trigger when a new post appears in a subreddit."""

        service: "Reddit"

        def __init__(self) -> None:
            config_schema = [{"name": "subreddit", "type": "input", "values": []}]
            super().__init__(
                "Triggered when a new post appears in a subreddit", config_schema
            )

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            token: str = get_user_service_token(session, user_id, self.service.name)
            subreddit = get_component(area_action.config, "subreddit", "values")

            url = f"https://oauth.reddit.com/r/{subreddit}/new?limit=1"
            headers = {"Authorization": f"bearer {token}", "User-Agent": "AreaApp/1.0"}

            r = requests.get(url, headers=headers)
            if r.status_code != 200:
                logger.error(f"Reddit error: {r.text}")
                return False

            posts = r.json().get("data", {}).get("children", [])
            if not posts:
                return False

            latest_post = posts[0]["data"]
            return self.service._compare_post_state(session, area_action, latest_post)

    class new_hot_post(Action):
        """Trigger when a new hot post appears in a subreddit."""

        service: "Reddit"

        def __init__(self) -> None:
            config_schema = [{"name": "subreddit", "type": "input", "values": []}]
            super().__init__(
                "Triggered when a new hot post appears in a subreddit", config_schema
            )

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            token: str = get_user_service_token(session, user_id, self.service.name)
            subreddit = get_component(area_action.config, "subreddit", "values")

            url = f"https://oauth.reddit.com/r/{subreddit}/hot?limit=1"
            headers = {"Authorization": f"bearer {token}", "User-Agent": "AreaApp/1.0"}

            r = requests.get(url, headers=headers)
            if r.status_code != 200:
                logger.error(f"Reddit error: {r.text}")
                return False

            posts = r.json().get("data", {}).get("children", [])
            if not posts:
                return False

            latest_post = posts[0]["data"]
            return self.service._compare_post_state(session, area_action, latest_post)

    class new_top_post(Action):
        """Trigger when a new top post appears in a subreddit."""

        service: "Reddit"

        def __init__(self) -> None:
            config_schema = [{"name": "subreddit", "type": "input", "values": []}]
            super().__init__(
                "Triggered when a new top post appears in a subreddit", config_schema
            )

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            token: str = get_user_service_token(session, user_id, self.service.name)
            subreddit = get_component(area_action.config, "subreddit", "values")

            url = f"https://oauth.reddit.com/r/{subreddit}/top?limit=1"
            headers = {"Authorization": f"bearer {token}", "User-Agent": "AreaApp/1.0"}

            r = requests.get(url, headers=headers)
            if r.status_code != 200:
                logger.error(f"Reddit error: {r.text}")
                return False

            posts = r.json().get("data", {}).get("children", [])
            if not posts:
                return False

            latest_post = posts[0]["data"]
            return self.service._compare_post_state(session, area_action, latest_post)

    class post_message(Reaction):
        """Post a new message in a subreddit."""

        service: "Reddit"

        def __init__(self) -> None:
            config_schema = [
                {"name": "subreddit", "type": "input", "values": []},
                {"name": "title", "type": "input", "values": []},
                {"name": "text", "type": "input", "values": []},
            ]
            super().__init__("Post a new message to a subreddit", config_schema)

        def execute(self, session: Session, area_action: AreaReaction, user_id: int):
            token: str = get_user_service_token(session, user_id, self.service.name)
            subreddit = get_component(area_action.config, "subreddit", "values")
            title = get_component(area_action.config, "title", "values")
            text = get_component(area_action.config, "text", "values")

            url = "https://oauth.reddit.com/api/submit"
            headers = {"Authorization": f"bearer {token}", "User-Agent": "AreaApp/1.0"}
            data = {
                "sr": subreddit,
                "kind": "self",
                "title": title,
                "text": text,
                "api_type": "json",
                "resubmit": True,
            }

            r = requests.post(url, headers=headers, data=data)
            if r.status_code != 200:
                logger.error(f"Reddit post error: {r.text}")
                raise RedditApiError("Failed to post message")
            logger.debug(f"Posted to r/{subreddit}")

    def _compare_post_state(
        self, session: Session, area_action: AreaAction, post: Dict[str, Any]
    ) -> bool:
        """Check if the post is new compared to the last stored one."""
        if not area_action.last_state:
            area_action.last_state = post
            session.add(area_action)
            session.commit()
            return False

        last_id = area_action.last_state.get("id")
        new_id = post.get("id")
        if last_id == new_id:
            return False

        area_action.last_state = post
        session.add(area_action)
        session.commit()
        return True

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
        except RedditApiError:
            return False

    def oauth_link(self, state: str = None) -> str:
        base_url = "https://www.reddit.com/api/v1/authorize"
        redirect = f"{settings.FRONT_URL}/callbacks/link/{self.name}"
        params = {
            "client_id": settings.REDDIT_CLIENT_ID,
            "response_type": "code",
            "state": state if state else generate_state(),
            "redirect_uri": redirect,
            "duration": "permanent",
            "scope": "identity read submit",
        }
        return f"{base_url}?{urlencode(params)}"

    def _get_token(self, code: str) -> RedditOAuthTokenRes:
        url = "https://www.reddit.com/api/v1/access_token"
        auth = (settings.REDDIT_CLIENT_ID, settings.REDDIT_CLIENT_SECRET)
        redirect = f"{settings.FRONT_URL}/callbacks/link/{self.name}"
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect,
        }
        headers = {"User-Agent": "AreaApp/1.0"}
        r = requests.post(url, data=data, auth=auth, headers=headers)
        if r.status_code != 200:
            logger.error(f"Reddit token error: {r.text}")
            raise RedditApiError(f"Failed to get Reddit token: {r.text}")
        return RedditOAuthTokenRes(**r.json())

    def _get_user_info(self, token: str) -> Dict[str, Any]:
        url = "https://oauth.reddit.com/api/v1/me"
        headers = {"Authorization": f"bearer {token}", "User-Agent": "AreaApp/1.0"}
        r = requests.get(url, headers=headers)
        if r.status_code != 200:
            raise RedditApiError("Failed to get Reddit user info")
        data = r.json()
        return data

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
        except RedditApiError as e:
            raise HTTPException(status_code=400, detail=e.message)

        return oauth_add_link(
            session, self.name, user, token_res.access_token, request, is_mobile
        )
