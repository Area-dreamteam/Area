from fastapi import APIRouter, HTTPException
from sqlmodel import select
from models import Area, User
from schemas import (
    AreaGet,
    AreaIdGet,
    AreaGetPublic,
    AreaIdGetPublic,
    UserShortInfo,
    ActionBasicInfo,
    ReactionBasicInfo,
    ActionInfo,
    ReactionInfo,
    Role,
    AreaDeletionResponse,
)
from dependencies.db import SessionDep
from dependencies.roles import CurrentUser
from api.users.areas.db import create_copy_area
from api.areas.db import get_area_action_basic_info, get_area_action_info, get_area_reactions_basic_info, get_area_reactions_info

router = APIRouter(prefix="/areas", tags=["areas"])


@router.get(
    "/public",
    response_model=list[AreaGetPublic],
    summary="Get public areas",
    description="Browse automation areas shared by the community",
)
def get_areas_public(session: SessionDep) -> list[AreaGetPublic]:
    areas: list[Area] = session.exec(select(Area).where(Area.is_public == True)).all()

    areas_data: list[AreaGetPublic] = []
    for area in areas:
        user: User = session.exec(select(User).where(User.id == area.user_id)).first()
        if not user:
            raise HTTPException(status_code=404, detail="Data not found")

        action_data: ActionBasicInfo = get_area_action_info(session, area)
        user_data = UserShortInfo(id=user.id, name=user.name)
        area_data = AreaGetPublic(
            id=area.id,
            name=area.name,
            description=area.description,
            user=user_data,
            created_at=area.created_at,
            color=action_data.service.color,
        )
        areas_data.append(area_data)
    return areas_data


@router.get(
    "/{id}",
    response_model=AreaIdGet,
    summary="Get area details",
    description="Get complete area configuration (owner/admin only)",
    responses={
        403: {"description": "Access denied"},
        404: {"description": "Area not found"},
    },
)
def get_area_by_id(id: int, session: SessionDep, user: CurrentUser) -> AreaIdGet:
    area: Area = session.exec(select(Area).where(Area.id == id)).first()
    if not area:
        raise HTTPException(status_code=404, detail="Data not found")
    if area.user_id != user.id and user.role != Role.ADMIN:
        raise HTTPException(status_code=403, detail="Permission Denied")

    action_data: ActionInfo = get_area_action_info(session, area)
    reactions_data: list[ReactionInfo] = get_area_reactions_info(session, area)

    user_data = UserShortInfo(id=user.id, name=user.name)
    area_info = AreaGet(
        id=area.id,
        name=area.name,
        description=area.description,
        user=user_data,
        enable=area.enable,
        created_at=area.created_at,
        color=action_data.service.color,
    )

    area_data = AreaIdGet(
        area_info=area_info, action=action_data, reactions=reactions_data
    )
    return area_data


@router.delete(
    "/{id}",
    response_model=AreaDeletionResponse,
    summary="Delete area",
    description="Permanently delete area and stop its automation",
    responses={
        403: {"description": "Access denied"},
        404: {"description": "Area not found"},
    },
)
def delete_area(
    id: int, session: SessionDep, user: CurrentUser
) -> AreaDeletionResponse:
    area: Area = session.exec(select(Area).where(Area.id == id)).first()
    if not area:
        raise HTTPException(status_code=404, detail="Data not found")
    if area.user_id != user.id and user.role != Role.ADMIN:
        raise HTTPException(status_code=403, detail="Permission Denied")
    session.delete(area)
    session.commit()
    return AreaDeletionResponse(
        message="Area deleted", area_id=area.id, user_id=user.id
    )


@router.get(
    "/public/{id}",
    response_model=AreaIdGetPublic,
    summary="Get public area details",
    description="Get complete details of a public area",
    responses={404: {"description": "Public area not found"}},
)
def get_area_public_by_id(id: int, session: SessionDep) -> AreaIdGetPublic:
    area: Area = session.exec(
        select(Area).where(Area.id == id, Area.is_public == True)
    ).first()
    if not area:
        raise HTTPException(status_code=404, detail="Data not found")

    user: User = session.exec(select(User).where(User.id == area.user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="Data not found")

    action_data: ActionBasicInfo = get_area_action_basic_info(session, area)
    reactions_data: list[ReactionBasicInfo] = get_area_reactions_basic_info(session, area)

    user_data = UserShortInfo(id=user.id, name=user.name)
    area_info = AreaGetPublic(
        id=area.id,
        name=area.name,
        description=area.description,
        user=user_data,
        created_at=area.created_at,
        color=action_data.service.color,
    )

    area_data = AreaIdGetPublic(
        area_info=area_info, action=action_data, reactions=reactions_data
    )
    return area_data


@router.post(
    "/public/{id}/copy",
    summary="Copy a public area",
    description="Copy a public area to your private areas section",
    responses={404: {"description": "Public area not found"}},
)
def copy_area_public_by_id(id: int, session: SessionDep, user: CurrentUser):
    area: Area = session.exec(
        select(Area).where(Area.id == id, Area.is_public == True)
    ).first()
    if not area:
        raise HTTPException(status_code=404, detail="Data not found")

    create_copy_area(session, area, False)
    return {"message": "Area copy", "area_id": area.id, "user_id": user.id}
