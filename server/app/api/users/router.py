from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from schemas import UserIdGet, UserOauthLoginGet, UserUpdate, Role

from models import User, Service, UserService, UserOAuthLogin, OAuthLogin
from dependencies.db import SessionDep
from dependencies.roles import CurrentUser, CurrentAdmin

router = APIRouter(prefix="/users", tags=["users"])

def get_user_data(session: SessionDep, user: User) -> UserIdGet:
    oauths_login: list[OAuthLogin] = session.exec(
        select(OAuthLogin)
    ).all()

    if not oauths_login:
        raise HTTPException(status_code=404, detail="Oauth login not found")
    oauth_login_list: list[UserOauthLoginGet] = []
    for oauth_login in oauths_login:
        connected: bool = False
        user_oauth_login: UserOAuthLogin = session.exec(select(UserOAuthLogin).where(UserOAuthLogin.oauth_login_id == oauth_login.id, UserOAuthLogin.user_id == user.id)).first()
        if user_oauth_login:
            connected = True
        oauth_data: UserOauthLoginGet = UserOauthLoginGet(id=oauth_login.id, name=oauth_login.name, image_url=oauth_login.image_url, color=oauth_login.color, connected=connected)
        oauth_login_list.append(oauth_data)
    user_data = UserIdGet(id=user.id, name=user.name, email=user.email, role=user.role, oauth_login=oauth_login_list)
    return user_data

@router.get("/me", response_model=UserIdGet)
def get_current_user(session: SessionDep, user: CurrentUser) -> UserIdGet:
    user_data: UserIdGet = get_user_data(session, user)
    return user_data

@router.delete("/me")
def delete_current_user(session: SessionDep, user: CurrentUser):
    user_data: User = session.exec(select(User).where(User.id == user.id)).first()
    if not user_data:
        raise HTTPException(status_code=404, detail="Data not found")
    session.delete(user_data)
    session.commit()
    return {"message": "User deleted", "user_id": user.id}

@router.patch("/me")
def update_user_infos(updateUser: UserUpdate, session: SessionDep, user: CurrentUser):
    user_data: User = session.exec(
        select(User)
        .where(User.id == user.id)
    ).first()
    if not user_data:
        raise HTTPException(status_code=404, detail="Data not found")

    user_email_exist: User = session.exec(
        select(User)
        .where(User.email == updateUser.email, User.email != user.email)
    ).first()
    if user_email_exist:
        raise HTTPException(status_code=403, detail="Permission Denied: Email already exist")

    user_data.name = updateUser.name
    user_data.email = updateUser.email
    user_data.password = updateUser.password
    session.add(user_data)
    session.commit()
    return {"message": "User updated", "user_id": user.id}

@router.get("/", response_model=list[UserIdGet])
def get_users(session: SessionDep, _: CurrentAdmin) -> list[User]:
    users: list[User] = session.exec(select(User)).all()

    users_list: list[User] = []
    for user in users:
        user_data: UserIdGet = get_user_data(session, user)
        users_list.append(user_data)
    return users_list

@router.get("/{id}", response_model=UserIdGet)
def get_users_by_id(id: int, session: SessionDep, _: CurrentAdmin) -> UserIdGet:
    user: User = session.exec(select(User).where(User.id == id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="Data not found")

    user_data: UserIdGet = get_user_data(session, user)
    return user_data

@router.delete("/{id}")
def delete_user_by_id(id: int, session: SessionDep, user: CurrentAdmin):
    user_data: User = session.exec(select(User).where(User.id == id)).first()
    if not user_data:
        raise HTTPException(status_code=404, detail="Data not found")

    session.delete(user_data)
    session.commit()
    return {"message": "User deleted", "user_id": id}
