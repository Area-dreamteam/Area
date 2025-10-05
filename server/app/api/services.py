from fastapi import APIRouter, HTTPException
from sqlmodel import select
from models import Service, Action, Reaction
from schemas import ServiceGet, ServiceIdGet, ActionShortInfo, ReactionShortInfo
from dependencies.db import SessionDep
from dependencies.roles import CurrentUser

router = APIRouter()

@router.get("/services", response_model=list[ServiceGet])
def get_service(session: SessionDep) -> list[ServiceGet]:
    services: list[Service] = session.exec(select(
        Service.id,
        Service.name,
        Service.image_url,
        Service.category,
        Service.color)
    ).all()
    return services

@router.get("/services/{id}", response_model=ServiceIdGet)
def get_service_by_id(id: int, session: SessionDep, _: CurrentUser) -> ServiceIdGet:
    service: Service = session.exec(select(Service).where(Service.id == id)).first()
    if not service:
        raise HTTPException(status_code=404, detail="Data not found")

    service_data = ServiceIdGet(id=service.id, name=service.name, description=service.description, image_url=service.image_url, category=service.category, color=service.color)
    return service_data

@router.get("/services/{id}/actions", response_model=list[ActionShortInfo])
def get_actions_of_service(id: int, session: SessionDep, _: CurrentUser) -> list[ActionShortInfo]:
    actions_data: list[ActionShortInfo] = []

    actions: list[Action] = session.exec(select(Action).where(Action.service_id == id)).all()
    for action in actions:
        action_data = ActionShortInfo(id=action.id, name=action.name, description=action.description)
        actions_data.append(action_data)
    return actions_data

@router.get("/services/{id}/reactions", response_model=list[ReactionShortInfo])
def get_reactions_of_service(id: int, session: SessionDep, _: CurrentUser) -> list[ReactionShortInfo]:
    reactions_data: list[ReactionShortInfo] = []

    reactions: list[Reaction] = session.exec(select(Reaction).where(Reaction.service_id == id)).all()
    for reaction in reactions:
        reaction_data = ReactionShortInfo(id=reaction.id, name=reaction.name, description=reaction.description)
        reactions_data.append(reaction_data)
    return reactions_data
