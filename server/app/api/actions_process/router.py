from typing import List, Any
from fastapi import APIRouter, HTTPException
from services.services import services_dico
from sqlmodel import select, join

from models import (
    AreaAction,
    Action,
    Area,
    Service,
    Reaction,
    AreaReaction,
    User,
    UserService,
)
from dependencies.db import SessionDep
from core.logger import logger
from cron.cron import deleteJob

router = APIRouter(prefix="/actions_process", tags=["actions_process"])


def reaction_process(session: SessionDep, area_id: int):
    area: Area = session.exec(select(Area).where(Area.id == area_id)).first()
    if not area:
        return

    reactions_data: list[tuple[str, str, AreaReaction]] = session.exec(
        select(Service.name, Reaction.name, AreaReaction)
        .join(Reaction, Reaction.id == AreaReaction.reaction_id)
        .join(Service, Service.id == Reaction.service_id)
        .where(AreaReaction.area_id == area.id)
    ).all()
    if not reactions_data:
        return

    for service_name, reaction_name, area_reaction in reactions_data:
        services_dico[service_name].execute(
            reaction_name, session, area_reaction, area.user_id
        )


def compare_action_data(
    session: SessionDep,
    user_actions_config: dict[int, list[AreaAction]],
    action_data: tuple[Action, Service],
):
    for user_id, user_actions in user_actions_config.items():
        for user_action in user_actions:
            if not services_dico[action_data[1].name].check(
                action_data[0].name, session, user_action, user_id
            ):
                continue
            reaction_process(session, user_action.area_id)


@router.post("/")
def process_action(action_id: int, session: SessionDep):
    action_data: tuple[Action, Service] = session.exec(
        select(Action, Service)
        .join(Service, Service.id == Action.service_id)
        .where(Action.id == action_id)
    ).first()
    if not action_data:
        raise HTTPException(status_code=404, detail="Data not found")

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
        deleteJob(action_id)
        return

    user_actions_config: dict[int, list[AreaAction]] = {
        id: [] for id in set(next(zip(*user_actions_config_data)))
    }
    for id, data in user_actions_config_data:
        user_actions_config[id].append(data)

    compare_action_data(session, user_actions_config, action_data)
    return {}
