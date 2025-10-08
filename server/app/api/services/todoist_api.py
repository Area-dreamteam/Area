from pydantic import BaseModel
from pydantic_core import ValidationError
from urllib.parse import urlencode
import requests
import json

from schemas.services.todoist import Task, Project
from core.utils import generate_state


class TodoistOAuthTokenRes(BaseModel):
    access_token: str
    token_type: str


class TodoistApiError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class TodoistApi:
    def __init__(self):
        pass

    def is_token_valid(self, token):
        try:
            self.get_user_info(token)
            return True
        except TodoistApiError:
            return False

    def get_oauth_link(self, client_id, user_id):
        base_url = "https://todoist.com/oauth/authorize"
        params = {
            "client_id": client_id,
            "scope": "data:read_write,data:delete,project:delete,backups:read",
            "state": generate_state(),
        }
        return f"{base_url}?{urlencode(params)}"

    def get_token(self, client_id, client_secret, code):
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

    def get_projects_id(self, token, project_name):
        return next(
            (
                project.project_id
                for project in todoist_api.get_projects(token)
                if project.name == project_name
            ),
            None,
        )

    def get_user_info(self, token):
        base_url = "https://api.todoist.com/api/v1/sync"
        params = {"sync_token": "'*'", "resource_types": json.dumps(["user"])}
        email_r = requests.post(
            f"{base_url}?{urlencode(params)}",
            headers={"Authorization": f"Bearer {token}"},
        )

        if email_r.status_code != 200:
            raise TodoistApiError("Failed to retrieve email")

        return email_r.json()["user"]

    def get_tasks(self, token, project_name=None) -> list[Task]:
        base_url = "https://api.todoist.com/api/v1/tasks"
        params = {}

        if project_name is not None:
            project_id = self.get_projects_id(token, project_name)
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

    def get_new_tasks_id(self, token, project_name) -> set[str]:
        tasks = self.get_tasks(token, project_name)

        tasks_id = set(task.task_id for task in tasks)
        tasks_id -= set(task.task_id for task in user_data["last_state"])

        user_data["last_state"] = self.get_tasks(token)

        return tasks_id

    def get_new_tasks(self, token, project_name) -> list[Task]:
        tasks: list[Task] = self.get_tasks(token, project_name)
        new_tasks_id: set[str] = self.get_new_tasks_id(token, project_name)

        return [task for task in tasks if task.task_id in new_tasks_id]

    def get_projects(self, token) -> list[Project]:
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

    def create_task(self, token, content, project_name=None):
        base_url = f"https://api.todoist.com/api/v1/tasks"
        params = {"content": content}

        if project_name is not None:
            project_id = self.get_projects_id(token, project_name)
            if project_id is not None:
                params["project_id"] = project_id
            else:
                return

        r = requests.post(
            f"{base_url}", data=params, headers={"Authorization": f"Bearer {token}"}
        )

        if r.status_code != 200:
            raise TodoistApiError("Failed to create task")


todoist_api = TodoistApi()
