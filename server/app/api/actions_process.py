import json
from typing import List
from reactions import reaction_list
from models.areas.area_action import AreaAction
from fastapi import APIRouter, HTTPException
from sqlmodel import select, join
from models import Action, Service
from schemas import ActionIdGet, ServiceGet
from dependencies.db import SessionDep
from dependencies.roles import CurrentUser

router = APIRouter()


@router.post("/actions_process", response_model=ActionIdGet)
def process_action(action_id: int, session: SessionDep):
    actions: List[AreaAction] = session.exec(
        select(AreaAction)
        .join(AreaAction.action_id)
        .where(AreaAction.action_id == action_id)
    ).all()
    for i in actions:
        reaction_list[i.name](i.config)

    return {}
