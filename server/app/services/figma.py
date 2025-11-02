# app/services/figma.py
from __future__ import annotations
from typing import Dict, Any, List
from sqlmodel import Session, select
from fastapi import HTTPException, Request, Response
from pydantic import BaseModel
import requests
import json
import re
from urllib.parse import urlencode
import base64
from core.logger import logger
from core.config import settings
from core.utils import generate_state
from services.services_classes import (
    Service as ServiceClass,
    Action,
    Reaction,
    get_component,
)
from services.oauth_lib import oauth_add_link
from models import AreaAction, AreaReaction, UserService, User, Service
from api.users.db import get_user_service_token


class FigmaApiError(Exception):
    def __init__(self, message: str, status_code: int | None = None):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class FigmaOAuthTokenRes(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int
    token_type: str
    user_id_string: str


class Figma(ServiceClass):
    def __init__(self) -> None:
        super().__init__("Figma", "design", "#0dc07b", "images/Figma_logo.png", True)

    class new_file_in_project(Action):
        """Triggered when a new file is added in a specific Figma project."""

        service: "Figma"

        def __init__(self):
            config_schema = [{"name": "Project URL", "type": "input", "values": []}]
            super().__init__(
                "Triggered when a new file appears in a project", config_schema
            )

        def check(self, session: Session, area_action: AreaAction, user_id: int):
            try:
                token: str = get_user_service_token(session, user_id, self.service.name)
                project_url: str = get_component(
                    area_action.config, "Project URL", "values"
                )
                project_id: str = self.service._parse_figma_url(project_url).get("id", "")
                logger.error(project_id)
                url = f"https://api.figma.com/v1/projects/{project_id}/files"
                headers = {"Authorization": f"Bearer {token}"}
                r = requests.get(url, headers=headers)
                if r.status_code != 200:
                    raise FigmaApiError(f"Failed to list project files: {r.text}")

                data = r.json()
                files = []
                for f in data.get("files", []):
                    if "key" in f:
                        files.append(f["key"])
                    elif "id" in f:
                        files.append(f["id"])
                last_files = (area_action.last_state or {}).get("files", [])
                new_files = [f for f in files if f not in last_files]

                area_action.last_state = {"files": files}
                session.add(area_action)
                session.commit()

                return len(new_files) > 0
            except FigmaApiError as e:
                logger.error(f"{self.service.name}: {e}")
                return False

    class new_comment_on_file(Action):
        """Triggered when a new comment is added to a specific file."""

        service: "Figma"

        def __init__(self):
            config_schema = [{"name": "File URL", "type": "input", "values": []}]
            super().__init__(
                "Triggered when a new comment is added on a file", config_schema
            )

        def check(self, session: Session, area_action: AreaAction, user_id: int):
            try:
                token: str = get_user_service_token(session, user_id, self.service.name)
                file_url: str = get_component(area_action.config, "File URL", "values")
                file_id: str = self.service._parse_figma_url(file_url).get("id")

                url = f"https://api.figma.com/v1/files/{file_id}/comments"
                headers = {"Authorization": f"Bearer {token}"}
                r = requests.get(url, headers=headers)
                if r.status_code != 200:
                    raise FigmaApiError(f"Failed to get comments: {r.text}")

                comments = [c["id"] for c in r.json().get("comments", [])]
                last_comments = (area_action.last_state or {}).get("comments", [])
                new_comments = [c for c in comments if c not in last_comments]

                area_action.last_state = {"comments": comments}
                session.add(area_action)
                session.commit()

                return len(new_comments) > 0
            except FigmaApiError as e:
                logger.error(f"{self.service.name}: {e}")
                return False

    class create_comment(Reaction):
        """Add a comment to a Figma file."""

        def __init__(self):
            config_schema = [
                {"name": "File URL", "type": "input", "values": []},
                {"name": "Comment Text", "type": "input", "values": []},
            ]
            super().__init__("Add a comment to a file", config_schema)

        def execute(self, session: Session, area_reaction: AreaReaction, user_id: int):
            try:
                token: str = get_user_service_token(session, user_id, self.service.name)
                file_url: str = get_component(area_reaction.config, "File URL", "values")
                text: str = get_component(
                    area_reaction.config, "Comment Text", "values"
                )
                file_id: str = self.service._parse_figma_url(file_url).get("id")

                url = f"https://api.figma.com/v1/files/{file_id}/comments"
                headers = {
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                }
                payload = {"message": text}
                r = requests.post(url, headers=headers, data=json.dumps(payload))
                if r.status_code != 200:
                    raise FigmaApiError(f"Failed to create comment: {r.text}")

                logger.debug(
                    f"{self.service.name}: comment added on file {file_id} for user {user_id}"
                )
            except FigmaApiError as e:
                logger.error(f"{self.service.name}: {e}")

    def _parse_figma_url(self, url: str) -> Dict[str, str]:
        patterns = {
            "file": r"figma\.com/(?:file|design)/([a-zA-Z0-9]+)",
            "project": r"figma\.com/(?:projects?|files/team/[a-zA-Z0-9]+/project)/([a-zA-Z0-9]+)",
            "team": r"figma\.com/team/([a-zA-Z0-9]+)",
            "team_files": r"figma\.com/files/team/([a-zA-Z0-9]+)",
        }

        for key, pattern in patterns.items():
            match = re.search(pattern, url)
            if match:
                return {"type": key, "id": match.group(1)}

        return {"type": "", "id": ""}

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

    def _is_token_valid(self, token: str) -> bool:
        try:
            self._get_user_info(token)
            return True
        except FigmaApiError:
            return False

    def oauth_link(self, state: str = None) -> str:
        base_url = "https://www.figma.com/oauth"
        redirect = f"{settings.FRONT_URL}/callbacks/link/{self.name}"
        params = {
            "client_id": settings.FIGMA_CLIENT_ID,
            "redirect_uri": redirect,
            "scope": "file_content:read file_comments:write file_comments:read current_user:read projects:read",
            "state": state if state else generate_state(),
            "response_type": "code",
        }
        return f"{base_url}?{urlencode(params)}"

    def _get_user_info(self, token: str) -> Dict[str, Any]:
        url = "https://api.figma.com/v1/me"
        headers = {"Authorization": f"Bearer {token}"}
        r = requests.get(url, headers=headers)
        if r.status_code != 200:
            raise FigmaApiError(f"Failed to get Figma user info: {r.text}")
        return r.json()

    def _get_token(self, code: str) -> FigmaOAuthTokenRes:
        url = "https://api.figma.com/v1/oauth/token"
        redirect = f"{settings.FRONT_URL}/callbacks/link/{self.name}"
        auth_str = f"{settings.FIGMA_CLIENT_ID}:{settings.FIGMA_CLIENT_SECRET}"
        b64_auth = base64.b64encode(auth_str.encode()).decode()
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {b64_auth}",
        }
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect,
        }
        r = requests.post(url, headers=headers, data=data)
        if r.status_code != 200:
            logger.error(f"Figma token error: {r.status_code} {r.text}")
            raise FigmaApiError("Failed to exchange code for token")
        return FigmaOAuthTokenRes(**r.json())

    def oauth_callback(
        self,
        session: Session,
        code: str,
        user: User,
        request: Request | None = None,
        is_mobile: bool = False,
    ) -> Response:
        if not user:
            raise HTTPException(status_code=400, detail="User must be authenticated")
        try:
            token_data = self._get_token(code)
            return oauth_add_link(
                session, self.name, user, token_data.access_token, request, is_mobile
            )
        except FigmaApiError as e:
            raise HTTPException(status_code=400, detail=e.message)
