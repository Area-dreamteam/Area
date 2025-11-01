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
import json
from models import AreaAction, UserService, Service, User, AreaReaction
from api.users.db import get_user_service_token


class DropboxOAuthTokenRes(BaseModel):
    """Dropbox OAuth token response format."""

    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str
    scope: str
    account_id: str
    uid: str


class DropboxApiError(Exception):
    """Dropbox API-specific errors."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class Dropbox(ServiceClass):
    """Dropbox automation service."""

    def __init__(self) -> None:
        super().__init__(
            "Dropbox", "storage", "#0061FE", "images/Dropbox_logo.webp", True
        )

    class new_file_in_folder(Action):
        """Triggered when a new file is added in a specific folder."""

        service: "Dropbox"

        def __init__(self):
            config_schema = [{"name": "Folder path", "type": "input", "values": []}]
            super().__init__(
                "Triggered when a new file appears in a folder", config_schema
            )

        def check(self, session: Session, area_action: AreaAction, user_id: int):
            try:
                token: str = get_user_service_token(session, user_id, self.service.name)
                folder: str = get_component(area_action.config, "Folder path", "values")

                url: str = "https://api.dropboxapi.com/2/files/list_folder"
                headers = {
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                }
                data = {"path": folder, "limit": 15}
                r = requests.post(url, headers=headers, json=data)
                if r.status_code != 200:
                    raise DropboxApiError(f"Failed to list folder: {r.text}")

                files = [
                    entry["id"]
                    for entry in r.json().get("entries", [])
                    if entry[".tag"] == "file"
                ]
                last_files = (area_action.last_state or {}).get("files", [])

                new_files = [f for f in files if f not in last_files]
                area_action.last_state = {"files": files}
                session.add(area_action)
                session.commit()

                return len(new_files) > 0
            except DropboxApiError as e:
                logger.error(f"{self.service.name}: {e}")
                return False

    class new_text_file_in_folder(Action):
        """Triggered when a new text file is added in a specific folder."""

        service: "Dropbox"

        def __init__(self):
            config_schema = [{"name": "Folder path", "type": "input", "values": []}]
            super().__init__(
                "Triggered when a new text file appears in a folder", config_schema
            )

        def check(self, session: Session, area_action: AreaAction, user_id: int):
            try:
                token: str = get_user_service_token(session, user_id, self.service.name)
                folder: str = get_component(area_action.config, "Folder path", "values")

                url: str = "https://api.dropboxapi.com/2/files/list_folder"
                headers = {
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                }
                data = {"path": folder, "limit": 15}
                r = requests.post(url, headers=headers, json=data)
                if r.status_code != 200:
                    raise DropboxApiError(f"Failed to list folder: {r.text}")

                files = [
                    entry["id"]
                    for entry in r.json().get("entries", [])
                    if entry[".tag"] == "file" and entry["name"].endswith(".txt")
                ]
                last_files = (area_action.last_state or {}).get("files", [])

                new_files = [f for f in files if f not in last_files]
                area_action.last_state = {"files": files}
                session.add(area_action)
                session.commit()

                return len(new_files) > 0
            except DropboxApiError as e:
                logger.error(f"{self.service.name}: {e}")
                return False

    class new_shared_link(Action):
        """Triggered when a new shared file link is created."""

        service: "Dropbox"

        def __init__(self):
            super().__init__("Triggered when a file shared link is created", [])

        def check(self, session: Session, area_action: AreaAction, user_id: int):
            try:
                token = get_user_service_token(session, user_id, self.service.name)
                url = "https://api.dropboxapi.com/2/sharing/list_shared_links"
                headers = {
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                }
                data = {"direct_only": True}
                r = requests.post(url, headers=headers, json=data)
                if r.status_code != 200:
                    raise DropboxApiError(f"Failed to fetch shared links: {r.text}")

                links = [link["id"] for link in r.json().get("links", [])]
                prev = (area_action.last_state or {}).get("links", [])

                new_links = [link for link in links if link not in prev]
                area_action.last_state = {"links": links}
                session.add(area_action)
                session.commit()

                return len(new_links) > 0
            except DropboxApiError as e:
                logger.error(f"{self.service.name}: {e}")
                return False

    class create_text_file(Reaction):
        """Create a new text file in Dropbox."""

        def __init__(self):
            config_schema = [
                {"name": "File path", "type": "input", "values": []},
                {"name": "Content", "type": "input", "values": []},
            ]
            super().__init__("Create a new text file", config_schema)

        def execute(self, session: Session, area_reaction: AreaReaction, user_id: int):
            try:
                token: str = get_user_service_token(session, user_id, self.service.name)
                file_path: str = get_component(
                    area_reaction.config, "File path", "values"
                )
                content: str = get_component(area_reaction.config, "Content", "values")

                url: str = "https://content.dropboxapi.com/2/files/upload"
                headers = {
                    "Authorization": f"Bearer {token}",
                    "Dropbox-API-Arg": json.dumps({"path": file_path, "mode": "add"}),
                    "Content-Type": "application/octet-stream",
                }
                r = requests.post(url, headers=headers, data=content.encode("utf-8"))
                if r.status_code != 200:
                    raise DropboxApiError(f"Failed to create text file: {r.text}")
                logger.debug(
                    f"{self.service.name}: file create {file_path} for user {user_id}"
                )
            except DropboxApiError as e:
                logger.error(f"{self.service.name}: {e}")

    class move_file_or_folder(Reaction):
        """Move a Dropbox file or folder."""

        def __init__(self):
            config_schema = [
                {"name": "From path", "type": "input", "values": []},
                {"name": "To path", "type": "input", "values": []},
            ]
            super().__init__("Move a file or folder", config_schema)

        def execute(self, session: Session, area_reaction: AreaReaction, user_id: int):
            try:
                token: str = get_user_service_token(session, user_id, self.service.name)
                from_path: str = get_component(
                    area_reaction.config, "From path", "values"
                )
                to_path: str = get_component(area_reaction.config, "To path", "values")

                url = "https://api.dropboxapi.com/2/files/move_v2"
                headers = {
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                }
                data = {"from_path": from_path, "to_path": to_path}

                r = requests.post(url, headers=headers, json=data)
                if r.status_code != 200:
                    raise DropboxApiError(f"Failed to move file/folder: {r.text}")
                logger.debug(
                    f"{self.service.name}: move {from_path} to {to_path} for user {user_id}"
                )
            except DropboxApiError as e:
                logger.error(f"{self.service.name}: {e}")

    class revoke_shared_link(Reaction):
        """Revoke a Dropbox shared link."""

        def __init__(self):
            config_schema = [{"name": "URL", "type": "input", "values": []}]
            super().__init__("Revoke a Dropbox shared link", config_schema)

        def execute(self, session: Session, area_reaction: AreaReaction, user_id: int):
            try:
                token: str = get_user_service_token(session, user_id, self.service.name)
                url_to_revoke: str = get_component(
                    area_reaction.config, "URL", "values"
                )

                url = "https://api.dropboxapi.com/2/sharing/revoke_shared_link"
                headers = {
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                }
                data = {"url": url_to_revoke}

                r = requests.post(url, headers=headers, json=data)
                if r.status_code != 200:
                    raise DropboxApiError(f"Failed to revoke shared link: {r.text}")
                logger.debug(
                    f"{self.service.name}: revoke shared link {url_to_revoke} for user {user_id}"
                )
            except DropboxApiError as e:
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
        return True

    def _is_token_valid(self, token: str) -> bool:
        try:
            self._get_user_info(token)
            return True
        except DropboxApiError:
            return False

    def oauth_link(self, state: str = None) -> str:
        base_url = "https://www.dropbox.com/oauth2/authorize"
        redirect = f"{settings.FRONT_URL}/callbacks/link/{self.name}"
        params = {
            "client_id": settings.DROPBOX_CLIENT_ID,
            "response_type": "code",
            "redirect_uri": redirect,
            "token_access_type": "offline",
        }
        return f"{base_url}?{urlencode(params)}"

    def _get_token(self, code: str) -> DropboxOAuthTokenRes:
        url = "https://api.dropboxapi.com/oauth2/token"
        redirect = f"{settings.FRONT_URL}/callbacks/link/{self.name}"
        data = {
            "code": code,
            "grant_type": "authorization_code",
            "client_id": settings.DROPBOX_CLIENT_ID,
            "client_secret": settings.DROPBOX_CLIENT_SECRET,
            "redirect_uri": redirect,
        }
        r = requests.post(url, data=data)
        if r.status_code != 200:
            logger.error(f"Dropbox token error: {r.text}")
            raise DropboxApiError(f"Failed to get Dropbox token: {r.text}")
        return DropboxOAuthTokenRes(**r.json())

    def _get_user_info(self, token: str) -> Dict[str, Any]:
        url = "https://api.dropboxapi.com/2/check/user"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        r = requests.post(url, headers=headers, json={})
        if r.status_code != 200:
            raise DropboxApiError(f"Failed to get Dropbox user info: {r.text}")
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
        except DropboxApiError as e:
            raise HTTPException(status_code=400, detail=e.message)

        return oauth_add_link(session, self.name, user, token_res.access_token)
