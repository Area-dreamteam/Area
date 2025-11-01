"""Notion service integration.

Provides page and database automation for Notion workspaces.
Supports OAuth authentication and page/database management.
"""

from typing import Dict, Any, List
from services.oauth_lib import oauth_add_link
from models.areas import AreaAction, AreaReaction
from services.services_classes import (
    Service as ServiceClass,
    Action,
    Reaction,
    get_component,
)
from api.users.db import get_user_service_token
from models.services.service import Service as ServiceModel
from core.config import settings
from core.categories import ServiceCategory
from models.users.user import User
from sqlmodel import Session, select
from core.utils import generate_state
from pydantic import BaseModel
from pydantic_core import ValidationError
from urllib.parse import urlencode
import requests
from fastapi import Request, HTTPException, Response
from models.users.user_service import UserService
from core.logger import logger
import base64


class NotionOAuthTokenRes(BaseModel):
    """Notion OAuth token response format."""

    access_token: str
    token_type: str
    bot_id: str
    workspace_id: str
    workspace_name: str | None = None
    workspace_icon: str | None = None
    owner: Dict[str, Any] | None = None
    duplicated_template_id: str | None = None


class NotionApiError(Exception):
    """Notion API-specific errors."""

    def __init__(self, message: str, status_code: int | None = None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class Notion(ServiceClass):
    """Notion automation service.

    Provides page and database monitoring capabilities, as well as
    page and database creation reactions.
    """

    class new_page(Action):
        """Triggered when a new page is created in the workspace."""

        service: "Notion"

        def __init__(self):
            config_schema = []
            super().__init__(
                "Triggered when a new page is created in your workspace",
                config_schema,
                "*/5 * * * *",
            )

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            try:
                pages = self.service._search_pages(session, user_id)

                if not pages:
                    return False

                page_ids = {page["id"] for page in pages}
                previous_page_ids = set(
                    area_action.last_state.get("page_ids", [])
                    if area_action.last_state
                    else []
                )

                if (
                    not area_action.last_state
                    or "page_ids" not in area_action.last_state
                ):
                    area_action.last_state = {"page_ids": list(page_ids)}
                    session.add(area_action)
                    session.commit()
                    return False

                new_page_ids = page_ids - previous_page_ids

                area_action.last_state = {"page_ids": list(page_ids)}
                session.add(area_action)
                session.commit()

                return len(new_page_ids) > 0

            except NotionApiError as e:
                logger.error(f"{self.service.name} new_page check error: {e.message}")
                return False

    class database_item_added(Action):
        """Triggered when a new item is added to a database."""

        service: "Notion"

        def __init__(self):
            config_schema = [
                {"name": "Database Name", "type": "input", "values": []},
            ]
            super().__init__(
                "Triggered when a new item is added to a specific database",
                config_schema,
                "*/5 * * * *",
            )

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            try:
                database_name = get_component(
                    area_action.config, "Database Name", "values"
                )

                if not database_name or not database_name.strip():
                    logger.error("Database Name is required")
                    return False

                database_id = self.service._get_database_id_by_name(
                    session, user_id, database_name
                )
                if not database_id:
                    logger.error(f"Database '{database_name}' not found")
                    return False

                items = self.service._query_database(session, user_id, database_id)

                if not items:
                    return False

                item_ids = {item["id"] for item in items}
                previous_item_ids = set(
                    area_action.last_state.get("item_ids", [])
                    if area_action.last_state
                    else []
                )

                if (
                    not area_action.last_state
                    or "item_ids" not in area_action.last_state
                ):
                    area_action.last_state = {"item_ids": list(item_ids)}
                    session.add(area_action)
                    session.commit()
                    return False

                new_item_ids = item_ids - previous_item_ids

                area_action.last_state = {"item_ids": list(item_ids)}
                session.add(area_action)
                session.commit()

                return len(new_item_ids) > 0

            except NotionApiError as e:
                logger.error(
                    f"{self.service.name} database_item_added check error: {e.message}"
                )
                return False

    class page_updated(Action):
        """Triggered when a specific page is updated."""

        service: "Notion"

        def __init__(self):
            config_schema = [
                {"name": "Page Title", "type": "input", "values": []},
            ]
            super().__init__(
                "Triggered when a specific page is updated",
                config_schema,
                "*/10 * * * *",
            )

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            try:
                page_title = get_component(area_action.config, "Page Title", "values")

                if not page_title or not page_title.strip():
                    logger.error("Page Title is required")
                    return False

                page_id = self.service._get_page_id_by_title(
                    session, user_id, page_title
                )
                if not page_id:
                    logger.error(f"Page '{page_title}' not found")
                    return False

                page = self.service._get_page(session, user_id, page_id)

                if not page:
                    return False

                last_edited_time = page.get("last_edited_time")
                previous_edited_time = (
                    area_action.last_state.get("last_edited_time")
                    if area_action.last_state
                    else None
                )

                if (
                    not area_action.last_state
                    or "last_edited_time" not in area_action.last_state
                ):
                    area_action.last_state = {"last_edited_time": last_edited_time}
                    session.add(area_action)
                    session.commit()
                    return False

                is_updated = last_edited_time != previous_edited_time

                area_action.last_state = {"last_edited_time": last_edited_time}
                session.add(area_action)
                session.commit()

                return is_updated

            except NotionApiError as e:
                logger.error(
                    f"{self.service.name} page_updated check error: {e.message}"
                )
                return False

    class create_page(Reaction):
        """Create a new page in Notion."""

        service: "Notion"

        def __init__(self):
            config_schema = [
                {"name": "Parent Page Title", "type": "input", "values": []},
                {"name": "New Page Title", "type": "input", "values": []},
                {"name": "Page Content", "type": "input", "values": []},
            ]
            super().__init__("Create a new page in Notion", config_schema)

        def execute(self, session: Session, area_reaction: AreaReaction, user_id: int):
            try:
                parent_title = get_component(
                    area_reaction.config, "Parent Page Title", "values"
                )
                title = get_component(area_reaction.config, "New Page Title", "values")
                content = get_component(area_reaction.config, "Page Content", "values")

                if not parent_title or not parent_title.strip():
                    logger.error("Parent Page Title is required")
                    return

                if not title or not title.strip():
                    logger.error("New Page Title is required")
                    return

                parent_id = self.service._get_page_id_by_title(
                    session, user_id, parent_title
                )
                if not parent_id:
                    logger.error(f"Parent page '{parent_title}' not found")
                    return

                self.service._create_page(session, user_id, parent_id, title, content)
                logger.info(f"Created Notion page: {title}")

            except NotionApiError as e:
                logger.error(f"{self.service.name} create_page error: {e.message}")

    class create_database_item(Reaction):
        """Create a new item in a Notion database."""

        service: "Notion"

        def __init__(self):
            config_schema = [
                {"name": "Database Name", "type": "input", "values": []},
                {"name": "Item Title", "type": "input", "values": []},
            ]
            super().__init__("Create a new item in a Notion database", config_schema)

        def execute(self, session: Session, area_reaction: AreaReaction, user_id: int):
            try:
                database_name = get_component(
                    area_reaction.config, "Database Name", "values"
                )
                title = get_component(area_reaction.config, "Item Title", "values")

                if not database_name or not database_name.strip():
                    logger.error("Database Name is required")
                    return

                if not title or not title.strip():
                    logger.error("Item Title is required")
                    return

                database_id = self.service._get_database_id_by_name(
                    session, user_id, database_name
                )
                if not database_id:
                    logger.error(f"Database '{database_name}' not found")
                    return

                self.service._create_database_item(session, user_id, database_id, title)
                logger.info(f"Created database item: {title}")

            except NotionApiError as e:
                logger.error(
                    f"{self.service.name} create_database_item error: {e.message}"
                )

    class append_block_to_page(Reaction):
        """Append a text block to an existing page."""

        service: "Notion"

        def __init__(self):
            config_schema = [
                {"name": "Page Title", "type": "input", "values": []},
                {"name": "Text Content", "type": "input", "values": []},
            ]
            super().__init__("Append a text block to an existing page", config_schema)

        def execute(self, session: Session, area_reaction: AreaReaction, user_id: int):
            try:
                page_title = get_component(area_reaction.config, "Page Title", "values")
                content = get_component(area_reaction.config, "Text Content", "values")

                if not page_title or not page_title.strip():
                    logger.error("Page Title is required")
                    return

                if not content or not content.strip():
                    logger.error("Text Content is required")
                    return

                page_id = self.service._get_page_id_by_title(
                    session, user_id, page_title
                )
                if not page_id:
                    logger.error(f"Page '{page_title}' not found")
                    return

                self.service._append_block_to_page(session, user_id, page_id, content)
                logger.info(f"Appended content to page: {page_title}")

            except NotionApiError as e:
                logger.error(
                    f"{self.service.name} append_block_to_page error: {e.message}"
                )

    def __init__(self) -> None:
        super().__init__(
            "All-in-one workspace for notes, tasks, wikis, and databases",
            ServiceCategory.PRODUCTIVITY,
            "#000000",
            "/images/Notion_logo.webp",
            True,
        )

    def _get_token(
        self, client_id: str, client_secret: str, code: str
    ) -> NotionOAuthTokenRes:
        """Exchange authorization code for access token."""
        url = "https://api.notion.com/v1/oauth/token"

        credentials = f"{client_id}:{client_secret}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()

        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/json",
        }

        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": f"{settings.FRONT_URL}/callbacks/link/Notion",
        }

        r = requests.post(url, headers=headers, json=data, timeout=10)

        if r.status_code != 200:
            raise NotionApiError(f"Failed to exchange code: {r.text}")

        try:
            return NotionOAuthTokenRes(**r.json())
        except ValidationError:
            raise NotionApiError("Invalid OAuth response")

    def _get_headers(self, session: Session, user_id: int) -> Dict[str, str]:
        """Get authorization headers for API requests."""
        token = get_user_service_token(session, user_id, self.name)

        if not token:
            raise NotionApiError("User not authenticated")

        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }

    def _make_request(
        self,
        session: Session,
        user_id: int,
        method: str,
        endpoint: str,
        data: dict | None = None,
    ) -> dict:
        """Make authenticated API request to Notion."""
        headers = self._get_headers(session, user_id)
        url = f"https://api.notion.com/v1{endpoint}"

        r = requests.request(method, url, headers=headers, json=data, timeout=10)

        if r.status_code not in [200, 201]:
            raise NotionApiError(
                f"API request failed: {r.text}", status_code=r.status_code
            )

        return r.json()

    def _search_pages(self, session: Session, user_id: int) -> List[Dict[str, Any]]:
        """Search for pages in the workspace."""
        data = {
            "filter": {"value": "page", "property": "object"},
            "sort": {"direction": "descending", "timestamp": "last_edited_time"},
            "page_size": 100,
        }

        result = self._make_request(session, user_id, "POST", "/search", data)
        return result.get("results", [])

    def _query_database(
        self, session: Session, user_id: int, database_id: str
    ) -> List[Dict[str, Any]]:
        """Query a database for all items."""
        endpoint = f"/databases/{database_id}/query"
        data = {
            "page_size": 100,
            "sorts": [{"timestamp": "created_time", "direction": "descending"}],
        }

        result = self._make_request(session, user_id, "POST", endpoint, data)
        return result.get("results", [])

    def _get_page(self, session: Session, user_id: int, page_id: str) -> Dict[str, Any]:
        """Get a specific page."""
        endpoint = f"/pages/{page_id}"
        return self._make_request(session, user_id, "GET", endpoint)

    def _get_page_id_by_title(
        self, session: Session, user_id: int, title: str
    ) -> str | None:
        """Find a page ID by its title."""
        pages = self._search_pages(session, user_id)
        for page in pages:
            properties = page.get("properties", {})
            title_prop = properties.get("title", {})
            title_array = title_prop.get("title", [])
            if title_array:
                page_title = title_array[0].get("plain_text", "")
                if page_title.lower() == title.lower():
                    return page["id"]
        return None

    def _get_database_id_by_name(
        self, session: Session, user_id: int, name: str
    ) -> str | None:
        """Find a database ID by its name."""
        data = {
            "filter": {"value": "database", "property": "object"},
            "page_size": 100,
        }
        result = self._make_request(session, user_id, "POST", "/search", data)
        databases = result.get("results", [])

        for db in databases:
            properties = db.get("properties", {})
            title_prop = properties.get("title", {})
            title_array = title_prop.get("title", [])
            if title_array:
                db_name = title_array[0].get("plain_text", "")
                if db_name.lower() == name.lower():
                    return db["id"]
        return None

    def _create_page(
        self,
        session: Session,
        user_id: int,
        parent_id: str,
        title: str,
        content: str = "",
    ):
        """Create a new page in Notion."""
        children = []

        if content:
            children.append(
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": content}}]
                    },
                }
            )

        data = {
            "parent": {"page_id": parent_id},
            "properties": {
                "title": {"title": [{"type": "text", "text": {"content": title}}]}
            },
            "children": children,
        }

        self._make_request(session, user_id, "POST", "/pages", data)

    def _create_database_item(
        self, session: Session, user_id: int, database_id: str, title: str
    ):
        """Create a new item in a database."""
        data = {
            "parent": {"database_id": database_id},
            "properties": {
                "Name": {"title": [{"type": "text", "text": {"content": title}}]}
            },
        }

        self._make_request(session, user_id, "POST", "/pages", data)

    def _append_block_to_page(
        self, session: Session, user_id: int, page_id: str, content: str
    ):
        """Append a text block to an existing page."""
        endpoint = f"/blocks/{page_id}/children"
        data = {
            "children": [
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": content}}]
                    },
                }
            ]
        }

        self._make_request(session, user_id, "PATCH", endpoint, data)

    def is_connected(self, session: Session, user_id: int) -> bool:
        """Check if user has connected their Notion account."""
        user_service = session.exec(
            select(UserService)
            .join(ServiceModel)
            .where(
                UserService.user_id == user_id,
                ServiceModel.name == self.name,
            )
        ).first()

        if not user_service or not user_service.access_token:
            return False

        try:
            headers = {
                "Authorization": f"Bearer {user_service.access_token}",
                "Content-Type": "application/json",
                "Notion-Version": "2022-06-28",
            }
            r = requests.post(
                "https://api.notion.com/v1/search",
                headers=headers,
                json={"page_size": 1},
                timeout=10,
            )
            return r.status_code == 200
        except Exception:
            return False

    def oauth_link(self, state: str = "") -> str:
        """Generate Notion OAuth authorization URL."""
        base_url = "https://api.notion.com/v1/oauth/authorize"
        params = {
            "client_id": settings.NOTION_CLIENT_ID,
            "redirect_uri": f"{settings.FRONT_URL}/callbacks/link/Notion",
            "response_type": "code",
            "owner": "user",
            "state": state if state else generate_state(),
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
        """Handle Notion OAuth callback."""
        if not user:
            raise HTTPException(status_code=400, detail="User must be authenticated")

        try:
            token_res = self._get_token(
                settings.NOTION_CLIENT_ID,
                settings.NOTION_CLIENT_SECRET,
                code,
            )
        except NotionApiError as e:
            raise HTTPException(status_code=400, detail=e.message)

        return oauth_add_link(
            session, self.name, user, token_res.access_token, request, is_mobile
        )
