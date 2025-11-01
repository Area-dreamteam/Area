from core.logger import logger
from models.users.user_service import UserService
from fastapi import APIRouter, HTTPException
from sqlmodel import select
from models import Service, Action, Reaction
from schemas import ServiceGet, ServiceIdGet, ActionShortInfo, ReactionShortInfo
from dependencies.db import SessionDep
from dependencies.roles import CurrentUser, CurrentUserNoFail
from services.services import services_dico

router = APIRouter(prefix="/services", tags=["services"])


@router.get(
    "/list",
    response_model=list[ServiceGet],
    summary="List all services",
    description="Get all available services for automation",
)
def get_service(session: SessionDep) -> list[ServiceGet]:
    services: list[Service] = session.exec(
        select(
            Service.id,
            Service.name,
            Service.image_url,
            Service.category,
            Service.color,
            Service.oauth_required,
        )
    ).all()
    return services


@router.get(
    "/{id}",
    response_model=ServiceIdGet,
    summary="Get service details",
    responses={404: {"description": "Service not found"}},
)
def get_service_by_id(id: int, session: SessionDep, _: CurrentUser) -> ServiceIdGet:
    service: Service = session.exec(select(Service).where(Service.id == id)).first()
    if not service:
        raise HTTPException(status_code=404, detail="Data not found")

    service_data = ServiceIdGet(
        id=service.id,
        name=service.name,
        description=service.description,
        image_url=service.image_url,
        category=service.category,
        color=service.color,
        oauth_required=service.oauth_required,
    )
    return service_data


@router.get(
    "/{id}/actions",
    response_model=list[ActionShortInfo],
    summary="Get service actions",
    description="List all trigger actions available for this service",
)
def get_actions_of_service(
    id: int, session: SessionDep, _: CurrentUser
) -> list[ActionShortInfo]:
    actions_data: list[ActionShortInfo] = []

    actions: list[Action] = session.exec(
        select(Action).where(Action.service_id == id)
    ).all()
    for action in actions:
        action_data = ActionShortInfo(
            id=action.id, name=action.name, description=action.description
        )
        actions_data.append(action_data)
    return actions_data


@router.get(
    "/{id}/reactions",
    response_model=list[ReactionShortInfo],
    summary="Get service reactions",
    description="List all response reactions available for this service",
)
def get_reactions_of_service(
    id: int, session: SessionDep, _: CurrentUser
) -> list[ReactionShortInfo]:
    reactions_data: list[ReactionShortInfo] = []

    reactions: list[Reaction] = session.exec(
        select(Reaction).where(Reaction.service_id == id)
    ).all()
    for reaction in reactions:
        reaction_data = ReactionShortInfo(
            id=reaction.id, name=reaction.name, description=reaction.description
        )
        reactions_data.append(reaction_data)
    return reactions_data


@router.get(
    "/{id}/is_connected",
    response_model=dict,
    summary="Check service connection",
    description="Check if current user has connected this service",
)
def is_service_connected(id: int, session: SessionDep, user: CurrentUserNoFail) -> dict:
    service_name: str = session.exec(
        select(Service.name)
        .join(UserService, UserService.service_id == Service.id)
        .where(UserService.service_id == id, UserService.user_id == user.id)
    ).first()
    logger.debug(service_name)
    if service_name is None:
        return {"is_connected": False}

    if services_dico[service_name].is_connected(session, user.id) is True:
        return {"is_connected": True}

    user_service: UserService = session.exec(
        select(UserService)
        .join(Service, Service.id == UserService.service_id)
        .where(Service.name == service_name)
    ).first()
    if not user_service:
        return {"is_connected": False}

    session.delete(user_service)
    session.commit()
    return {"is_connected": False}


@router.delete("/{id}/disconnect")
def disconnect_service(id: int, session: SessionDep, user: CurrentUser):
    user_service: UserService = session.exec(
        select(UserService).where(
            UserService.service_id == id, UserService.user_id == user.id
        )
    ).first()
    if not user_service:
        raise HTTPException(status_code=400, detail="User service not found")

    session.delete(user_service)
    session.commit()
    return {
        "message": "Service disconnected",
        "service_id": user_service.id,
        "user_id": user.id,
    }
