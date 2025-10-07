from core.security import sign_jwt
from models.services.service import Service
from models.users.user_service import UserService
from models.users.user import User
from dependencies.db import SessionDep
from sqlmodel import select
from fastapi import APIRouter, Request, HTTPException, Depends, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from core.config import settings
from typing import Annotated

from .github_api import github_api, GithubApiError


templates = Jinja2Templates(directory="templates")

router = APIRouter(tags=["github"], prefix="/github")


@router.get("/index")
def github_index():
    raise HTTPException(
        status_code=302,
        detail="Redirecting to GitHub OAuth",
        headers={
            "Location": github_api.get_oauth_link(
                settings.GITHUB_CLIENT_ID,
                "http://127.0.0.1:8080/services/github/login_oauth_token",
            )
        },
    )


def windowCloseAndCookie(token: str) -> Response:
    html = """
    <script>
      window.opener.postMessage({ type: "github_login_complete" }, "*");
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
def login_oauth_token(session: SessionDep, code: str):
    try:
        token_res = github_api.get_token(
            settings.GITHUB_CLIENT_ID, settings.GITHUB_CLIENT_SECRET, code
        )
    except GithubApiError as e:
        raise HTTPException(status_code=400, detail=e.message)

    try:
        user_info = github_api.get_email(token_res.access_token)[0]
        print(user_info)
        existing = session.exec(
            select(User).where(User.email == user_info["email"])
        ).first()
        if not existing:
            """User Register with oauth"""
            new_user = User(
                name=user_info["email"].split("@")[0],
                email=user_info["email"],
            )

            session.add(new_user)
            session.commit()
            session.refresh(new_user)

            service = session.exec(
                select(Service).where(Service.name == "github")
            ).first()
            new_user_service = UserService(
                user_id=new_user.id,
                service_id=service.id,
                access_token=token_res.access_token,
            )
            session.add(new_user_service)
            session.commit()
            token = sign_jwt(new_user.id)

            return windowCloseAndCookie(token)
        """User login with new oauth"""

        service = session.exec(
            select(UserService)
            .join(Service, Service.id == UserService.service_id)
            .where(Service.name == "github", UserService.user_id == existing.id)
        ).first()
        if not service:
            """Already existing user, First time connecting to service"""

            service = session.exec(
                select(Service).where(Service.name == "github")
            ).first()
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
    except GithubApiError as e:
        return HTTPException(status_code=400, detail=e.message)
