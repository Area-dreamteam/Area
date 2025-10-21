from fastapi import HTTPException
from sqlmodel import select
from models import Area, Action, AreaAction, Service, AreaReaction
from schemas import ActionBasicInfo, ServiceGet
from dependencies.db import SessionDep


def create_copy_area_action(
    session: SessionDep, new_area: int, area_action: AreaAction
):
    new_area_action = AreaAction(
        area_id=new_area, action_id=area_action.action_id, config=area_action.config
    )
    session.add(new_area_action)
    session.commit()


def create_copy_area_reaction(
    session: SessionDep, new_area: int, area_reactions: list[AreaReaction]
):
    for area_reaction in area_reactions:
        new_area_reaction = AreaReaction(
            area_id=new_area.id,
            reaction_id=area_reaction.reaction_id,
            config=area_reaction.config,
        )
        session.add(new_area_reaction)
        session.commit()
        session.refresh(new_area_reaction)


def create_copy_area(session: SessionDep, area: Area, is_public: bool):
    new_area = Area(
        user_id=area.user_id,
        name=area.name,
        description=area.description,
        enable=False,
        created_at=None,
        is_public=is_public,
    )
    session.add(new_area)
    session.commit()
    session.refresh(new_area)

    area_action: AreaAction = session.exec(
        select(AreaAction).where(AreaAction.area_id == area.id)
    ).first()
    if not area_action:
        raise HTTPException(status_code=404, detail="Area action not found")
    create_copy_area_action(session, new_area.id, area_action)

    area_reactions: list[AreaReaction] = session.exec(
        select(AreaReaction).where(AreaReaction.area_id == area.id)
    ).all()
    if not area_reactions:
        raise HTTPException(status_code=404, detail="Area reactions not found")
    create_copy_area_reaction(session, new_area, area_reactions)


def get_area_action_info(session: SessionDep, area: Area) -> ActionBasicInfo:
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
