from fastapi import APIRouter
from sqlmodel import select
from models import Reaction
from schemas import ReactionIdGet
from dependencies.db import SessionDep
from dependencies.roles import CurrentUser

router = APIRouter()

@router.get("/reactions/{id}", response_model=ReactionIdGet)
def get_reaction_by_id(session: SessionDep, user: CurrentUser):
    return
