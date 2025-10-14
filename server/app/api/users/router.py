from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from schemas import UserIdGet, UserServiceGet

from models import User, Service, UserService
from dependencies.db import SessionDep
from dependencies.roles import CurrentUser, CurrentAdmin

router = APIRouter(prefix="/users", tags=["users"])

def get_user_data(session: SessionDep, user: User) -> UserIdGet:
    user_services: list[UserService] = session.exec(select(UserService).where(UserService.user_id == user.id)).all()

    services_list: list[UserServiceGet] = []
    for user_service in user_services:
        service: Service = session.exec(select(Service).where(Service.id == user_service.service_id)).first()
        if not service:
            raise HTTPException(status_code=404, detail="Data not found")

        service_data: UserServiceGet = UserServiceGet(id=service.id, name=service.name, image_url=service.image_url, color=service.color, connected=False)
        services_list.append(service_data)
    user_data = UserIdGet(id=user.id, name=user.name, email=user.email, role=user.role, user_services=services_list)
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
def delete_user_by_id(id: int, session: SessionDep, _: CurrentUser):
    user_data: User = session.exec(select(User).where(User.id == id)).first()
    if not user_data:
        raise HTTPException(status_code=404, detail="Data not found")
    session.delete(user_data)
    session.commit()
    return {"message": "User deleted", "user_id": id}
