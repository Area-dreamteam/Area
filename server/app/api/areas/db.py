from fastapi import APIRouter, HTTPException
from sqlmodel import select
from models import Area, Action, AreaAction, Service, AreaReaction, Reaction
from schemas import (
    ActionBasicInfo,
    ReactionBasicInfo,
    ActionInfo,
    ReactionInfo,
    ServiceGet,
)
from dependencies.db import SessionDep

router = APIRouter(prefix="/areas", tags=["areas"])


def get_area_action_info(session: SessionDep, area: Area) -> ActionInfo:
    """Get action configuration for an area."""
    action_area: AreaAction = session.exec(
        select(AreaAction).where(AreaAction.area_id == area.id)
    ).first()
    if not action_area:
        raise HTTPException(status_code=404, detail="Action area not found")

    action: Action = session.exec(
        select(Action).where(Action.id == action_area.action_id)
    ).first()
    if not action:
        raise HTTPException(status_code=404, detail="Action not found")

    service: Service = session.exec(
        select(Service).where(Service.id == action.service_id)
    ).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    service = ServiceGet(
        id=service.id,
        name=service.name,
        image_url=service.image_url,
        category=service.category,
        color=service.color,
    )
    area_action_data = ActionInfo(
        id=action.id, name=action.name, description=action.description, service=service, config=action_area.config
    )
    return area_action_data


def get_area_reactions_info(session: SessionDep, area: Area) -> list[ReactionInfo]:
    """Get all reaction configurations for an area."""
    reactions_area: AreaReaction = session.exec(
        select(AreaReaction).where(AreaReaction.area_id == area.id)
    ).all()
    if not reactions_area:
        raise HTTPException(status_code=404, detail="Reaction area not found")

    area_reactions_data: list[ReactionBasicInfo] = []
    for reaction_area in reactions_area:
        reaction: Reaction = session.exec(
            select(Reaction).where(Reaction.id == reaction_area.reaction_id)
        ).first()
        if not reaction:
            raise HTTPException(status_code=404, detail="Data not found")

        service: Service = session.exec(
            select(Service).where(Service.id == reaction.service_id)
        ).first()
        if not service:
            raise HTTPException(status_code=404, detail="Data not found")

        service = ServiceGet(
            id=service.id,
            name=service.name,
            image_url=service.image_url,
            category=service.category,
            color=service.color,
        )
        area_reaction_data = ReactionInfo(
            id=reaction.id,
            name=reaction.name,
            description=reaction.description,
            service=service,
            config=reaction_area.config
        )
        area_reactions_data.append(area_reaction_data)
    return area_reactions_data

def get_area_action_basic_info(session: SessionDep, area: Area) -> ActionBasicInfo:
    """Get action configuration for an area."""
    action_area: AreaAction = session.exec(
        select(AreaAction).where(AreaAction.area_id == area.id)
    ).first()
    if not action_area:
        raise HTTPException(status_code=404, detail="Action area not found")

    action: Action = session.exec(
        select(Action).where(Action.id == action_area.action_id)
    ).first()
    if not action:
        raise HTTPException(status_code=404, detail="Action not found")

    service: Service = session.exec(
        select(Service).where(Service.id == action.service_id)
    ).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    service = ServiceGet(
        id=service.id,
        name=service.name,
        image_url=service.image_url,
        category=service.category,
        color=service.color,
    )
    area_action_data = ActionBasicInfo(
        id=action.id, name=action.name, description=action.description, service=service
    )
    return area_action_data


def get_area_reactions_basic_info(session: SessionDep, area: Area) -> list[ReactionBasicInfo]:
    """Get all reaction configurations for an area."""
    reactions_area: AreaReaction = session.exec(
        select(AreaReaction).where(AreaReaction.area_id == area.id)
    ).all()
    if not reactions_area:
        raise HTTPException(status_code=404, detail="Reaction area not found")

    area_reactions_data: list[ReactionBasicInfo] = []
    for reaction_area in reactions_area:
        reaction: Reaction = session.exec(
            select(Reaction).where(Reaction.id == reaction_area.reaction_id)
        ).first()
        if not reaction:
            raise HTTPException(status_code=404, detail="Data not found")

        service: Service = session.exec(
            select(Service).where(Service.id == reaction.service_id)
        ).first()
        if not service:
            raise HTTPException(status_code=404, detail="Data not found")

        service = ServiceGet(
            id=service.id,
            name=service.name,
            image_url=service.image_url,
            category=service.category,
            color=service.color,
        )
        area_reaction_data = ReactionBasicInfo(
            id=reaction.id,
            name=reaction.name,
            description=reaction.description,
            service=service,
        )
        area_reactions_data.append(area_reaction_data)
    return area_reactions_data