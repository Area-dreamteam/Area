from sqlmodel import Session
from pydantic import BaseModel
from pydantic_core import ValidationError
from sqlmodel import select
import requests
from urllib.parse import urlencode
from fastapi import HTTPException, Response, Request
from typing import Dict, Any, List

from core.utils import generate_state
from services.oauth_lib import oauth_add_link
from models import AreaAction, UserService, User, Service
from core.config import settings
from services.services_classes import (
    Service as ServiceClass,
    Action,
    Reaction,
    get_component,
)
from core.logger import logger
from api.users.db import get_user_service_token
from core.categories import ServiceCategory


class GoogleOAuthTokenRes(BaseModel):
    """Google OAuth token response format."""

    access_token: str
    token_type: str
    refresh_token: str
    expires_in: int


class GoogleCalendarApiError(Exception):
    """Google API-specific errors."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class GoogleCalendar(ServiceClass):
    def __init__(self) -> None:
        super().__init__(
            "Service email de Google",
            ServiceCategory.CALENDAR,
            "#4285F4",
            "/images/GoogleCalendar_logo.webp",
            True,
        )

    class new_event_created(Action):
        """Triggered when a new event is created in Google Calendar."""

        service: "GoogleCalendar"

        def __init__(self):
            config_schema = [{"name": "Calendar name", "type": "input", "values": []}]
            super().__init__("Triggered when a new event is created", config_schema)

        def check(self, session, area_action, user_id):
            try:
                token = get_user_service_token(session, user_id, self.service.name)
                calendar_name = get_component(
                    area_action.config, "Calendar name", "values"
                )
                calendar_id: int = self.service._find_calendar_id(token, calendar_name)
                url = f"https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events"
                headers = {"Authorization": f"Bearer {token}"}
                r = requests.get(url, headers=headers)
                if r.status_code != 200:
                    raise GoogleCalendarApiError(
                        f"Failed to fetch calendar events: {r.text}"
                    )
                events = r.json().get("items", [])
                latest_event_id = events[-1] if events else None
            except GoogleCalendarApiError as e:
                logger.error(f"{self.service.name}: {e}")
            return self.service._compare_data(session, area_action, latest_event_id)

    class create_event(Reaction):
        """Create a new event in Google Calendar."""

        service: "GoogleCalendar"

        def __init__(self):
            config_schema = [
                {"name": "Calendar name", "type": "input", "values": []},
                {"name": "Summary", "type": "input", "values": []},
                {
                    "name": "Start Time (format: YYYY-MM-DD)",
                    "type": "input",
                    "values": [],
                },
                {
                    "name": "End Time (format: YYYY-MM-DD)",
                    "type": "input",
                    "values": [],
                },
            ]
            super().__init__("Create a new event in Google Calendar", config_schema)

        def execute(self, session, area_reaction, user_id):
            try:
                token = get_user_service_token(session, user_id, self.service.name)
                calendar_name = get_component(
                    area_reaction.config, "Calendar name", "values"
                )
                summary = get_component(area_reaction.config, "Summary", "values")
                start_time = get_component(
                    area_reaction.config, "Start Time (format: YYYY-MM-DD)", "values"
                )
                end_time = get_component(
                    area_reaction.config, "End Time (format: YYYY-MM-DD)", "values"
                )
                calendar_id: int = self.service._find_calendar_id(token, calendar_name)
                url = f"https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events"
                headers = {
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                }
                body = {
                    "summary": summary,
                    "start": {"date": start_time},
                    "end": {"date": end_time},
                }
                r = requests.post(url, headers=headers, json=body)
                if r.status_code != 200:
                    raise GoogleCalendarApiError(f"Failed to create event: {r.text}")
            except GoogleCalendarApiError as e:
                logger.error(f"{self.service.name}: {e}")

    class create_event_detail(Reaction):
        """Create a new event in Google Calendar."""

        service: "GoogleCalendar"

        def __init__(self):
            config_schema = [
                {"name": "Calendar name", "type": "input", "values": []},
                {"name": "Summary", "type": "input", "values": []},
                {
                    "name": "Start Time (format: YYYY-MM-DDTHH:MM:SS±HH:MM)",
                    "type": "input",
                    "values": [],
                },
                {
                    "name": "End Time (format: YYYY-MM-DDTHH:MM:SS±HH:MM)",
                    "type": "input",
                    "values": [],
                },
            ]
            super().__init__("Create a new event in Google Calendar", config_schema)

        def execute(self, session, area_reaction, user_id):
            try:
                token = get_user_service_token(session, user_id, self.service.name)
                calendar_name = get_component(
                    area_reaction.config, "Calendar name", "values"
                )
                summary = get_component(area_reaction.config, "Summary", "values")
                start_time = get_component(
                    area_reaction.config,
                    "Start Time (format: YYYY-MM-DDTHH:MM:SS±HH:MM)",
                    "values",
                )
                end_time = get_component(
                    area_reaction.config,
                    "End Time (format: YYYY-MM-DDTHH:MM:SS±HH:MM)",
                    "values",
                )
                calendar_id: int = self.service._find_calendar_id(token, calendar_name)
                url = f"https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events"
                headers = {
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                }
                body = {
                    "summary": summary,
                    "start": {"dateTime": start_time},
                    "end": {"dateTime": end_time},
                }
                r = requests.post(url, headers=headers, json=body)
                if r.status_code != 200:
                    raise GoogleCalendarApiError(f"Failed to create event: {r.text}")
            except GoogleCalendarApiError as e:
                logger.error(f"{self.service.name}: {e}")

    def _list_user_calendars(self, access_token: str) -> List[Dict[str, Any]]:
        url = "https://www.googleapis.com/calendar/v3/users/me/calendarList"
        headers = {"Authorization": f"Bearer {access_token}"}
        params = {"minAccessRole": "reader", "maxResults": 250}
        r = requests.get(url, headers=headers, params=params)
        data = r.json()
        return data.get("items", [])

    def _find_calendar_id(self, access_token: str, name: str = None) -> str:
        calendars = self._list_user_calendars(access_token)
        if name:
            name_low = name.strip().lower()
            for cal in calendars:
                if name_low in cal.get("summary", "").lower():
                    return cal["id"]
        for cal in calendars:
            if cal.get("primary") is True:
                return cal["id"]
        return "primary"

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
        except GoogleCalendarApiError:
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
            raise GoogleCalendarApiError("Failed to retrieve Google token")
        try:
            return GoogleOAuthTokenRes(**r.json())
        except ValidationError:
            raise GoogleCalendarApiError("Invalid Google OAuth response")

    def _get_user_info(self, token: str) -> Dict[str, Any]:
        url = "https://www.googleapis.com/oauth2/v2/userinfo"
        r = requests.get(url, headers={"Authorization": f"Bearer {token}"})
        if r.status_code != 200:
            raise GoogleCalendarApiError("Failed to fetch user info")
        return r.json()

    def oauth_link(self, state: str = None) -> str:
        """Generate Google OAuth authorization URL."""
        base_url = "https://accounts.google.com/o/oauth2/v2/auth"
        redirect = f"{settings.FRONT_URL}/callbacks/link/{self.name}"
        params = {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "redirect_uri": redirect,
            "response_type": "code",
            "scope": "https://www.googleapis.com/auth/userinfo.email  https://www.googleapis.com/auth/calendar  https://www.googleapis.com/auth/calendar.readonly  https://www.google.com/calendar/feeds",
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
        except GoogleCalendarApiError as e:
            raise HTTPException(status_code=400, detail=e.message)

        return oauth_add_link(
            session, self.name, user, token_res.access_token, request, is_mobile
        )
