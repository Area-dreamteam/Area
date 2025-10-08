from models.users.user_service import UserService
from fastapi import APIRouter, HTTPException
from sqlmodel import select
from models import Service, Action, Reaction
from schemas import ServiceGet, ServiceIdGet, ActionShortInfo, ReactionShortInfo
from dependencies.db import SessionDep
from dependencies.roles import CurrentUser, CurrentUserNoFail


router = APIRouter(tags=["services"], prefix="")


@router.get("/", response_model=list[ServiceGet])
def get_service(session: SessionDep) -> list[ServiceGet]:
    services: list[Service] = session.exec(
        select(
            Service.id, Service.name, Service.image_url, Service.category, Service.color
        )
    ).all()
    return services


@router.get("/{id}", response_model=ServiceIdGet)
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
    )
    return service_data


@router.get("/{id}/actions", response_model=list[ActionShortInfo])
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


@router.get("/{id}/reactions", response_model=list[ReactionShortInfo])
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


@router.get("/{id}/is_connected", response_model=bool)
def is_service_connected(
    id: int | str, session: SessionDep, user: CurrentUserNoFail
) -> bool:
    if id.isnumeric():
        service = session.exec(
            select(UserService).where(
                UserService.service_id == id, UserService.user_id == user.id
            )
        ).first()
    elif isinstance(id, str):
        service = session.exec(
            select(UserService)
            .join(Service, Service.id == UserService.service_id)
            .where(Service.name == id, UserService.user_id == user.id)
        ).first()
    print("is connected: ", service is not None, "to :", id, "---", user)
    return service is not None
