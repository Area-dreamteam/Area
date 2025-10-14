from cron.cron import newJob, isCronExists
from fastapi import APIRouter, HTTPException
from sqlmodel import select
from models import Area, User, Action, AreaAction, Service, AreaReaction, Reaction
from schemas import AreaGet, UserShortInfo, ActionBasicInfo, ServiceGet, CreateArea, UpdateArea, AreaIdGet, Role
from dependencies.db import SessionDep
from dependencies.roles import CurrentUser

router = APIRouter(prefix="/users/areas", tags=["users_areas"])

def get_area_action_info(session: SessionDep, area: Area) -> ActionBasicInfo:
    action_area: AreaAction = session.exec(select(AreaAction).where(AreaAction.area_id == area.id)).first()
    if not action_area:
        raise HTTPException(status_code=404, detail="Action area not found")

    action: Action = session.exec(select(Action).where(Action.id == action_area.action_id)).first()
    if not action:
        raise HTTPException(status_code=404, detail="Action not found")

    service: Service = session.exec(select(Service).where(Service.id == action.service_id)).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    service = ServiceGet(id=service.id, name=service.name, image_url=service.image_url, category=service.category, color=service.color)
    area_action_data = ActionBasicInfo(id=action.id, name=action.name, description=action.description, service=service)
    return area_action_data

@router.get("/", response_model=list[AreaGet])
def get_user_areas(session: SessionDep, user: CurrentUser) -> list[AreaGet]:
    areas: list[Area] = session.exec(
        select(Area)
        .where(Area.user_id == user.id, Area.is_public == False)
    ).all()

    areas_data: list[AreaGet] = []
    for area in areas:
        action_data: ActionBasicInfo = get_area_action_info(session, area)
        user_data = UserShortInfo(id=user.id, name=user.name)
        area_data = AreaGet(id=area.id, name=area.name, description=area.description, user=user_data, enable=area.enable, created_at=area.created_at, color=action_data.service.color)
        areas_data.append(area_data)
    return areas_data

@router.get("/public", response_model=list[AreaGet])
def get_public_user_areas(session: SessionDep, user: CurrentUser) -> list[AreaGet]:
    areas: list[Area] = session.exec(
        select(Area)
        .where(Area.user_id == user.id, Area.is_public == True)
    ).all()

    areas_data: list[AreaGet] = []
    for area in areas:
        action_data: ActionBasicInfo = get_area_action_info(session, area)
        user_data = UserShortInfo(id=user.id, name=user.name)
        area_data = AreaGet(id=area.id, name=area.name, description=area.description, user=user_data, enable=area.enable, created_at=area.created_at, color=action_data.service.color)
        areas_data.append(area_data)
    return areas_data

@router.post("/")
def create_area(area: CreateArea, session: SessionDep,  user: CurrentUser):
    action: Action = session.exec(
        select(Action)
        .where(Action.id == area.action.action_id)
    ).first()
    if not action:
        raise HTTPException(status_code=404, detail="Action not found")

    for area_reaction in area.reactions:
        reaction: Reaction = session.exec(
            select(Reaction)
            .where(Reaction.id == area_reaction.reaction_id)
        ).first()
        if not reaction:
            raise HTTPException(status_code=404, detail="Reaction not found")

    new_area = Area(user_id=user.id, name=area.name, description=area.description, enable=False, created_at=None, is_public=False)
    session.add(new_area)
    session.commit()
    session.refresh(new_area)

    new_area_action = AreaAction(area_id=new_area.id, action_id=area.action.action_id, config=area.action.config)
    session.add(new_area_action)
    session.commit()
    session.refresh(new_area_action)

    for reaction in area.reactions:
        new_area_reaction = AreaReaction(area_id=new_area.id, reaction_id=reaction.reaction_id, config=reaction.config)
        session.add(new_area_reaction)
        session.commit()
        session.refresh(new_area_reaction)
    return {"message": "Area created", "area_id": new_area.id, "user_id": user.id}

@router.patch("/{id}", response_model=AreaIdGet)
def update_user_area(id: int, areaUpdate: UpdateArea, session: SessionDep,  user: CurrentUser):
    area: Area = session.exec(
        select(Area)
        .where(Area.id == id)
    ).first()
    if not area:
        raise HTTPException(status_code=404, detail="Data not found")
    if area.user_id != user.id and user.role != Role.ADMIN:
        raise HTTPException(status_code=403, detail="Permission Denied")
    
    # Update que les configs ou tout ?
    session.add(area)
    session.commit()
    session.refresh(area)
    return area

@router.patch("/{id}/enable")
def enable_user_area(id: int, session: SessionDep, user: CurrentUser, response_model=AreaIdGet):
    area: Area = session.exec(
        select(Area)
        .where(Area.id == id)
    ).first()
    if not area:
        raise HTTPException(status_code=404, detail="Data not found")
    if (area.user_id != user.id and user.role != Role.ADMIN) or area.is_public == True:
        raise HTTPException(status_code=403, detail="Permission Denied")

    area_action: AreaAction = session.exec(
        select(AreaAction)
        .where(AreaAction.area_id == area.id)
    ).first()
    if not area_action:
        raise HTTPException(status_code=404, detail="Data not found")

    area.enable = not area.enable
    if (area.enable):
        if isCronExists(area_action.action_id) is False:
            newJob(area_action.action_id)

    session.add(area)
    session.commit()
    session.refresh(area)
    return area

@router.delete("/public/{id}/unpublish")
def unpublished_user_public_area(id: int, session: SessionDep, user: CurrentUser):
    area: Area = session.exec(
        select(Area)
        .where(Area.id == id)
    ).first()
    if not area:
        raise HTTPException(status_code=404, detail="Data not found")
    if area.user_id != user.id and user.role != Role.ADMIN:
        raise HTTPException(status_code=403, detail="Permission Denied")
    if Area.is_public == False and user.role != Role.ADMIN:
        raise HTTPException(status_code=403, detail="Permission Denied")
    session.delete(area)
    session.commit()
    return {"message": "Area deleted", "area_id": area.id, "user_id": user.id}

@router.post("/{id}/publish")
def publish_user_area(id: int, session: SessionDep, user: CurrentUser):
    area: Area = session.exec(
        select(Area)
        .where(Area.id == id)
    ).first()
    if not area:
        raise HTTPException(status_code=404, detail="Data not found")
    if area.user_id != user.id and user.role != Role.ADMIN:
        raise HTTPException(status_code=403, detail="Permission Denied")

    # A faire: Créer une nouvelle area privée avec public=True et enable=False
    # area.is_public = True
    # area.enable = False

    # session.add(area)
    # session.commit()
    # session.refresh(area)
    return {}
