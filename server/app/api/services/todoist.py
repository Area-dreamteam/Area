from dependencies.roles import CurrentUser, CurrentUserNoFail
from core.security import sign_jwt
from models.services.service import Service
from models.users.user_service import UserService
from models.users.user import User
from dependencies.db import SessionDep
from sqlmodel import select
from fastapi import APIRouter, Request, HTTPException, Depends, Response, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from core.config import settings
from typing import Annotated

from .todoist_api import todoist_api, TodoistApiError


templates = Jinja2Templates(directory="templates")

router = APIRouter(tags=["todoist"], prefix="/todoist")


@router.get("/index/{id}")
def todoist_index(id: int):
    raise HTTPException(
        status_code=302,
        detail="Redirecting to Todoist OAuth",
        headers={
            "Location": todoist_api.get_oauth_link(settings.TODOIST_CLIENT_ID, id)
        },
    )


def windowCloseAndCookie(token: str) -> Response:
    html = """
    <script>
      window.opener.postMessage({ type: "todoist_login_complete" }, "*");
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


@router.get("/login_oauth_token")
def login_oauth_token(session: SessionDep, code: str, user: CurrentUser):
    print("user id: ", user)
    try:
        token_res = todoist_api.get_token(
            settings.TODOIST_CLIENT_ID,
            settings.TODOIST_CLIENT_SECRET,
            code,
        )
    except TodoistApiError as e:
        raise HTTPException(status_code=400, detail=e.message)

    print(user)
    try:
        existing = session.exec(select(User).where(User.id == user.id)).first()

        service = session.exec(
            select(UserService)
            .join(Service, Service.id == UserService.service_id)
            .where(Service.name == "todoist", UserService.user_id == existing.id)
        ).first()
        if not service:
            """Already existing user, First time connecting to service"""

            service = session.exec(
                select(Service).where(Service.name == "todoist")
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
