from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from core.config import settings
from typing import Annotated

from .github_api import github_api, GithubApiError
from ..temp_db import user_data



def github_email():
    if user_data["email"] is None:
        raise HTTPException(
            status_code=302,
            detail="Redirecting to GitHub OAuth",
            headers={"Location": github_api.get_oauth_link(settings.GITHUB_CLIENT_ID, "http://127.0.0.1:8080/services/github/login_oauth_token")}
        )
    else:
        return user_data["email"]



templates = Jinja2Templates(directory="templates")

router = APIRouter(tags=["github"], prefix="/github")



@router.get("/login_oauth_token")
def login_oauth_token(code: str):
    try:
        token_res = github_api.get_token(settings.GITHUB_CLIENT_ID, settings.GITHUB_CLIENT_SECRET, code)
    except GithubApiError as e:
        raise HTTPException(status_code=400, detail=e.message)
    
    try:
        user_data["email"] = github_api.get_email(token_res.access_token)
        return RedirectResponse("/services/github/index")
    except GithubApiError as e:
        return HTTPException(status_code=400, detail=e.message)


@router.get("/index", response_class=HTMLResponse)
def github_index(request: Request, email: Annotated[list, Depends(github_email)]):
    return templates.TemplateResponse(request=request, name="services/github.html", context={"email": email})


@router.get("/mail")
def github_mail():
    return "test mail"
