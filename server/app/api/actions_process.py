from typing import List, Any
from fastapi import APIRouter, HTTPException
from sqlmodel import select, join

from reactions.reaction_list import reaction_list
from models import AreaAction, Action, Area, Service, Reaction, AreaReaction
from dependencies.db import SessionDep
from core.logger import logger

router = APIRouter()

@router.post("/actions_process")
def process_action(action_id: int, session: SessionDep):
    action_data: tuple[Action, Service] = session.exec(
        select(Action, Service)
        .join(Service, Service.id == Action.service_id)
        .where(Action.id == action_id)).first()
    if not action_data:
        raise HTTPException(status_code=404, detail="Data not found")

    logger.debug(f"action_id: {action_id}")
    actions_config: List[AreaAction] = session.exec(
        select(AreaAction)
        .join(Action, Action.id == AreaAction.action_id)
        .join(Area, Area.id == AreaAction.area_id)
        .where(AreaAction.action_id == action_id, Area.enable == True, Area.is_public == True)
    ).all()

    for action_config in actions_config:
        # Recupere la new_data de l'action avec la config associée dans le service
        # if old_data == new_data:
        #   continue

        area: Area = session.exec(
            select(Area)
            .where(Area.id == action_config.area_id)
        ).first()
        if not area:
            continue

        logger.debug(f"area_id: {area.id}")

        reactions_data: list[tuple[Any, str, str]] = session.exec(
            select(AreaReaction.config, Reaction.name, Service.name)
            .join(Reaction, Reaction.id == AreaReaction.reaction_id)
            .join(Service, Service.id == Reaction.service_id)
            .where(AreaReaction.area_id == area.id)
        ).all()
        if not reactions_data:
            continue

        for reaction_config, reaction_name, service_name in reactions_data:
            reaction_list[reaction_name](reaction_config, service_name)

    return {}
