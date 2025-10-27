"""OAuth integration utilities.

Common OAuth flow helpers for service authentication and user account linking.
Provides unified OAuth callback handling for both login and service connection.
"""

from typing import Dict, Any
from models.oauth.oauth_login import OAuthLogin
from models.users.user_oauth_login import UserOAuthLogin
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


def windowCloseAndCookie(
    id: int, name: str, request: Request = None, is_mobile: bool = False
) -> Response:
    token = sign_jwt(id)

    print(f"OAuth callback - Is mobile flag set: {is_mobile}")

    if is_mobile:
        # Redirect to mobile deeplink
        from fastapi.responses import RedirectResponse

        deeplink_url = f"area://oauth-callback?token={token}&service={name}"
        print(f"Redirecting to mobile deeplink: {deeplink_url}")
        return RedirectResponse(url=deeplink_url, status_code=302)

    html = f"""
    <script>
      window.opener.postMessage({{ type: "{name}_login_complete" }}, "*");
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


class OAuthApiError(Exception):
    """OAuth-related API errors."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def oauth_add_link(
    session: Session, name: str, user: User, access_token: str, request: Request = None
) -> Response:
    """Link a service to existing authenticated user account.

    Creates or updates service connection with OAuth token.
    """
    existing = session.exec(select(User).where(User.id == user.id)).first()
    service = session.exec(
        select(UserService)
        .join(Service, Service.id == UserService.service_id)
        .where(Service.name == name, UserService.user_id == existing.id)
    ).first()
    if not service:
        """Already existing user, First time connecting to service"""

        service = session.exec(select(Service).where(Service.name == name)).first()
        print(service)
        new_user_service = UserService(
            user_id=existing.id,
            service_id=service.id,
            access_token=access_token,
        )
        session.add(new_user_service)
        session.commit()

        return windowCloseAndCookie(existing.id, name, request)
    """Already existing user, connecting to service"""
    service.access_token = access_token
    session.commit()

    return windowCloseAndCookie(existing.id, name, request)


def oauth_add_login(
    session: Session,
    name: str,
    user: User | None,
    access_token: str,
    user_mail: str,
    request: Request = None,
    is_mobile: bool = False,
) -> Response:
    """Handle OAuth login flow - register new user or authenticate existing one.

    Creates new account if user doesn't exist, otherwise authenticates.
    """
    if user is None:
        existing = session.exec(select(User).where(User.email == user_mail)).first()
    else:
        existing = session.exec(select(User).where(User.id == user.id)).first()
    if not existing:
        """User Register with oauth"""
        new_user = User(
            name=user_mail.split("@")[0],
            email=user_mail,
        )

        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        service = session.exec(
            select(OAuthLogin).where(OAuthLogin.name == name)
        ).first()

        new_user_service = UserOAuthLogin(
            user_id=new_user.id,
            oauth_login_id=service.id,
            access_token=access_token,
        )
        session.add(new_user_service)
        session.commit()
        return windowCloseAndCookie(new_user.id, name, request, is_mobile)
    """User login with new oauth"""

    service = session.exec(
        select(UserOAuthLogin)
        .join(OAuthLogin, OAuthLogin.id == UserOAuthLogin.oauth_login_id)
        .where(
            OAuthLogin.name == name,
            UserOAuthLogin.user_id == existing.id,
        )
    ).first()
    if not service:
        """Already existing user, First time connecting to service"""
        service = session.exec(
            select(OAuthLogin).where(OAuthLogin.name == name)
        ).first()
        new_user_service = UserOAuthLogin(
            user_id=existing.id,
            oauth_login_id=service.id,
            access_token=access_token,
        )
        session.add(new_user_service)
        session.commit()
        return windowCloseAndCookie(existing.id, name, request, is_mobile)

    """Already existing user, connecting to service"""
    service.access_token = access_token
    session.commit()
    return windowCloseAndCookie(existing.id, name, request, is_mobile)
