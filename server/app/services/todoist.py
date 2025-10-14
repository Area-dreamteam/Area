from typing import Dict, Any
from models.areas import AreaAction, AreaReaction
from services.services_classes import Service as ServiceClass, Action, Reaction
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
from fastapi import APIRouter, Request, HTTPException, Depends, Response, Query
from core.security import sign_jwt
from models.users.user_service import UserService
from sqlmodel import select
from fastapi.responses import HTMLResponse, RedirectResponse


class TodoistOAuthTokenRes(BaseModel):
    access_token: str
    token_type: str


class TodoistApiError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class Todoist(ServiceClass):
    class task_completed(Action):
        def __init__(self) -> None:
            config = [{"name": "task_id", "type": "input", "values": []}]
            super().__init__("checks when a task is completed", config)

        def check(self, session: Session, area_action: AreaAction, user_id: int):
            print(f"Checking task completion: {area_action.config}")

    class create_task(Reaction):
        def __init__(self) -> None:
            config = [
                {"name": "task_name", "type": "input", "values": []},
                {
                    "name": "priority",
                    "type": "select",
                    "values": ["low", "medium", "high", "urgent"],
                },
                {
                    "name": "reminders",
                    "type": "check_list",
                    "values": {"15m": True, "30m": True, "45m": False, "1h": False},
                },
            ]
            super().__init__("creates a new task", config)

        def execute(self, session: Session, area_action: AreaReaction, user_id: int):
            print(f"Creating task with params: {area_action.config}")

    def __init__(self) -> None:
        super().__init__("A modern interconnected todolist", "LifeStyle")

    def _is_token_valid(self, token):
        try:
            self.get_user_info(token)
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
        # tasks_id -= set(task.task_id for task in user_data["last_state"])

        # user_data["last_state"] = self._get_tasks(token)

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
        base_url = f"https://api.todoist.com/api/v1/tasks"
        params = {"content": content}

        if project_name is not None:
            project_id = self._get_projects_id(token, project_name)
            if project_id is not None:
                params["project_id"] = project_id
            else:
                return

        r = requests.post(
            f"{base_url}", data=params, headers={"Authorization": f"Bearer {token}"}
        )

        if r.status_code != 200:
            raise TodoistApiError("Failed to create task")

    def is_connected(self, session: Session) -> bool:
        return self._is_token_valid("")  # TODO: get token in db

    def oauth_link(self) -> str:
        base_url = "https://todoist.com/oauth/authorize"
        params = {
            "client_id": settings.TODOIST_CLIENT_ID,
            "scope": "data:read_write,data:delete,project:delete,backups:read",
            "state": generate_state(),
        }
        return f"{base_url}?{urlencode(params)}"

    def oauth_callback(self, session: Session, code: str, user: User) -> None:
        def windowCloseAndCookie(token: str) -> Response:
            html = f"""
            <script>
              window.opener.postMessage({{ type: "{self.name}_login_complete" }}, "*");
              window.close();
            </script>
            """
            response = HTMLResponse(content=html)
            response.set_cookie(
                key="access_token",
                value=f"Bearer {token}",
                httponly=True,
                secure=True,
                max_age=settings.ACCESS_TOKEN_EXPIRE_HOURS * 3600,
                samesite="none",
            )
            return response

        try:
            token_res = self._get_token(
                settings.TODOIST_CLIENT_ID,
                settings.TODOIST_CLIENT_SECRET,
                code,
            )
        except TodoistApiError as e:
            raise HTTPException(status_code=400, detail=e.message)

        try:
            existing = session.exec(select(User).where(User.id == user.id)).first()

            service = session.exec(
                select(UserService)
                .join(Service, Service.id == UserService.service_id)
                .where(Service.name == self.name, UserService.user_id == existing.id)
            ).first()
            if not service:
                """Already existing user, First time connecting to service"""

                service = session.exec(
                    select(Service).where(Service.name == self.name)
                ).first()
                print(service)
                new_user_service = UserService(
                    user_id=existing.id,
                    service_id=service.id,
                    access_token=token_res.access_token,
                )
                session.add(new_user_service)
                session.commit()

                token = sign_jwt(existing.id)
                return windowCloseAndCookie(token)
            """Already existing user, connecting to service"""
            service.access_token = token_res.access_token
            session.commit()
            token = sign_jwt(existing.id)

            return windowCloseAndCookie(token)
        except TodoistApiError as e:
            return HTTPException(status_code=400, detail=e.message)
