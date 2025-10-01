from fastapi import APIRouter, Depends
from sqlmodel import select
from schemas import UserIdGet
from dependencies.db import SessionDep
from dependencies.roles import CurrentUser, CurrentAdmin

router = APIRouter()

@router.get("/users", response_model=list[UserIdGet])
def get_users(session: SessionDep, user: CurrentAdmin):
    return

@router.get("/users/{id}", response_model=UserIdGet)
def get_users_by_id(session: SessionDep, user: CurrentAdmin):
    return

@router.get("/users/me", response_model=UserIdGet)
def get_current_user(session: SessionDep, user: CurrentUser):
    return
