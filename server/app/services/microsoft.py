from sqlmodel import Session
from pydantic import BaseModel
from sqlmodel import select
import requests
from urllib.parse import urlencode
from fastapi import HTTPException, Response, Request
from typing import Dict, Any
import json

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


class MicrosoftOAuthTokenRes(BaseModel):
    """Microsoft OAuth token response format."""

    access_token: str
    token_type: str
    refresh_token: str
    expires_in: int


class MicrosoftApiError(Exception):
    """Microsoft API-specific errors."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class MicrosoftOauth(oauth_service):
    """Microsoft OAuth login service."""

    def __init__(self) -> None:
        super().__init__(color="#00A4EF", img_url="/images/Microsoft_logo.png")

    def _get_token(self, code: str) -> MicrosoftOAuthTokenRes:
        url = f"https://login.microsoftonline.com/{settings.MICROSOFT_DIR_TENANT}/oauth2/v2.0/token"
        redirect = f"{settings.FRONT_URL}/callbacks/login/{self.name}"
        data = {
            "client_id": settings.MICROSOFT_CLIENT_ID,
            "client_secret": settings.MICROSOFT_CLIENT_SECRET,
            "code": code,
            "redirect_uri": redirect,
            "grant_type": "authorization_code",
        }
        r = requests.post(url, data=data)
        if r.status_code != 200:
            raise MicrosoftApiError(f"Failed to get Microsoft token: {r.text}")
        return MicrosoftOAuthTokenRes(**r.json())

    def _get_user_info(self, token: str) -> Dict[str, Any]:
        url = "https://graph.microsoft.com/v1.0/me"
        r = requests.get(url, headers={"Authorization": f"Bearer {token}"})
        if r.status_code != 200:
            raise MicrosoftApiError("Failed to get Microsoft user info")
        data = r.json()
        email = data.get("mail") or data.get("userPrincipalName")
        data["email"] = email
        return data

    def oauth_link(self, state: str = None) -> str:
        base_url = f"https://login.microsoftonline.com/{settings.MICROSOFT_DIR_TENANT}/oauth2/v2.0/authorize"
        redirect = f"{settings.FRONT_URL}/callbacks/login/{self.name}"
        params = {
            "client_id": settings.MICROSOFT_CLIENT_ID,
            "response_type": "code",
            "redirect_uri": redirect,
            "scope": "openid profile offline_access https://graph.microsoft.com/User.Read",
            "state": state if state else generate_state(),
            "prompt": "select_account",
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
        """Handle Microsoft OAuth callback and create/authenticate user."""
        try:
            token_res = self._get_token(code)
        except MicrosoftApiError as e:
            raise HTTPException(status_code=400, detail=e.message)
        try:
            user_info = self._get_user_info(token_res.access_token)
        except MicrosoftApiError as e:
            return HTTPException(status_code=400, detail=e.message)
        return oauth_add_login(
            session, self.name, user, token_res.access_token, user_info["email"]
        )


class Outlook(ServiceClass):
    """Outlook services automation."""

    def __init__(self) -> None:
        super().__init__(
            "Microsoft Outlook Service",
            "mail",
            "#0078D4",
            "/images/Outlook_logo.webp",
            True,
        )

    class new_email_sent(Action):
        """Trigger when new email is sent."""

        service: "Outlook"

        def __init__(self) -> None:
            config_schema = [
                {"name": "to", "type": "input", "values": []},
                {"name": "subject", "type": "input", "values": []},
            ]
            super().__init__("Triggered when new email is sent", config_schema)

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            token: str = get_user_service_token(session, user_id, self.service.name)
            # receiver_filter = get_component(area_action.config, "to", "values")
            # subject_filter = get_component(area_action.config, "subject", "values")

            try:
                message: Dict[str, Any] = self.service._get_latest_email(
                    token, folder="SentItems"
                )
                return self.service._compare_email_state(session, area_action, message)
            except MicrosoftApiError as e:
                logger.error(f"{self.service.name}: {e}")
                return False

    class new_email_inbox(Action):
        """Trigger when new email arrives."""

        service: "Outlook"

        def __init__(self) -> None:
            config_schema = [
                {"name": "from", "type": "input", "values": []},
                {"name": "subject", "type": "input", "values": []},
            ]
            super().__init__("Triggered when new email arrives", config_schema)

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            token: str = get_user_service_token(session, user_id, self.service.name)
            # sender_filter = get_component(area_action.config, "from", "values")
            # subject_filter = get_component(area_action.config, "subject", "values")

            try:
                message: Dict[str, Any] = self.service._get_latest_email(
                    token, folder="Inbox"
                )
                return self.service._compare_email_state(session, area_action, message)
            except MicrosoftApiError as e:
                logger.error(f"{self.service.name}: {e}")
                return False

    class send_email(Reaction):
        """Send email to specified recipient."""

        service: "Outlook"

        def __init__(self) -> None:
            config_schema = [
                {"name": "to", "type": "input", "values": []},
                {"name": "subject", "type": "input", "values": []},
                {"name": "body", "type": "input", "values": []},
            ]
            super().__init__("Send email to recipient", config_schema)

        def execute(self, session: Session, area_action: AreaReaction, user_id: int):
            try:
                token: str = get_user_service_token(session, user_id, self.service.name)
                to = get_component(area_action.config, "to", "values")
                subject = get_component(area_action.config, "subject", "values")
                body = get_component(area_action.config, "body", "values")

                url = "https://graph.microsoft.com/v1.0/me/sendMail"
                headers = {
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                }
                payload = {
                    "message": {
                        "subject": subject,
                        "body": {"contentType": "Text", "content": body},
                        "toRecipients": [{"emailAddress": {"address": to}}],
                    }
                }
                r = requests.post(url, headers=headers, data=json.dumps(payload))

                if r.status_code not in (200, 202):
                    raise MicrosoftApiError("Failed to send email")
                logger.debug(f"Outlook: Email sent to {to}")
            except MicrosoftApiError as e:
                logger.error(f"{self.service.name}: {e}")

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
        except MicrosoftApiError:
            return False

    def _get_token(self, code: str) -> MicrosoftOAuthTokenRes:
        url = f"https://login.microsoftonline.com/{settings.MICROSOFT_DIR_TENANT}/oauth2/v2.0/token"
        redirect = f"{settings.FRONT_URL}/callbacks/link/{self.name}"
        data = {
            "client_id": settings.MICROSOFT_CLIENT_ID,
            "client_secret": settings.MICROSOFT_CLIENT_SECRET,
            "code": code,
            "redirect_uri": redirect,
            "grant_type": "authorization_code",
        }
        r = requests.post(url, data=data)
        if r.status_code != 200:
            raise MicrosoftApiError(f"Failed to get Microsoft token: {r.text}")
        return MicrosoftOAuthTokenRes(**r.json())

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
        # last_state_values = (
        #     area_action.last_state.get("snippet", ""),
        #     area_action.last_state.get("historyId", ""),
        # )
        # message_values = (
        #     message.get("snippet", ""),
        #     message.get("historyId", ""),
        # )
        # if last_state_values == message_values:
        #     return False
        # area_action.last_state = message
        # session.add(area_action)
        # session.commit()
        return True

    def _get_latest_email(
        self,
        token: str,
        sender_filter: str = None,
        subject_filter: str = None,
        folder: str = "Inbox",
    ):
        query = ""
        if sender_filter:
            query += f"from/emailAddress/address eq '{sender_filter}'"
        if subject_filter:
            if len(query) > 0:
                query += " and "
            query += f"subject eq '{subject_filter}'"
        base_url = f"https://graph.microsoft.com/v1.0/me/mailFolders/{folder}/messages"
        params = {
            "$top": 1,
            "$orderby": f"{'receivedDateTime' if folder == 'Inbox' else 'sentDateTime'} desc",
        }
        headers = {"Authorization": f"Bearer {token}"}

        r = requests.get(base_url, headers=headers, params=params)

        if r.status_code != 200:
            raise MicrosoftApiError("Outlook: Failed to get messages")
        messages = r.json().get("value", [])
        return messages[0] if messages else None

    def _get_user_info(self, token: str) -> Dict[str, Any]:
        url = "https://graph.microsoft.com/v1.0/me"
        r = requests.get(url, headers={"Authorization": f"Bearer {token}"})
        logger.error(r.json())
        if r.status_code != 200:
            raise MicrosoftApiError("Invalid token or expired")
        return r.json()

    def oauth_link(self, state: str = None) -> str:
        base_url = f"https://login.microsoftonline.com/{settings.MICROSOFT_DIR_TENANT}/oauth2/v2.0/authorize"
        redirect = f"{settings.FRONT_URL}/callbacks/link/{self.name}"
        params = {
            "client_id": settings.MICROSOFT_CLIENT_ID,
            "response_type": "code",
            "redirect_uri": redirect,
            "scope": "offline_access Mail.Read Mail.Send User.Read",
            "state": state if state else generate_state(),
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
        except MicrosoftApiError as e:
            raise HTTPException(status_code=400, detail=e.message)

        return oauth_add_link(
            session, self.name, user, token_res.access_token, request, is_mobile
        )
