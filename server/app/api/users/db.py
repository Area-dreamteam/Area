from sqlmodel import select
from models import UserService, User
from sqlmodel import Session
from fastapi import HTTPException
from schemas import UserIdGet, UserOauthLoginGet

from models import UserOAuthLogin, OAuthLogin, Service
from dependencies.db import SessionDep


def get_user_service_token(session: Session, user_id: int, service_name: str) -> str | None:
    user_service: UserService = session.exec(
        select(UserService)
        .join(Service, Service.id == UserService.service_id)
        .join(User, User.id == UserService.user_id)
        .where(user_id == UserService.user_id, Service.name == service_name)
    ).first()
    if not user_service:
        return None
    token = user_service.access_token
    return token


def get_user_data(session: SessionDep, user: User) -> UserIdGet:
    oauths_login: list[OAuthLogin] = session.exec(select(OAuthLogin)).all()

    if not oauths_login:
        raise HTTPException(status_code=404, detail="Oauth login not found")
    oauth_login_list: list[UserOauthLoginGet] = []
    for oauth_login in oauths_login:
        connected: bool = False
        user_oauth_login: UserOAuthLogin = session.exec(
            select(UserOAuthLogin).where(
                UserOAuthLogin.oauth_login_id == oauth_login.id,
                UserOAuthLogin.user_id == user.id,
            )
        ).first()
        if user_oauth_login:
            connected = True
        oauth_data: UserOauthLoginGet = UserOauthLoginGet(
            id=oauth_login.id,
            name=oauth_login.name,
            image_url=oauth_login.image_url,
            color=oauth_login.color,
            connected=connected,
        )
        oauth_login_list.append(oauth_data)
    user_data = UserIdGet(
        id=user.id,
        name=user.name,
        email=user.email,
        role=user.role,
        oauth_login=oauth_login_list,
    )
    return user_data
