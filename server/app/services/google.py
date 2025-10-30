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


class GoogleApiError(Exception):
    """Google API-specific errors."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class GoogleOauth(oauth_service):
    """Google OAuth service for user authentication."""

    def __init__(self) -> None:
        super().__init__(color="#4285F4", img_url="/images/Google_logo.png")

    def _get_token(self, code: str) -> GoogleOAuthTokenRes:
        base_url = "https://oauth2.googleapis.com/token"
        redirect = f"{settings.FRONT_URL}/callbacks/login/{self.name}"
        params = {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": redirect,
        }
        r = requests.post(base_url, data=params)
        if r.status_code != 200:
            raise GoogleApiError("Failed to retrieve Google token")
        try:
            return GoogleOAuthTokenRes(**r.json())
        except ValidationError:
            raise GoogleApiError("Invalid Google OAuth response")

    def _get_user_info(self, token: str) -> Dict[str, Any]:
        url = "https://www.googleapis.com/oauth2/v2/userinfo"
        r = requests.get(url, headers={"Authorization": f"Bearer {token}"})
        if r.status_code != 200:
            raise GoogleApiError("Failed to fetch user info")
        return r.json()

    def oauth_link(self, state: str = None) -> str:
        """Generate Google OAuth authorization URL."""
        base_url = "https://accounts.google.com/o/oauth2/v2/auth"
        redirect = f"{settings.FRONT_URL}/callbacks/login/{self.name}"
        params = {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "redirect_uri": redirect,
            "response_type": "code",
            "scope": "https://www.googleapis.com/auth/userinfo.email",
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
        """Handle Google OAuth callback and create/authenticate user."""
        try:
            token_res = self._get_token(code)
        except GoogleApiError as e:
            raise HTTPException(status_code=400, detail=e.message)
        try:
            user_info = self._get_user_info(token_res.access_token)
        except GoogleApiError as e:
            return HTTPException(status_code=400, detail=e.message)
        return oauth_add_login(
            session, self.name, user, token_res.access_token, user_info["email"]
        )


class Gmail(ServiceClass):
    """Google services automation.

    Provides Gmail integration for email monitoring and sending.
    Supports filtering by sender, subject, and custom content.
    """

    class new_email_sent(Action):
        """Trigger when new email is sent."""

        service: "Gmail"

        def __init__(self) -> None:
            config_schema = []
            super().__init__("Triggered when new email is sent", config_schema)

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            token: str = get_user_service_token(session, user_id, self.service.name)

            try:
                message: Dict[str, Any] = self.service._get_latest_email(
                    token, label="in:sent"
                )
                logger.info("Gmail: Found matching email.")
                return self.service._compare_email_state(session, area_action, message)
            except GoogleApiError as e:
                logger.error(f"Gmail: error checking new emails - {e.message}")
                return False

    class new_email_inbox(Action):
        """Trigger when new email arrives."""

        service: "Gmail"

        def __init__(self) -> None:
            config_schema = []
            super().__init__("Triggered when new email arrives", config_schema)

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            token: str = get_user_service_token(session, user_id, self.service.name)

            try:
                message: Dict[str, Any] = self.service._get_latest_email(
                    token, label="in:inbox"
                )
                logger.info("Gmail: Found matching email.")
                return self.service._compare_email_state(session, area_action, message)
            except GoogleApiError as e:
                logger.error(f"Gmail: error checking new emails - {e.message}")
                return False

    class send_email(Reaction):
        """Send email to specified recipient."""

        service: "Gmail"

        def __init__(self) -> None:
            config_schema = [
                {"name": "to", "type": "input", "values": []},
                {"name": "subject", "type": "input", "values": []},
                {"name": "body", "type": "input", "values": []},
            ]
            super().__init__("Send email to recipient", config_schema)

        def execute(self, session: Session, area_action: AreaReaction, user_id: int):
            token: str = get_user_service_token(session, user_id, self.service.name)
            to = get_component(area_action.config, "to", "values")
            subject = get_component(area_action.config, "subject", "values")
            body = get_component(area_action.config, "body", "values")

            try:
                self.service._send_email(token, to, subject, body)
                logger.info(f"Gmail: Email sent to {to}")
            except GoogleApiError as e:
                logger.error(f"Gmail: error sending email - {e.message}")

    def __init__(self) -> None:
        super().__init__("Service email de Google", "mail", "#0A378A", "/images/Google_logo.png", True)

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
    #         raise GoogleApiError("Failed to refresh Google access token")
    #     try:
    #         return GoogleOAuthTokenRes(**r.json())
    #     except ValidationError:
    #         raise GoogleApiError("Invalid Google refresh token response")

    def _is_token_valid(self, token: str) -> bool:
        try:
            self._get_user_info(token)
            return True
        except GoogleApiError:
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
            raise GoogleApiError("Failed to retrieve Google token")
        try:
            return GoogleOAuthTokenRes(**r.json())
        except ValidationError:
            raise GoogleApiError("Invalid Google OAuth response")

    def _get_user_info(self, token: str) -> Dict[str, Any]:
        url = "https://www.googleapis.com/oauth2/v2/userinfo"
        r = requests.get(url, headers={"Authorization": f"Bearer {token}"})
        if r.status_code != 200:
            raise GoogleApiError("Failed to fetch user info")
        return r.json()

    def _compare_email_state(
        self,
        session: Session,
        area_action: AreaAction,
        message: Dict[str, Any],
    ) -> bool:
        if not area_action.last_state:
            area_action.last_state = message if message else None
            session.add(area_action)
            session.commit()
            return False
        if message is None:
            return False
        last_state_values = (
            area_action.last_state.get("snippet", ""),
            area_action.last_state.get("historyId", ""),
        )
        message_values = (
            message.get("snippet", ""),
            message.get("historyId", ""),
        )
        if last_state_values == message_values:
            return False
        area_action.last_state = message
        session.add(area_action)
        session.commit()
        return True

    def _get_latest_email(
        self,
        token: str,
        sender_filter: str = None,
        subject_filter: str = None,
        label: str = "in:inbox",
    ) -> List[Dict[str, Any]]:
        """Retrieve latest emails matching optional filters."""
        base_url = "https://gmail.googleapis.com/gmail/v1/users/me/messages"
        query = label
        if sender_filter:
            query += f"from:{sender_filter} "
        if subject_filter:
            query += f"subject:{subject_filter}"
        params = {"maxResults": 1, "q": query}
        r = requests.get(
            base_url, headers={"Authorization": f"Bearer {token}"}, params=params
        )
        if r.status_code != 200:
            raise GoogleApiError("Failed to retrieve messages")

        messages = r.json().get("messages", [])
        if not messages:
            return None

        msg_id = messages[0]["id"]
        detail_url = f"{base_url}/{msg_id}"
        detail = requests.get(
            detail_url,
            headers={"Authorization": f"Bearer {token}"},
            params={"format": "metadata"},
        )
        if detail.status_code != 200:
            raise GoogleApiError("Failed to retrieve message details")

        return detail.json()

    def _send_email(self, token: str, to: str, subject: str, body: str):
        """Send an email via Gmail API."""
        message = MIMEText(body)
        message["to"] = to
        message["subject"] = subject
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        payload = {"raw": raw}
        url = "https://gmail.googleapis.com/gmail/v1/users/me/messages/send"
        r = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
            json=payload,
        )
        if r.status_code not in (200, 202):
            raise GoogleApiError("Failed to send email")

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
        except GoogleApiError as e:
            raise HTTPException(status_code=400, detail=e.message)

        return oauth_add_link(session, self.name, user, token_res.access_token, request, is_mobile)
