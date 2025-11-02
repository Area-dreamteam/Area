import requests
from urllib.parse import urlencode
from sqlmodel import Session, select
from fastapi import HTTPException, Response, Request
from typing import Dict, Any
from pydantic import BaseModel

from core.config import settings
from core.logger import logger
from services.oauth_lib import oauth_add_link
from services.services_classes import (
    Service as ServiceClass,
    Action,
    Reaction,
    get_component,
)
from models import AreaAction, UserService, Service, User, AreaReaction
from api.users.db import get_user_service_token


class CalendlyOAuthTokenRes(BaseModel):
    """Calendly OAuth token response format."""

    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str
    scope: str


class CalendlyApiError(Exception):
    """Calendly API-specific errors."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class Calendly(ServiceClass):
    """Calendly automation service."""

    def __init__(self) -> None:
        super().__init__(
            "Calendly", "productivity", "#006BFF", "images/Calendly_logo.webp", True
        )

    class new_event_scheduled(Action):
        """Triggered when a new event is scheduled."""

        service: "Calendly"

        def __init__(self):
            config_schema = []
            super().__init__("Triggered when a new event is scheduled", config_schema)

        def check(self, session: Session, area_action: AreaAction, user_id: int):
            try:
                token: str = get_user_service_token(session, user_id, self.service.name)
                user_data = self.service._get_user_info(token)
                user_uri: str = user_data.get("uri", "")
                url: str = "https://api.calendly.com/scheduled_events"
                headers = {
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                }
                params = {"user": user_uri}
                r = requests.get(url, headers=headers, params=params)
                if r.status_code != 200:
                    raise CalendlyApiError(f"Failed to fetch events: {r.text}")

                events = [
                    event["event_type"] for event in r.json().get("collection", [])
                ]
                last_events = (area_action.last_state or {}).get("events", [])

                new_events = [e for e in events if e not in last_events]
                area_action.last_state = {"events": events}
                session.add(area_action)
                session.commit()

                return len(new_events) > 0
            except CalendlyApiError as e:
                logger.error(f"{self.service.name}: {e}")
                return False

    class event_cancelled(Action):
        """Triggered when an event is cancelled."""

        service: "Calendly"

        def __init__(self):
            super().__init__("Triggered when an event is cancelled", [])

        def check(self, session: Session, area_action: AreaAction, user_id: int):
            try:
                token = get_user_service_token(session, user_id, self.service.name)
                user_data = self.service._get_user_info(token)
                user_uri: str = user_data.get("uri", "")
                url: str = "https://api.calendly.com/scheduled_events"
                headers = {
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                }
                params = {
                    "sort": "start_time:desc",
                    "status": "canceled",
                    "user": user_uri,
                }
                r = requests.get(url, headers=headers, params=params)
                if r.status_code != 200:
                    raise CalendlyApiError(
                        f"Failed to fetch cancelled events: {r.text}"
                    )

                cancelled_events = [
                    event["uri"] for event in r.json().get("collection", [])
                ]
                last_cancelled = (area_action.last_state or {}).get(
                    "cancelled_events", []
                )

                new_cancelled = [
                    event for event in cancelled_events if event not in last_cancelled
                ]
                area_action.last_state = {"cancelled_events": cancelled_events}
                session.add(area_action)
                session.commit()

                return len(new_cancelled) > 0
            except CalendlyApiError as e:
                logger.error(f"{self.service.name}: {e}")
                return False

    class create_meeting(Reaction):
        """Create a new meeting event."""

        service: "Calendly"

        def __init__(self):
            config_schema = [
                {"name": "Event name", "type": "input", "values": []},
                {"name": "Duration (minutes)", "type": "input", "values": []},
                {"name": "Description", "type": "input", "values": []},
            ]
            super().__init__("Create a new meeting event", config_schema)

        def execute(self, session: Session, area_action: AreaReaction, user_id: int):
            try:
                token = get_user_service_token(session, user_id, self.service.name)
                event_name = get_component(area_action.config, "Event name", "values")
                try:
                    duration: int = get_component(
                        area_action.config, "Duration (minutes)", "values"
                    )
                except Exception:
                    raise CalendlyApiError("Invalid duration value")
                description = get_component(area_action.config, "Description", "values")

                user_data = self.service._get_user_info(token)
                user_uri = user_data.get("uri", "")

                url = "https://api.calendly.com/event_types"
                headers = {
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                }
                data = {
                    "name": event_name,
                    "duration": duration,
                    "description": description,
                    "location": {"type": "online"},
                    "type": "standard",
                    "active": True,
                    "owner": user_uri,
                }
                r = requests.post(url, headers=headers, json=data)
                if r.status_code != 201:
                    raise CalendlyApiError(f"Failed to create event: {r.text}")
                logger.info(f"{self.service.name} - {self.name} - Created event '{event_name}' - User: {user_id}")
            except CalendlyApiError as e:
                logger.error(f"{self.service.name}: {e}")

    def is_connected(self, session: Session, user_id: int) -> bool:
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
        if self._is_token_valid(user_service.access_token):
            return True
        if user_service.refresh_token is None:
            return False
        return True

    def _is_token_valid(self, token: str) -> bool:
        try:
            self._get_user_info(token)
            return True
        except CalendlyApiError:
            return False

    def oauth_link(self, state: str | None = None) -> str:
        base_url = "https://auth.calendly.com/oauth/authorize"
        redirect = f"{settings.FRONT_URL}/callbacks/link/{self.name}"
        params = {
            "client_id": settings.CALENDLY_CLIENT_ID,
            "response_type": "code",
            "redirect_uri": redirect,
            "scope": "default",
        }
        return f"{base_url}?{urlencode(params)}"

    def _get_token(self, code: str) -> CalendlyOAuthTokenRes:
        url = "https://auth.calendly.com/oauth/token"
        redirect = f"{settings.FRONT_URL}/callbacks/link/{self.name}"
        data = {
            "code": code,
            "grant_type": "authorization_code",
            "client_id": settings.CALENDLY_CLIENT_ID,
            "client_secret": settings.CALENDLY_CLIENT_SECRET,
            "redirect_uri": redirect,
        }
        r = requests.post(url, data=data)
        if r.status_code != 200:
            logger.error(f"Calendly token error: {r.text}")
            raise CalendlyApiError(f"Failed to get Calendly token: {r.text}")
        return CalendlyOAuthTokenRes(**r.json())

    def _get_user_info(self, token: str) -> Dict[str, Any]:
        url = "https://api.calendly.com/users/me"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        r = requests.get(url, headers=headers)
        if r.status_code != 200:
            raise CalendlyApiError(f"Failed to get Calendly user info: {r.text}")
        return r.json().get("resource", {})

    def oauth_callback(
        self,
        session: Session,
        code: str,
        user: User | None,
        request: Request | None = None,
        is_mobile: bool = False,
    ) -> Response:
        try:
            token_res = self._get_token(code)
        except CalendlyApiError as e:
            raise HTTPException(status_code=400, detail=e.message)

        if user:
            return oauth_add_link(session, self.name, user, token_res.access_token)
        else:
            raise HTTPException(status_code=400, detail="User not found")
