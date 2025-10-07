from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from core.config import settings
from typing import Annotated

from .todoist_api import todoist_api, TodoistApiError
from ..temp_db import user_data



def todoist_todo():
    if user_data["token"] is None:
        raise HTTPException(
            status_code=302,
            detail="Redirecting to Todoist OAuth",
            headers={"Location": todoist_api.get_oauth_link(settings.TODOIST_CLIENT_ID)}
        )
    else:
        return user_data["token"]



templates = Jinja2Templates(directory="templates")

router = APIRouter(tags=["todoist"], prefix="/todoist")



@router.get("/login_oauth_token")
def login_oauth_token(code: str):
    try:
        token_res = todoist_api.get_token(settings.TODOIST_CLIENT_ID, settings.TODOIST_CLIENT_SECRET, code)
    except TodoistApiError as e:
        raise HTTPException(status_code=400, detail=e.message)
    
    try:
        user_data["token"] = token_res.access_token
        user_data["user_info"] = todoist_api.get_user_info(user_data["token"])
        user_data["last_state"] = todoist_api.get_tasks(user_data["token"])
        return RedirectResponse("/services/todoist/index")
    except TodoistApiError as e:
        return HTTPException(status_code=400, detail=e.message)


@router.get("/index", response_class=HTMLResponse)
def todoist_index(request: Request, token: Annotated[list, Depends(todoist_todo)]):
    new_tasks = todoist_api.get_new_tasks(token, "Inbox")
    for new_task in new_tasks:
        todoist_api.create_task(token, new_task.content, project_name="Perso 🏡")
    
    return templates.TemplateResponse(request=request, name="services/todoist.html", context={"email": user_data["user_info"]["email"], "tasks": []})


@router.get("/mail")
def todoist_mail():
    return "test mail"
