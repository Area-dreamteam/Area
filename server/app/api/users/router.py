from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from schemas import UserIdGet, UserUpdate, Role

from models import User
from dependencies.db import SessionDep
from dependencies.roles import CurrentUser, CurrentAdmin
from db import get_user_data

router = APIRouter(prefix="/users", tags=["users"])

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
