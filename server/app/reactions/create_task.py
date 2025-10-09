from dependencies.db import SessionDep
from models import UserService, User
from sqlmodel import select
from core.logger import logger

from api.services.todoist_api import todoist_api, TodoistApiError

def get_component(config: list, name: str, key: str):
    for comp in config:
        if comp.get("name") == name:
            if key:
                return comp.get(key, None)
            return comp
    return None

def create_task(session: SessionDep, user_id: int, config: list):
    user_service: UserService = session.exec(
        select(UserService)
        .join(User, User.id == UserService.user_id)
        .where(user_id == UserService.user_id)
    ).first()
    if not user_service:
        return
    token = user_service.access_token

    content: str = get_component(config, "content", "values")
    project_name: str = get_component(config, "project_name", "values")
    try:
        todoist_api.create_task(token, content, project_name)
    except TodoistApiError:
        logger.error("Error: Todolist create_task reaction")
