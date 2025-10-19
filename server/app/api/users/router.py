from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from schemas import UserIdGet, UserDeletionResponse

from models import User
from dependencies.db import SessionDep
from dependencies.roles import CurrentUser, CurrentAdmin
from api.users.db import get_user_data

router = APIRouter(prefix="/users", tags=["users"])

@router.get(
    "/me",
    response_model=UserIdGet,
    summary="Get current user profile",
    description="Get complete profile with connected services"
)
def get_current_user(session: SessionDep, user: CurrentUser) -> UserIdGet:
    user_data: UserIdGet = get_user_data(session, user)
    return user_data

@router.delete(
    "/me",
    response_model=UserDeletionResponse,
    summary="Delete current user",
    description="Permanently delete current user account"
)
def delete_current_user(session: SessionDep, user: CurrentUser) -> UserDeletionResponse:
    user_data: User = session.exec(select(User).where(User.id == user.id)).first()
    if not user_data:
        raise HTTPException(status_code=404, detail="Data not found")
    session.delete(user_data)
    session.commit()
    return UserDeletionResponse(message="User deleted", user_id=user.id)

@router.get(
    "/",
    response_model=list[UserIdGet],
    summary="List all users",
    description="Admin only: get all users with their connected services"
)
def get_users(session: SessionDep, _: CurrentAdmin) -> list[User]:
    users: list[User] = session.exec(select(User)).all()

    users_list: list[User] = []
    for user in users:
        user_data: UserIdGet = get_user_data(session, user)
        users_list.append(user_data)
    return users_list

@router.get(
    "/{id}",
    response_model=UserIdGet,
    summary="Get user by ID",
    description="Admin only: get specific user details",
    responses={404: {"description": "User not found"}}
)
def get_users_by_id(id: int, session: SessionDep, _: CurrentAdmin) -> UserIdGet:
    user: User = session.exec(select(User).where(User.id == id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="Data not found")

    user_data: UserIdGet = get_user_data(session, user)
    return user_data

@router.delete(
    "/{id}",
    response_model=UserDeletionResponse,
    summary="Delete user by ID",
    description="Delete specific user account",
    responses={404: {"description": "User not found"}}
)
def delete_user_by_id(id: int, session: SessionDep, _: CurrentUser) -> UserDeletionResponse:
    user_data: User = session.exec(select(User).where(User.id == id)).first()
    if not user_data:
        raise HTTPException(status_code=404, detail="Data not found")

    session.delete(user_data)
    session.commit()
    return UserDeletionResponse(message="User deleted", user_id=id)
