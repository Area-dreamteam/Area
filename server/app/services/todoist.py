"""Todoist service integration.

Provides task completion triggers and task creation reactions.
Supports OAuth authentication and project-based task management.
"""

from services.oauth_lib import oauth_add_link
from models.areas import AreaAction, AreaReaction
from services.services_classes import (
    Service as ServiceClass,
    Action,
    Reaction,
    get_component,
)
from models.services.service import Service
from schemas.services.todoist import Task, Project
from core.config import settings
from models.users.user import User
from sqlmodel import Session
from core.utils import generate_state
from pydantic import BaseModel
from pydantic_core import ValidationError
from urllib.parse import urlencode
import requests
import json
from fastapi import Request, HTTPException, Response
from models.users.user_service import UserService
from sqlmodel import select
from core.logger import logger
from api.users.db import get_user_service_token


class TodoistOAuthTokenRes(BaseModel):
    """Todoist OAuth token response format."""

    access_token: str
    token_type: str


class TodoistApiError(Exception):
    """Todoist API-specific errors."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class Todoist(ServiceClass):
    """Todoist automation service.

    Provides task completion monitoring and task creation capabilities.
    Supports project-based organization and priority settings.
    """

    class new_completed_task(Action):
        """Triggered when a task is marked complete."""

        service: "Todoist"

        def __init__(self):
            config_schema = []
            super().__init__("Triggered when a task is completed", config_schema)

        def check(self, session, area_action, user_id):
            try:
                token = get_user_service_token(session, user_id, self.service.name)
                headers = {"Authorization": f"Bearer {token}"}
                url = "https://api.todoist.com/sync/v9/completed/get_all"
                r = requests.get(url, headers=headers)
                if r.status_code != 200:
                    raise TodoistApiError("Failed to fetch completed tasks")

                data = r.json()
                completed_task = data.get("items", [])[0] if data.get("items") else None
            except TodoistApiError as e:
                logger.error(f"{self.service.name}: {e}")
            return self.service._compare_data(session, area_action, completed_task, "task_id")

    class new_task_added(Action):
        """Triggered when a new task is added to Todoist."""

        service: "Todoist"

        def __init__(self):
            config_schema = []
            super().__init__("Triggered when a new task is added", config_schema)

        def check(self, session, area_action, user_id):
            try:
                token = get_user_service_token(session, user_id, self.service.name)
                headers = {"Authorization": f"Bearer {token}"}
                url = "https://api.todoist.com/rest/v2/tasks"
                r = requests.get(url, headers=headers)
                logger.error(r.json())
                if r.status_code != 200:
                    raise TodoistApiError("Failed to fetch tasks")

                task = r.json()[-1] if len(r.json()) > 0 else None
            except TodoistApiError as e:
                logger.error(f"{self.service.name}: {e}")
            return self.service._compare_data(session, area_action, task, "id")

    class create_task(Reaction):
        service: "Todoist"

        def __init__(self) -> None:
            config_schema = [
                {"name": "Content", "type": "input", "values": []},
                {"name": "Project name", "type": "input", "values": []},
            ]
            super().__init__("creates a new task", config_schema)

        def execute(self, session: Session, area_action: AreaReaction, user_id: int):
            try:
                token: str = get_user_service_token(session, user_id, self.service.name)
                content: str = get_component(area_action.config, "Content", "values")
                project_name: str = get_component(
                    area_action.config, "Project name", "values"
                )
                self.service._create_task(token, content, project_name)
                logger.debug(f"Todoist: Creating task for user {user_id}")
            except TodoistApiError as e:
                logger.error(f"{self.service.name}: {e}")

    def __init__(self) -> None:
        super().__init__(
            "A modern interconnected todolist",
            "LifeStyle",
            "#CE3608",
            "/images/Todoist_logo.webp",
            True,
        )

    def _compare_data(
        self, session: Session, area_action: AreaAction, data: Dict[str, Any], key: str
    ) -> bool:
        """Check if the data is new compared to the last stored one."""
        if not area_action.last_state:
            area_action.last_state = data
            session.add(area_action)
            session.commit()
            return False

        if data and data[key] != area_action.last_state.get(key):
            area_action.last_state = data
            session.add(area_action)
            session.commit()
            return True
        return False

    def _is_token_valid(self, token):
        try:
            self._get_user_info(token)
            return True
        except TodoistApiError:
            return False

    def _get_token(self, client_id, client_secret, code):
        base_url = "https://todoist.com/oauth/access_token"
        params = {"client_id": client_id, "client_secret": client_secret, "code": code}

        r = requests.post(
            f"{base_url}?{urlencode(params)}", headers={"Accept": "application/json"}
        )

        if r.status_code != 200:
            raise TodoistApiError("Invalid code or failed to retrieve token")

        try:
            return TodoistOAuthTokenRes(**r.json())
        except ValidationError:
            raise TodoistApiError("Invalid OAuth response")

    def _get_projects_id(self, token, project_name):
        return next(
            (
                project.project_id
                for project in self._get_projects(token)
                if project.name == project_name
            ),
            None,
        )

    def _get_user_info(self, token):
        base_url = "https://api.todoist.com/api/v1/sync"
        params = {"sync_token": "'*'", "resource_types": json.dumps(["user"])}
        email_r = requests.post(
            f"{base_url}?{urlencode(params)}",
            headers={"Authorization": f"Bearer {token}"},
        )

        if email_r.status_code != 200:
            raise TodoistApiError("Failed to retrieve email")

        return email_r.json()["user"]

    def _get_tasks(self, token, project_name=None) -> list[Task]:
        base_url = "https://api.todoist.com/api/v1/tasks"
        params = {}

        if project_name is not None:
            project_id = self._get_projects_id(token, project_name)
            if project_id is not None:
                params["project_id"] = project_id
            else:
                return []

        r = requests.get(
            f"{base_url}?{urlencode(params)}",
            headers={"Authorization": f"Bearer {token}"},
        )

        if r.status_code != 200:
            raise TodoistApiError("Failed to retrieve tasks")

        task_list = []

        for task in r.json()["results"]:
            task_list.append(Task(**task))

        return task_list

    def _get_new_tasks_id(self, token, project_name) -> set[str]:
        tasks = self._get_tasks(token, project_name)

        tasks_id = set(task.task_id for task in tasks)

        return tasks_id

    def _get_new_tasks(self, token, project_name) -> list[Task]:
        tasks: list[Task] = self._get_tasks(token, project_name)
        new_tasks_id: set[str] = self._get_new_tasks_id(token, project_name)

        return [task for task in tasks if task.task_id in new_tasks_id]

    def _get_projects(self, token) -> list[Project]:
        base_url = "https://api.todoist.com/api/v1/projects"
        params = {}
        r = requests.get(
            f"{base_url}?{urlencode(params)}",
            headers={"Authorization": f"Bearer {token}"},
        )

        if r.status_code != 200:
            raise TodoistApiError("Failed to retrieve projects")

        projects_list = []

        for project in r.json()["results"]:
            projects_list.append(Project(**project))

        return projects_list

    def _create_task(self, token, content, project_name=None):
        base_url = "https://api.todoist.com/api/v1/tasks"
        data = {"content": content}

        if project_name is not None:
            project_id = self._get_projects_id(token, project_name)
            if project_id is not None:
                data["project_id"] = project_id
            else:
                return

        r = requests.post(
            f"{base_url}", data=data, headers={"Authorization": f"Bearer {token}"}
        )

        if r.status_code != 200:
            raise TodoistApiError("Failed to create task")

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

    def oauth_link(self, state: str = None) -> str:
        base_url = "https://todoist.com/oauth/authorize"
        params = {
            "client_id": settings.TODOIST_CLIENT_ID,
            "scope": "data:read_write,data:delete,project:delete,backups:read",
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
            token_res = self._get_token(
                settings.TODOIST_CLIENT_ID,
                settings.TODOIST_CLIENT_SECRET,
                code,
            )
        except TodoistApiError as e:
            raise HTTPException(status_code=400, detail=e.message)

        return oauth_add_link(
            session, self.name, user, token_res.access_token, request, is_mobile
        )
