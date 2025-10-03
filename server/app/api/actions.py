from fastapi import APIRouter
from sqlmodel import select
from models import Action
from schemas import ActionIdGet
from dependencies.db import SessionDep

router = APIRouter()

@router.get("/actions/{id}", response_model=ActionIdGet)
def get_action_by_id(session: SessionDep):
    return
