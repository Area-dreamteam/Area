"""OAuth integration utilities.

Common OAuth flow helpers for service authentication and user account linking.
Provides unified OAuth callback handling for both login and service connection.
"""

from models.oauth.oauth_login import OAuthLogin
from models.users.user_oauth_login import UserOAuthLogin
from models.services.service import Service
from core.config import settings
from models.users.user import User
from sqlmodel import Session
from fastapi import Request, Response
from core.security import sign_jwt
from models.users.user_service import UserService
from sqlmodel import select
from fastapi.responses import HTMLResponse

def windowCloseAndCookie(
    id: int,
    name: str,
    request: Request | None = None,
    is_mobile: bool = False,
    is_login: bool = False,
    use_https_deeplink: bool = False,
) -> Response:
    token = sign_jwt(id)

    print(
        f"OAuth callback - Is mobile: {is_mobile}, Is login: {is_login}, Use HTTPS: {use_https_deeplink}"
    )

    if is_mobile:
        from fastapi.responses import RedirectResponse

        if use_https_deeplink:
            base_url = (
                str(request.base_url).rstrip("/")
                if request is not None
                else settings.FRONT_URL.rstrip("/")
            )
            if is_login:
                deeplink_url = f"{base_url}/oauth-callback?token={token}&service={name}"
                print(f"Redirecting to HTTPS login deeplink: {deeplink_url}")
            else:
                deeplink_url = f"{base_url}/oauth-callback?linked=true&service={name}"
                print(f"Redirecting to HTTPS link deeplink: {deeplink_url}")
        else:
            if is_login:
                deeplink_url = f"area://oauth-callback?token={token}&service={name}"
                print(f"Redirecting to mobile login deeplink: {deeplink_url}")
            else:
                deeplink_url = f"area://oauth-callback?linked=true&service={name}"
                print(f"Redirecting to mobile link deeplink: {deeplink_url}")
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
    session: Session,
    name: str,
    user: User,
    access_token: str,
    request: Request | None = None,
    is_mobile: bool = False,
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

        new_user_service = UserService(
            user_id=existing.id,
            service_id=service.id,
            access_token=access_token,
        )
        session.add(new_user_service)
        session.commit()
        session.refresh(new_user_service)

        return windowCloseAndCookie(existing.id, name, request, is_mobile)

    """Already existing user, connecting to service"""
    service.access_token = access_token
    session.commit()

    return windowCloseAndCookie(existing.id, name, request, is_mobile)


def oauth_add_login(
    session: Session,
    name: str,
    user: User | None,
    access_token: str,
    user_mail: str,
    request: Request | None = None,
    is_mobile: bool = False,
) -> Response:
    """Handle OAuth login flow - register new user or authenticate existing one.

    Creates new account if user doesn't exist, otherwise authenticates.
    """
    if user is None:
        existing = session.exec(select(User).where(User.email == user_mail)).first()
        if existing is None:
            existing = session.exec(select(User).join(UserOAuthLogin, UserOAuthLogin.user_id == User.id).where(UserOAuthLogin.email == user_mail)).first()
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
            email=user_mail,
            access_token=access_token,
        )
        session.add(new_user_service)
        session.commit()
        return windowCloseAndCookie(
            new_user.id, name, request, is_mobile, is_login=True
        )
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
        existing_oauth_login = session.exec(select(User).join(UserOAuthLogin, UserOAuthLogin.user_id == User.id).where(UserOAuthLogin.email == user_mail)).first()
        if existing_oauth_login:
            return windowCloseAndCookie(existing.id, name, request, is_mobile, is_login=True)
        existing_email = session.exec(select(User).where(User.email == user_mail)).first()
        if existing_email and existing.email != user_mail:
            return windowCloseAndCookie(existing.id, name, request, is_mobile, is_login=True)

        service = session.exec(
            select(OAuthLogin).where(OAuthLogin.name == name)
        ).first()
        new_user_service = UserOAuthLogin(
            user_id=existing.id,
            oauth_login_id=service.id,
            email=user_mail,
            access_token=access_token,
        )
        session.add(new_user_service)
        session.commit()
        return windowCloseAndCookie(
            existing.id, name, request, is_mobile, is_login=True
        )

    """Already existing user, connecting to service"""
    service.access_token = access_token
    session.commit()
    return windowCloseAndCookie(existing.id, name, request, is_mobile, is_login=True)
