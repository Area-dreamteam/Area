"""LinkedIn OAuth integration service.

Provides LinkedIn automation service for professional networking and content management.
"""

from typing import Dict, Any, List
import requests
from urllib.parse import urlencode
from pydantic import BaseModel
from pydantic_core import ValidationError
from fastapi import HTTPException, Response, Request
from sqlmodel import Session, select

from services.services_classes import (
    Service as ServiceClass,
    Action,
    Reaction,
    get_component,
)
from services.oauth_lib import oauth_add_link
from api.users.db import get_user_service_token

from models.users.user import User
from models.users.user_service import UserService
from models.services.service import Service
from models import AreaAction, AreaReaction

from core.config import settings
from core.utils import generate_state
from core.logger import logger
from core.categories import ServiceCategory


class LinkedInOAuthTokenRes(BaseModel):
    """LinkedIn OAuth token response format."""

    access_token: str
    expires_in: int
    refresh_token: str | None = None
    refresh_token_expires_in: int | None = None
    scope: str | None = None


class LinkedInApiError(Exception):
    """LinkedIn API-specific errors."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class LinkedIn(ServiceClass):
    """LinkedIn service for professional networking automation."""

    def __init__(self) -> None:
        super().__init__(
            description="LinkedIn Automation - Professional networking and content management",
            category=ServiceCategory.SOCIAL,
            color="#0A66C2",
            img_url="/images/LinkedIn_logo.webp",
            oauth=True,
        )

    class new_post_by_user(Action):
        """Triggered when a specific user creates a new post."""

        service: "LinkedIn"

        def __init__(self):
            config_schema = [
                {"name": "Username", "type": "input", "values": []},
            ]
            super().__init__(
                "Triggered when a specific user creates a new post",
                config_schema,
                "*/15 * * * *",
            )

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            token = get_user_service_token(session, user_id, self.service.name)
            if not token:
                return False

            username = get_component(area_action.config, "Username", "values")
            if not username:
                logger.error("No username provided")
                return False

            try:
                posts = self.service._get_user_posts(token, username)
            except LinkedInApiError as e:
                logger.error(f"Failed to fetch posts: {e.message}")
                return False

            current_post_ids = {post["id"] for post in posts}

            if not area_action.last_state or "post_ids" not in area_action.last_state:
                area_action.last_state = {"post_ids": list(current_post_ids)}
                session.add(area_action)
                session.commit()
                return False

            previous_post_ids = set(area_action.last_state.get("post_ids", []))

            area_action.last_state = {"post_ids": list(current_post_ids)}
            session.add(area_action)
            session.commit()

            new_posts = current_post_ids - previous_post_ids
            return len(new_posts) > 0

    class connection_request_received(Action):
        """Triggered when a new connection request is received."""

        service: "LinkedIn"

        def __init__(self):
            super().__init__(
                "Triggered when a new connection request is received",
                [],
                "*/10 * * * *",
            )

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            token = get_user_service_token(session, user_id, self.service.name)
            if not token:
                return False

            try:
                requests_data = self.service._get_connection_requests(token)
            except LinkedInApiError as e:
                logger.error(f"Failed to fetch connection requests: {e.message}")
                return False

            current_request_ids = {req["id"] for req in requests_data}

            if not area_action.last_state:
                area_action.last_state = {"request_ids": list(current_request_ids)}
                session.add(area_action)
                session.commit()
                return False

            previous_request_ids = set(area_action.last_state.get("request_ids", []))

            area_action.last_state = {"request_ids": list(current_request_ids)}
            session.add(area_action)
            session.commit()

            new_requests = current_request_ids - previous_request_ids
            return len(new_requests) > 0

    class profile_view_threshold(Action):
        """Triggered once when profile views reach a specific threshold."""

        service: "LinkedIn"

        def __init__(self):
            config_schema = [
                {"name": "Threshold", "type": "input", "values": []},
            ]
            super().__init__(
                "Triggered once when profile views reach a specific threshold",
                config_schema,
                "0 */6 * * *",
            )

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            token = get_user_service_token(session, user_id, self.service.name)
            if not token:
                return False

            threshold_str = get_component(area_action.config, "Threshold", "values")

            try:
                threshold = int(threshold_str)
            except (ValueError, TypeError):
                logger.error(f"Invalid threshold value: {threshold_str}")
                return False

            try:
                stats = self.service._get_profile_stats(token)
                current_views = stats.get("profile_views", 0)
            except LinkedInApiError as e:
                logger.error(f"Failed to fetch profile stats: {e.message}")
                return False

            already_triggered = (
                area_action.last_state.get("triggered", False)
                if area_action.last_state
                else False
            )

            if current_views >= threshold and not already_triggered:
                area_action.last_state = {"triggered": True, "views": current_views}
                session.add(area_action)
                session.commit()
                return True

            area_action.last_state = {
                "triggered": already_triggered,
                "views": current_views,
            }
            session.add(area_action)
            session.commit()
            return False

    class share_post(Reaction):
        """Share a text post on LinkedIn."""

        service: "LinkedIn"

        def __init__(self):
            config_schema = [
                {"name": "Content", "type": "input", "values": []},
                {
                    "name": "Visibility",
                    "type": "select",
                    "values": ["PUBLIC", "CONNECTIONS"],
                },
            ]
            super().__init__("Share a text post on LinkedIn", config_schema)

        def execute(self, session: Session, area_reaction: AreaReaction, user_id: int):
            token = get_user_service_token(session, user_id, self.service.name)
            if not token:
                logger.error(f"No token for user {user_id}")
                return

            content = get_component(area_reaction.config, "Content", "values")
            visibility = get_component(area_reaction.config, "Visibility", "values")

            if not content:
                logger.error("No content provided for post")
                return

            try:
                self.service._create_post(token, content, visibility)
                logger.info(f"LinkedIn post created successfully")
            except LinkedInApiError as e:
                logger.error(f"Failed to create post: {e.message}")

    class send_message(Reaction):
        """Send a direct message to a connection."""

        service: "LinkedIn"

        def __init__(self):
            config_schema = [
                {"name": "Recipient URN", "type": "input", "values": []},
                {"name": "Message", "type": "input", "values": []},
            ]
            super().__init__(
                "Send a direct message to a LinkedIn connection", config_schema
            )

        def execute(self, session: Session, area_reaction: AreaReaction, user_id: int):
            token = get_user_service_token(session, user_id, self.service.name)
            if not token:
                logger.error(f"No token for user {user_id}")
                return

            recipient_urn = get_component(
                area_reaction.config, "Recipient URN", "values"
            )
            message = get_component(area_reaction.config, "Message", "values")

            if not recipient_urn or not message:
                logger.error("Missing recipient URN or message")
                return

            try:
                self.service._send_message(token, recipient_urn, message)
                logger.info(f"LinkedIn message sent successfully")
            except LinkedInApiError as e:
                logger.error(f"Failed to send message: {e.message}")

    class add_comment(Reaction):
        """Add a comment to a LinkedIn post."""

        service: "LinkedIn"

        def __init__(self):
            config_schema = [
                {"name": "Post URN", "type": "input", "values": []},
                {"name": "Comment", "type": "input", "values": []},
            ]
            super().__init__("Add a comment to a LinkedIn post", config_schema)

        def execute(self, session: Session, area_reaction: AreaReaction, user_id: int):
            token = get_user_service_token(session, user_id, self.service.name)
            if not token:
                logger.error(f"No token for user {user_id}")
                return

            post_urn = get_component(area_reaction.config, "Post URN", "values")
            comment = get_component(area_reaction.config, "Comment", "values")

            if not post_urn or not comment:
                logger.error("Missing post URN or comment")
                return

            try:
                self.service._add_comment(token, post_urn, comment)
                logger.info(f"LinkedIn comment added successfully")
            except LinkedInApiError as e:
                logger.error(f"Failed to add comment: {e.message}")

    def _make_api_request(
        self,
        token: str,
        endpoint: str,
        method: str = "GET",
        data: Dict[str, Any] | None = None,
        api_version: str = "202405",
    ) -> Dict[str, Any] | List[Dict[str, Any]]:
        """Make authenticated request to LinkedIn API."""
        url = f"https://api.linkedin.com/rest{endpoint}"
        headers = {
            "Authorization": f"Bearer {token}",
            "LinkedIn-Version": api_version,
            "X-Restli-Protocol-Version": "2.0.0",
            "Content-Type": "application/json",
        }

        r = requests.request(method, url, headers=headers, json=data)

        if r.status_code not in [200, 201, 204]:
            logger.error(f"LinkedIn API error: {r.status_code} - {r.text}")
            raise LinkedInApiError(f"API request failed: {r.status_code}")

        if not r.text or r.status_code == 204:
            return {}

        return r.json()

    def _is_token_valid(self, token: str) -> bool:
        """Check if the access token is still valid."""
        try:
            self._make_api_request(token, "/me")
            return True
        except LinkedInApiError:
            return False

    def _get_user_profile_urn(self, token: str) -> str:
        """Get the authenticated user's profile URN."""
        try:
            data = self._make_api_request(token, "/me")
            return data.get("sub", "")
        except LinkedInApiError as e:
            raise LinkedInApiError(f"Failed to get user profile: {e.message}")

    def _get_user_posts(
        self, token: str, username: str, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Fetch recent posts by a user."""
        try:
            endpoint = f"/posts?author={username}&count={limit}"
            response = self._make_api_request(token, endpoint)
            return response.get("elements", [])
        except LinkedInApiError as e:
            raise LinkedInApiError(f"Failed to fetch user posts: {e.message}")

    def _get_connection_requests(self, token: str) -> List[Dict[str, Any]]:
        """Fetch pending connection requests."""
        try:
            endpoint = "/invitations?q=recipient&status=PENDING"
            response = self._make_api_request(token, endpoint)
            return response.get("elements", [])
        except LinkedInApiError as e:
            raise LinkedInApiError(f"Failed to fetch connection requests: {e.message}")

    def _get_profile_stats(self, token: str) -> Dict[str, Any]:
        """Fetch profile statistics including views."""
        try:
            endpoint = (
                "/networkSizes/urn:li:person:{id}?edgeType=CompanyFollowedByMember"
            )
            response = self._make_api_request(token, endpoint)
            return response
        except LinkedInApiError as e:
            raise LinkedInApiError(f"Failed to fetch profile stats: {e.message}")

    def _create_post(
        self, token: str, content: str, visibility: str = "PUBLIC"
    ) -> Dict[str, Any]:
        """Create a text post on LinkedIn."""
        try:
            profile_urn = self._get_user_profile_urn(token)

            post_data = {
                "author": profile_urn,
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {"text": content},
                        "shareMediaCategory": "NONE",
                    }
                },
                "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": visibility},
            }

            response = self._make_api_request(
                token, "/ugcPosts", method="POST", data=post_data
            )
            return response
        except LinkedInApiError as e:
            raise LinkedInApiError(f"Failed to create post: {e.message}")

    def _send_message(
        self, token: str, recipient_urn: str, message: str
    ) -> Dict[str, Any]:
        """Send a direct message to a connection."""
        try:
            profile_urn = self._get_user_profile_urn(token)

            message_data = {
                "recipients": [recipient_urn],
                "subject": "Message",
                "body": message,
            }

            response = self._make_api_request(
                token, "/messages", method="POST", data=message_data
            )
            return response
        except LinkedInApiError as e:
            raise LinkedInApiError(f"Failed to send message: {e.message}")

    def _add_comment(self, token: str, post_urn: str, comment: str) -> Dict[str, Any]:
        """Add a comment to a LinkedIn post."""
        try:
            profile_urn = self._get_user_profile_urn(token)

            comment_data = {
                "actor": profile_urn,
                "object": post_urn,
                "message": {"text": comment},
            }

            response = self._make_api_request(
                token,
                "/socialActions/{post_urn}/comments",
                method="POST",
                data=comment_data,
            )
            return response
        except LinkedInApiError as e:
            raise LinkedInApiError(f"Failed to add comment: {e.message}")

    def is_connected(self, session: Session, user_id: int) -> bool:
        """Check if user has a valid LinkedIn connection."""
        user_service = session.exec(
            select(UserService)
            .join(Service)
            .where(
                UserService.user_id == user_id,
                Service.name == self.name,
            )
        ).first()

        if not user_service:
            return False

        return self._is_token_valid(user_service.access_token)

    def oauth_link(self, state: str = "") -> str:
        """Generate LinkedIn OAuth authorization URL."""
        base_url = "https://www.linkedin.com/oauth/v2/authorization"
        redirect = f"{settings.FRONT_URL}/callbacks/link/{self.name}"

        params = {
            "response_type": "code",
            "client_id": settings.LINKEDIN_CLIENT_ID,
            "redirect_uri": redirect,
            "state": state if state else generate_state(),
            "scope": "profile email w_member_social r_basicprofile r_organization_social",
        }

        return f"{base_url}?{urlencode(params)}"

    def oauth_callback(
        self,
        session: Session,
        code: str,
        user: User | None,
        request: Request | None = None,
        is_mobile: bool = False,
    ) -> Response:
        """Handle OAuth callback and link service to user."""
        if not user:
            raise HTTPException(status_code=401, detail="User must be authenticated")

        try:
            token_res = self._get_token(code)
        except LinkedInApiError as e:
            raise HTTPException(status_code=400, detail=e.message)

        return oauth_add_link(
            session,
            self.name,
            user,
            token_res.access_token,
            request,
            is_mobile,
        )

    def _get_token(self, code: str) -> LinkedInOAuthTokenRes:
        """Exchange authorization code for access token."""
        base_url = "https://www.linkedin.com/oauth/v2/accessToken"
        redirect = f"{settings.FRONT_URL}/callbacks/link/{self.name}"

        data = {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": settings.LINKEDIN_CLIENT_ID,
            "client_secret": settings.LINKEDIN_CLIENT_SECRET,
            "redirect_uri": redirect,
        }

        r = requests.post(
            base_url,
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        if r.status_code != 200:
            logger.error(f"LinkedIn token exchange failed: {r.status_code} - {r.text}")
            raise LinkedInApiError("Failed to exchange authorization code")

        try:
            return LinkedInOAuthTokenRes(**r.json())
        except ValidationError as e:
            logger.error(f"Invalid LinkedIn token response: {e}")
            raise LinkedInApiError("Invalid OAuth response format")
