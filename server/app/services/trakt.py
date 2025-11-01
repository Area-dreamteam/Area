from datetime import datetime
from urllib.parse import urlencode
from pydantic import BaseModel

from core.config import settings
from core.logger import logger
from core.utils import generate_state
from fastapi import HTTPException, Request, Response
from models import AreaAction, Service, User, UserService
from services.area_api import AreaApi
from services.oauth_lib import oauth_add_link
from services.services_classes import (
    Service as ServiceClass,
    Action,
    get_component,
)
from sqlmodel import Session, select


class TraktApiError(Exception):
    """Trakt API-specific errors."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class TraktOAuthTokenRes(BaseModel):
    """Trakt OAuth token response format."""

    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str


class TraktApi(AreaApi):
    def __init__(self):
        super().__init__(TraktApiError)

    def test_movie(self, token) -> bool:
        res = self.get(
            "https://api.trakt.tv/movies/the-nightmare-before-christmas-1993",
            headers={
                "User-Agent": "Area/0.0.1",
                "Content-Type": "application/json",
                "trakt-api-key": settings.TRAKT_CLIENT_ID,
                "trakt-api-version": 2,
                "Authorization": f"Bearer {token}"
            },
        )
        logger.debug(f"test movie {res}")
        return True

    def get_token(self, code: str) -> TraktOAuthTokenRes:
        url = "https://api.trakt.tv/oauth/token"
        redirect = f"{settings.FRONT_URL}/callbacks/link/Trakt"
        data = {
            "code": code,
            "client_id": settings.TRAKT_CLIENT_ID,
            "client_secret": settings.TRAKT_CLIENT_SECRET,
            "redirect_uri": redirect,
            "grant_type": "authorization_code",
        }
        headers = {
            "User-Agent": "AreaApp/0.0.1",
            "Content-Type": "application/json",
            "trakt-api-key": settings.TRAKT_CLIENT_ID,
            "trakt-api-version": "2",
        }

        try:
            res = self.post(url, data=data, headers=headers)
        except TraktApiError as e:
            logger.error(f"Trakt token error: {e.message}")
            raise e

        return TraktOAuthTokenRes(**res)


trakt_api = TraktApi()


class Trakt(ServiceClass):
    def __init__(self) -> None:
        super().__init__("Service Trakt", "Movie", "#9F42C6", "images/Trakt_logo.webp", True)

    # class if_temperature_rise_above(Action):
    #     def __init__(self) -> None:
    #         config_schema = [
    #             {
    #                 "name": "temperature_limit",
    #                 "type": "input",
    #                 "values": [],
    #             }
    #         ]
    #         super().__init__(
    #             "Check if temperature rise above a certain limit",
    #             config_schema,
    #         )

    #     def check(
    #         self, session: Session, area_action: AreaAction, user_id: int
    #     ) -> bool:
    #         temperature_limit = int(
    #             get_component(area_action.config, "temperature_limit", "values")
    #         )
    #         longitude = get_component(area_action.config, "longitude", "values")
    #         latitude = get_component(area_action.config, "latitude", "values")
    #         timezone = get_component(area_action.config, "timezone", "values")

    #         current_temperature = open_meteo_api.get_current_temperature(latitude, longitude, timezone)

    #         return current_temperature > temperature_limit

    # class if_temperature_fall_bellow(Action):
    #     def __init__(self) -> None:
    #         config_schema = [
    #             {
    #                 "name": "temperature_limit",
    #                 "type": "input",
    #                 "values": [],
    #             }
    #         ]
    #         super().__init__(
    #             "Check if temperature fall bellow a certain limit",
    #             config_schema,
    #         )

    #     def check(
    #         self, session: Session, area_action: AreaAction, user_id: int
    #     ) -> bool:
    #         temperature_limit = int(
    #             get_component(area_action.config, "temperature_limit", "values")
    #         )
    #         longitude = get_component(area_action.config, "longitude", "values")
    #         latitude = get_component(area_action.config, "latitude", "values")
    #         timezone = get_component(area_action.config, "timezone", "values")

    #         current_temperature = open_meteo_api.get_current_temperature(latitude, longitude, timezone)

    #         return current_temperature < temperature_limit

    def oauth_link(self, state: str = None) -> str:
        base_url = "https://api.trakt.tv/oauth/authorize"
        redirect = f"{settings.FRONT_URL}/callbacks/link/Trakt"
        params = {
            "response_type": "code",
            "client_id": settings.TRAKT_CLIENT_ID,
            "redirect_uri": redirect,
            "state": state,
        }
        return f"{base_url}?{urlencode(params)}"

    def _is_token_valid(self, token: str) -> bool:
        try:
            trakt_api.test_movie(token)
            return True
        except TraktApiError:
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
        return True

    def oauth_callback(
        self,
        session: Session,
        code: str,
        user: User | None,
        request: Request = None,
        is_mobile: bool = False,
    ) -> Response:
        try:
            token_res = trakt_api.get_token(code)
        except TraktApiError as e:
            raise HTTPException(status_code=400, detail=e.message)

        return oauth_add_link(session, self.name, user, token_res.access_token)
