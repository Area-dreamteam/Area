from typing import List, Any
from fastapi import APIRouter, HTTPException
from sqlmodel import select, join

from reactions.reaction_list import reaction_list
from models import AreaAction, Action, Area, Service, Reaction, AreaReaction, User
from dependencies.db import SessionDep
from core.logger import logger

router = APIRouter()

def reaction_process(session: SessionDep, area_id: int):
    area: Area = session.exec(
        select(Area).where(Area.id == area_id)
    ).first()
    if not area:
        return

    logger.debug(f"area_id: {area.id}")
    reactions_data: list[tuple[Any, str, str]] = session.exec(
        select(AreaReaction.config, Reaction.name, Service.name)
        .join(Reaction, Reaction.id == AreaReaction.reaction_id)
        .join(Service, Service.id == Reaction.service_id)
        .where(AreaReaction.area_id == area.id)
    ).all()
    if not reactions_data:
        return

    for reaction_config, reaction_name, service_name in reactions_data:
        reaction_list[reaction_name](reaction_config, service_name)

@router.post("/actions_process")
def process_action(action_id: int, session: SessionDep):
    action_data: tuple[Action, Service] = session.exec(
        select(Action, Service)
        .join(Service, Service.id == Action.service_id)
        .where(Action.id == action_id)
    ).first()
    if not action_data:
        raise HTTPException(status_code=404, detail="Data not found")

    logger.debug(f"action_id: {action_id}")
    user_actions_config_data: List[tuple[int, AreaAction]] = session.exec(
        select(User.id, AreaAction)
        .join(Action, Action.id == AreaAction.action_id)
        .join(Area, Area.id == AreaAction.area_id)
        .join(User, User.id == Area.user_id)
        .where(
            AreaAction.action_id == action_id,
            Area.enable == True,
            Area.is_public == False,
        )
    ).all()
    
    if not user_actions_config_data:
        # Désactiver le cron de cette action
        raise HTTPException(status_code=404, detail="No data found for this action")

    # ----------------
    print(user_actions_config_data)
    user_actions_config: dict[int, list[AreaAction]] = {id: [] for id in set(next(zip(*user_actions_config_data)))}
    for id, data in user_actions_config_data:
        user_actions_config[id].append(data)

    # ----------------
    logger.debug(user_actions_config)

    for user_actions in user_actions_config.values():
        # Check une seul action d'un user

        # Recupere la new_data de l'action avec la config associée dans le service et update last_state
        # if old_data == new_data:
        #   continue

        for user_action in user_actions:
            reaction_process(session, user_action.area_id)

    return {}
