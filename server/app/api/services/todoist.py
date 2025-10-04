from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from core.config import settings
from typing import Annotated

from .todoist_api import todoist_api, TodoistApiError
from ..temp_db import user_data



def todoist_todo():
    if user_data["user_info"] is None:
        raise HTTPException(
            status_code=302,
            detail="Redirecting to Todoist OAuth",
            headers={"Location": todoist_api.get_oauth_link(settings.TODOIST_CLIENT_ID, "not used")}
        )
    else:
        return user_data["user_info"]



templates = Jinja2Templates(directory="templates")

router = APIRouter(tags=["todoist"], prefix="/todoist")



@router.get("/login_oauth_token")
def login_oauth_token(code: str):
    try:
        token_res = todoist_api.get_token(settings.TODOIST_CLIENT_ID, settings.TODOIST_CLIENT_SECRET, code)
    except TodoistApiError as e:
        raise HTTPException(status_code=400, detail=e.message)
    
    try:
        user_data["user_info"] = todoist_api.get_user_info(token_res.access_token)
        return RedirectResponse("/services/todoist/index")
    except TodoistApiError as e:
        return HTTPException(status_code=400, detail=e.message)


@router.get("/index", response_class=HTMLResponse)
def todoist_index(request: Request, user_info: Annotated[list, Depends(todoist_todo)]):
    return templates.TemplateResponse(request=request, name="services/todoist.html", context={"email": user_info["email"]})


@router.get("/mail")
def todoist_mail():
    return "test mail"
