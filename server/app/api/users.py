from fastapi import APIRouter
from sqlmodel import select
from models import User
from schemas import UserIdGet
from dependencies.db import SessionDep

router = APIRouter()

@router.get("/users", response_model=list[UserIdGet])
def get_users(session: SessionDep):
    return

@router.get("/users/{id}", response_model=UserIdGet)
def get_users_by_id(session: SessionDep):
    return

@router.get("/users/me", response_model=UserIdGet)
def get_current_user(session: SessionDep):
    return
