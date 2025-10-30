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


class StravaOAuthTokenRes(BaseModel):
    """Strava OAuth token response format."""

    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str


class StravaApiError(Exception):
    """Strava API-specific errors."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class Strava(ServiceClass):
    """Strava automation service."""

    def __init__(self) -> None:
        super().__init__(
            "Strava", "fitness", "#fc4c02", "images/Strava_logo.webp", True
        )

    class new_activity_by_you(Action):
        """Triggered when a new activity is uploaded."""

        service: "Strava"

        def __init__(self):
            config_schema = []
            super().__init__("Triggered when a new activity is recorded", config_schema)

        def check(self, session, area_action, user_id):
            try:
                token = get_user_service_token(session, user_id, self.service.name)
                url = "https://www.strava.com/api/v3/athlete/activities"
                params = {"per_page": 1}
                r = requests.get(
                    url, headers={"Authorization": f"Bearer {token}"}, params=params
                )
                if r.status_code != 200:
                    raise StravaApiError("Failed to fetch activities")

                activity = r.json()[0] if r.json() else None
            except StravaApiError as e:
                logger.error(f"{self.service.name}: {e}")
            return self.service._compare_data(session, area_action, activity)

    class new_routes_by_you(Action):
        """Triggered when a new routes is uploaded."""

        service: "Strava"

        def __init__(self):
            config_schema = []
            super().__init__("Triggered when a new routes is recorded", config_schema)

        def check(self, session, area_action, user_id):
            try:
                token = get_user_service_token(session, user_id, self.service.name)
                user_info = self.service._get_user_info(token)
                athlete_id: int = user_info.get("id", "")
                url = f"https://www.strava.com/api/v3/athletes/{athlete_id}/routes"
                params = {"per_page": 1}
                r = requests.get(
                    url, headers={"Authorization": f"Bearer {token}"}, params=params
                )
                logger.error(r.json())
                if r.status_code != 200:
                    raise StravaApiError("Failed to fetch activities")

                activity = r.json()[0] if r.json() else None
            except StravaApiError as e:
                logger.error(f"{self.service.name}: {e}")
            return self.service._compare_data(session, area_action, activity)

    class new_club_by_you(Action):
        """Triggered when a new club is create in your Strava account."""

        service: "Strava"

        def __init__(self):
            config_schema = []
            super().__init__(
                "Triggered when a new club is create in your Strava account",
                config_schema,
            )

        def check(self, session, area_action, user_id):
            try:
                token = get_user_service_token(session, user_id, self.service.name)
                url = "https://www.strava.com/api/v3/athlete/clubs"
                r = requests.get(url, headers={"Authorization": f"Bearer {token}"})
                if r.status_code != 200:
                    raise StravaApiError("Failed to fetch athlete clubs")
                logger.error(r.json())
                club = r.json()[-1] if r.json() else None
                logger.error(club)
            except StravaApiError as e:
                logger.error(f"{self.service.name}: {e}")
            return self.service._compare_data(session, area_action, club)

    class create_activity(Reaction):
        """Create a manual activity on Strava."""

        service: "Strava"

        def __init__(self):
            config_schema = [
                {"name": "name", "type": "input", "values": []},
                {"name": "description", "type": "input", "values": []},
                {"name": "type", "type": "select", "values": ["Ride", "Run", "Walk"]},
                {"name": "elapsed_time(seconds)", "type": "input", "values": []},
            ]
            super().__init__("Create a new manual activity", config_schema)

        def execute(self, session, area_reaction, user_id):
            try:
                token = get_user_service_token(session, user_id, self.service.name)
                name = get_component(area_reaction.config, "name", "values")
                type = get_component(area_reaction.config, "type", "values")
                try:
                    elapsed: int = get_component(
                        area_reaction.config, "elapsed_time(seconds)", "values"
                    )
                except Exception:
                    elapsed: int = 0
                desc = get_component(area_reaction.config, "description", "values")

                url = "https://www.strava.com/api/v3/activities"
                data = {
                    "name": name,
                    "type": type,
                    "elapsed_time": int(elapsed),
                    "description": desc,
                    "start_date_local": datetime.now(timezone.utc).isoformat(),
                }
                r = requests.post(
                    url, headers={"Authorization": f"Bearer {token}"}, data=data
                )
                if r.status_code != 201:
                    raise StravaApiError(f"Failed to create activity: {r.text}")
                logger.debug("Strava: created new activity for user {user_id}")
            except StravaApiError as e:
                logger.error(f"{self.service.name}: {e}")

    class update_weight(Reaction):
        """Update your weight on Strava."""

        service: "Strava"

        def __init__(self):
            config_schema = [
                {"name": "new_weight", "type": "input", "values": []},
            ]
            super().__init__("Update your weight on Strava", config_schema)

        def execute(self, session, area_reaction, user_id):
            try:
                token = get_user_service_token(session, user_id, self.service.name)
                try:
                    new_weight: float = float(
                        get_component(area_reaction.config, "new_weight", "values")
                    )
                except Exception:
                    raise StravaApiError("Incorrect weight value")

                url = "https://www.strava.com/api/v3/athlete"
                data = {
                    "weight": new_weight,
                }
                r = requests.put(
                    url, headers={"Authorization": f"Bearer {token}"}, data=data
                )
                if r.status_code != 200:
                    raise StravaApiError(f"Failed to update weight: {r.text}")
                logger.debug("Strava: update weight for user {user_id}")
            except StravaApiError as e:
                logger.error(f"{self.service.name}: {e}")

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
        except StravaApiError:
            return False

    def oauth_link(self, state: str = None) -> str:
        base_url = "https://www.strava.com/oauth/authorize"
        redirect = f"{settings.FRONT_URL}/callbacks/link/{self.name}"
        params = {
            "client_id": settings.STRAVA_CLIENT_ID,
            "response_type": "code",
            "state": state if state else generate_state(),
            "redirect_uri": redirect,
            "approval_prompt": "auto",
            "scope": "read,activity:read_all,profile:read_all,activity:write,profile:write",
        }
        return f"{base_url}?{urlencode(params)}"

    def _get_token(self, code: str) -> StravaOAuthTokenRes:
        url = "https://www.strava.com/oauth/token"
        data = {
            "client_id": settings.STRAVA_CLIENT_ID,
            "client_secret": settings.STRAVA_CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code",
        }
        r = requests.post(url, data=data)
        if r.status_code != 200:
            logger.error(f"Strava token error: {r.text}")
            raise StravaApiError(f"Failed to get Strava token: {r.text}")
        return StravaOAuthTokenRes(**r.json())

    def _get_user_info(self, token: str) -> Dict[str, Any]:
        url = "https://www.strava.com/api/v3/athlete"
        headers = {"Authorization": f"Bearer {token}"}
        r = requests.get(url, headers=headers)
        if r.status_code != 200:
            raise StravaApiError(f"Failed to get Strava user info: {r.text}")
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
        except StravaApiError as e:
            raise HTTPException(status_code=400, detail=e.message)

        return oauth_add_link(session, self.name, user, token_res.access_token)
