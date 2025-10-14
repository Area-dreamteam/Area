from core.security import sign_jwt
import requests
from urllib.parse import urlencode
from models.oauth.oauth_login import OAuthLogin
from models.users.user_oauth_login import UserOAuthLogin
from models.users.user import User
from sqlmodel import select
from fastapi import HTTPException, Response
from fastapi.responses import HTMLResponse
from core.config import settings

from pydantic import BaseModel
from services.services_classes import oauth_service
from sqlmodel import Session
from pydantic_core import ValidationError


class GithubOAuthTokenRes(BaseModel):
    access_token: str
    token_type: str
    scope: str


class GithubApiError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class github_oauth(oauth_service):
    def __init__(self) -> None:
        super().__init__()

    def _get_token(self, client_id, client_secret, code):
        base_url = "https://github.com/login/oauth/access_token"
        params = {"client_id": client_id, "client_secret": client_secret, "code": code}

        r = requests.post(
            f"{base_url}?{urlencode(params)}", headers={"Accept": "application/json"}
        )

        if r.status_code != 200:
            raise GithubApiError("Invalid code or failed to retrieve token")

        try:
            return GithubOAuthTokenRes(**r.json())
        except ValidationError:
            raise GithubApiError("Invalid OAuth response")

    def _get_email(self, token):
        base_url = "https://api.github.com/user/emails"
        email_r = requests.get(
            f"{base_url}",
            headers={"Authorization": f"token {token}", "Accept": "application/json"},
        )

        if email_r.status_code != 200:
            raise GithubApiError("Failed to retrieve mail")

        return email_r.json()

    def oauth_link(self) -> str:
        base_url = "https://github.com/login/oauth/authorize"
        redirect = "http://localhost:3000/callbacks/login/github_oauth"
        params = {
            "client_id": settings.GITHUB_CLIENT_ID,
            "redirect_uri": redirect,
            "prompt": "select_account",
            "allow_signup": "true",
            "scope": "user",
            "login": "",
            "force_verify": "true",
        }
        return f"{base_url}?{urlencode(params)}"

    def oauth_callback(self, session: Session, code: str, user: User) -> None:
        def windowCloseAndCookie(token: str) -> Response:
            html = f"""
            <script>
              window.opener.postMessage({{type: "{self.name}_login_complete" }}, "http://localhost:3000/");
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
                settings.GITHUB_CLIENT_ID, settings.GITHUB_CLIENT_SECRET, code
            )
        except GithubApiError as e:
            raise HTTPException(status_code=400, detail=e.message)

        try:
            user_info = self._get_email(token_res.access_token)[0]
            if user is None:
                existing = session.exec(
                    select(User).where(User.email == user_info["email"])
                ).first()
            else:
                existing = session.exec(select(User).where(User.id == user.id)).first()
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
                    select(OAuthLogin).where(OAuthLogin.name == self.name)
                ).first()

                new_user_service = UserOAuthLogin(
                    user_id=new_user.id,
                    oauth_login_id=service.id,
                    access_token=token_res.access_token,
                )
                session.add(new_user_service)
                session.commit()
                token = sign_jwt(new_user.id)

                return windowCloseAndCookie(token)
            """User login with new oauth"""

            service = session.exec(
                select(UserOAuthLogin)
                .join(OAuthLogin, OAuthLogin.id == UserOAuthLogin.oauth_login_id)
                .where(
                    OAuthLogin.name == self.name,
                    UserOAuthLogin.user_id == existing.id,
                )
            ).first()
            if not service:
                """Already existing user, First time connecting to service"""

                service = session.exec(
                    select(OAuthLogin).where(OAuthLogin.name == self.name)
                ).first()
                new_user_service = UserOAuthLogin(
                    user_id=existing.id,
                    oauth_login_id=service.id,
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
