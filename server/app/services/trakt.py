from datetime import datetime
from urllib.parse import urlencode
from pydantic import BaseModel

from core.config import settings
from core.logger import logger
from core.utils import generate_state
from api.users.db import get_user_service_token
from core.categories import ServiceCategory
from fastapi import HTTPException, Request, Response
from models import AreaAction, Service, User, UserService, AreaReaction
from services.area_api import AreaApi
from services.oauth_lib import oauth_add_link
from services.services_classes import (
    Service as ServiceClass,
    Action,
    Reaction,
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
                "trakt-api-version": "2",
                "Authorization": f"Bearer {token}",
            },
        )
        logger.debug(f"test movie {res}")
        return True
    
    def get_movie(self, token, name):
        res = self.get(
            f"https://api.trakt.tv/movies/{name}",
            headers={
                "User-Agent": "Area/0.0.1",
                "Content-Type": "application/json",
                "trakt-api-key": settings.TRAKT_CLIENT_ID,
                "trakt-api-version": "2",
                "Authorization": f"Bearer {token}",
            },
        )
        
        return res
    
    def add_to_favorite(self, token, name):
        movie = self.get_movie(token, name)
        
        self.post(
            "https://api.trakt.tv/sync/favorites",
            headers={
                "User-Agent": "Area/0.0.1",
                "Content-Type": "application/json",
                "trakt-api-key": settings.TRAKT_CLIENT_ID,
                "trakt-api-version": "2",
                "Authorization": f"Bearer {token}",
            },
            data={
                "movies": [movie]
            },
            good_status_code=[201]
        )
        
    def remove_from_favorite(self, token, name):
        movie = self.get_movie(token, name)
        
        self.post(
            "https://api.trakt.tv/sync/favorites/remove",
            headers={
                "User-Agent": "Area/0.0.1",
                "Content-Type": "application/json",
                "trakt-api-key": settings.TRAKT_CLIENT_ID,
                "trakt-api-version": "2",
                "Authorization": f"Bearer {token}",
            },
            data={
                "movies": [movie]
            },
            good_status_code=[200]
        )
        
    def add_to_watchlist(self, token, name):
        movie = self.get_movie(token, name)
        
        self.post(
            "https://api.trakt.tv/sync/watchlist",
            headers={
                "User-Agent": "Area/0.0.1",
                "Content-Type": "application/json",
                "trakt-api-key": settings.TRAKT_CLIENT_ID,
                "trakt-api-version": "2",
                "Authorization": f"Bearer {token}",
            },
            data={
                "movies": [movie]
            },
            good_status_code=[201]
        )

    def get_profile(self, token):
        res = self.get(
            "https://api.trakt.tv/users/settings",
            headers={
                "User-Agent": "Area/0.0.1",
                "Content-Type": "application/json",
                "trakt-api-key": settings.TRAKT_CLIENT_ID,
                "trakt-api-version": "2",
                "Authorization": f"Bearer {token}",
            },
        )

        return res

    def get_username(self, token):
        return self.get_profile(token)["user"]["username"]

    def get_watchlist(self, token):
        res = self.get(
            "https://api.trakt.tv/sync/watchlist/movies/added/asc",
            headers={
                "User-Agent": "Area/0.0.1",
                "Content-Type": "application/json",
                "trakt-api-key": settings.TRAKT_CLIENT_ID,
                "trakt-api-version": "2",
                "Authorization": f"Bearer {token}",
            },
        )
        return res
    
    def get_watch_history(self, token):
        res = self.get(
            "https://api.trakt.tv/sync/history/movies",
            headers={
                "User-Agent": "Area/0.0.1",
                "Content-Type": "application/json",
                "trakt-api-key": settings.TRAKT_CLIENT_ID,
                "trakt-api-version": "2",
                "Authorization": f"Bearer {token}",
            },
        )
        return res

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
        super().__init__("Service Trakt", ServiceCategory.MOVIE, "#2596be", "", True)

    class new_movie_in_watchlist(Action):
        def __init__(self) -> None:
            super().__init__("Check if a movie was added to watchlist")

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            token = get_user_service_token(session, user_id, self.service.name)
            last_state = area_action.last_state

            watchlist = trakt_api.get_watchlist(token)
            if not watchlist:
                return False

            last_movie_title = watchlist[0]["movie"]["title"]

            if (
                last_state is None
                or "last_movie_title" not in last_state
                or last_state["last_movie_title"] != last_movie_title
            ):
                area_action.last_state = {"last_movie_title": last_movie_title}
                session.add(area_action)
                session.commit()
                return True

            return False

    class new_movie_watched(Action):
        def __init__(self) -> None:
            super().__init__("Check if a new movie was watched")

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            token = get_user_service_token(session, user_id, self.service.name)
            last_state = area_action.last_state

            watch_history = trakt_api.get_watch_history(token)
            if not watch_history:
                return False

            last_movie_title = watch_history[0]["movie"]["title"]

            if (
                last_state is None
                or "last_movie_title" not in last_state
                or last_state["last_movie_title"] != last_movie_title
            ):
                area_action.last_state = {"last_movie_title": last_movie_title}
                session.add(area_action)
                session.commit()
                return True

            return False
        
    class add_to_favorite(Reaction):
        def __init__(self) -> None:
            config_schema = [
                {
                    "name": "movie_title",
                    "type": "input",
                    "values": [],
                }
            ]
            super().__init__("Add a movie to favorite", config_schema)

        def execute(self, session: Session, area_action: AreaReaction, user_id: int):  # type: ignore
            try:
                token = get_user_service_token(session, user_id, self.service.name)
                movie_name = get_component(area_action.config, "movie_title", "values")
                
                trakt_api.add_to_favorite(token, movie_name)
                
                logger.info(f'{self.service.name}: Add "{movie_name}" to favorite')

            except TraktApiError as e:
                logger.error(f'{self.service.name}: {e.message}')
                
    class remove_from_favorite(Reaction):
        def __init__(self) -> None:
            config_schema = [
                {
                    "name": "movie_title",
                    "type": "input",
                    "values": [],
                }
            ]
            super().__init__("Remove a movie from favorite", config_schema)

        def execute(self, session: Session, area_action: AreaReaction, user_id: int):  # type: ignore
            try:
                token = get_user_service_token(session, user_id, self.service.name)
                movie_name = get_component(area_action.config, "movie_title", "values")
                
                trakt_api.remove_from_favorite(token, movie_name)
                
                logger.info(f'{self.service.name}: Removed "{movie_name}" from favorite')

            except TraktApiError as e:
                logger.error(f'{self.service.name}: {e.message}')
                
    class add_to_watchlist(Reaction):
        def __init__(self) -> None:
            config_schema = [
                {
                    "name": "movie_title",
                    "type": "input",
                    "values": [],
                }
            ]
            super().__init__("Add a movie to watchlist", config_schema)

        def execute(self, session: Session, area_action: AreaReaction, user_id: int):  # type: ignore
            try:
                token = get_user_service_token(session, user_id, self.service.name)
                movie_name = get_component(area_action.config, "movie_title", "values")
                
                trakt_api.add_to_watchlist(token, movie_name)
                
                logger.info(f'{self.service.name}: Add "{movie_name}" to watchlist')

            except TraktApiError as e:
                logger.error(f'{self.service.name}: {e.message}')

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
