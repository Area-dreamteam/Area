from fastapi import APIRouter, HTTPException
from sqlmodel import select
from models import Area, User, Action, AreaAction, Service, AreaReaction
from schemas import AreaGet, AreaIdGet, AreaGetPublic, AreaIdGetPublic, UserShortInfo, ActionBasicInfo, ReactionBasicInfo, ServiceGet, CreateArea
from dependencies.db import SessionDep
from dependencies.roles import CurrentUser

router = APIRouter()

def get_area_action_info(session: SessionDep, area: Area) -> ActionBasicInfo:
    action_area: AreaAction = session.exec(select(AreaAction).where(AreaAction.area_id == area.id)).first()
    if not action_area:
        raise HTTPException(status_code=404, detail="Data not found")

    action: Action = session.exec(select(Action).where(Action.id == action_area.action_id)).first()
    if not action:
        raise HTTPException(status_code=404, detail="Data not found")

    service: Service = session.exec(select(Service).where(Service.id == action.service_id)).first()
    if not service:
        raise HTTPException(status_code=404, detail="Data not found")

    service = ServiceGet(id=service.id, name=service.name, image_url=service.image_url, category=service.category, color=service.color)
    area_action_data = ActionBasicInfo(id=action.id, name=action.name, description=action.description, service=service)
    return area_action_data

def get_area_reactions_info(session: SessionDep, area: Area) -> ReactionBasicInfo:
    reactions_area: AreaReaction = session.exec(select(AreaReaction).where(AreaReaction.area_id == area.id)).all()
    if not reactions_area:
        raise HTTPException(status_code=404, detail="Data not found")

    area_reactions_data: list[ReactionBasicInfo] = []
    for reaction_area in reactions_area:
        reaction: Action = session.exec(select(Action).where(Action.id == reaction_area.reaction_id)).first()
        if not reaction:
            raise HTTPException(status_code=404, detail="Data not found")

        service: Service = session.exec(select(Service).where(Service.id == reaction.service_id)).first()
        if not service:
            raise HTTPException(status_code=404, detail="Data not found")

        service = ServiceGet(id=service.id, name=service.name, image_url=service.image_url, category=service.category, color=service.color)
        area_reaction_data = ReactionBasicInfo(id=reaction.id, name=reaction.name, description=reaction.description, service=service)
        area_reactions_data.append(area_reaction_data)
    return area_reactions_data

@router.get("/areas", response_model=list[AreaGet])
def get_areas(session: SessionDep, _: CurrentUser) -> list[AreaGet]:
    areas: list[Area] = session.exec(select(Area)).all()

    areas_data: list[AreaGet] = []
    for area in areas:
        user: User = session.exec(select(User).where(User.id == area.user_id)).first()
        if not user:
            raise HTTPException(status_code=404, detail="Data not found")

        action_data: ActionBasicInfo = get_area_action_info(session, area)
        user_data = UserShortInfo(id=user.id, name=user.name)
        area_data = AreaGet(id=area.id, name=area.name, description=area.description, user=user_data, enable=area.enable, created_at=area.created_at, color=action_data.service.color)
        areas_data.append(area_data)
    return areas_data

@router.post("/areas")
def create_area(area: CreateArea, session: SessionDep,  user: CurrentUser):
    new_area = Area(user_id=user.id, name=area.name, description=area.description, enable=area.enable, created_at=None, is_public=area.is_public)
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

@router.delete("/areas/{id}")
def delete_area(id: int, session: SessionDep,  user: CurrentUser):
    area: Area = session.exec(select(Area).where(Area.id == id)).first()
    if not area:
        raise HTTPException(status_code=404, detail="Data not found")
    session.delete(area)
    session.commit()
    return {"message": "Area deleted", "area_id": area.id, "user_id": user.id}

@router.get("/areas/public", response_model=list[AreaGetPublic])
def get_areas_public(session: SessionDep) -> list[AreaGetPublic]:
    areas: list[Area] = session.exec(select(Area).where(Area.is_public == True)).all()

    areas_data: list[AreaGetPublic] = []
    for area in areas:
        user: User = session.exec(select(User).where(User.id == area.user_id)).first()
        if not user:
            raise HTTPException(status_code=404, detail="Data not found")

        action_data: ActionBasicInfo = get_area_action_info(session, area)
        user_data = UserShortInfo(id=user.id, name=user.name)
        area_data = AreaGetPublic(id=area.id, name=area.name, description=area.description, user=user_data, created_at=area.created_at, color=action_data.service.color)
        areas_data.append(area_data)
    return areas_data

@router.get("/areas/{id}", response_model=AreaIdGet)
def get_area_by_id(id: int, session: SessionDep, user: CurrentUser) -> AreaIdGet:
    area: Area = session.exec(select(Area).where(Area.id == id)).first()
    if not area:
        raise HTTPException(status_code=404, detail="Data not found")

    user: User = session.exec(select(User).where(User.id == area.user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="Data not found")

    action_data: ActionBasicInfo = get_area_action_info(session, area)
    reactions_data : list[ReactionBasicInfo] = get_area_reactions_info(session, area)

    user_data = UserShortInfo(id=user.id, name=user.name)
    area_info = AreaGet(id=area.id, name=area.name, description=area.description, user=user_data, enable=area.enable, created_at=area.created_at, color=action_data.service.color)
    
    area_data = AreaIdGet(area_info=area_info, action=action_data, reactions=reactions_data)
    return area_data

@router.get("/areas/public/{id}", response_model=AreaIdGetPublic)
def get_area_public_by_id(id: int, session: SessionDep) -> AreaIdGetPublic:
    area: Area = session.exec(select(Area).where(Area.id == id, Area.is_public == True)).first()
    if not area:
        raise HTTPException(status_code=404, detail="Data not found")

    user: User = session.exec(select(User).where(User.id == area.user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="Data not found")

    action_data: ActionBasicInfo = get_area_action_info(session, area)
    reactions_data : list[ReactionBasicInfo] = get_area_reactions_info(session, area)

    user_data = UserShortInfo(id=user.id, name=user.name)
    area_info = AreaGetPublic(id=area.id, name=area.name, description=area.description, user=user_data, created_at=area.created_at, color=action_data.service.color)
    
    area_data = AreaIdGetPublic(area_info=area_info, action=action_data, reactions=reactions_data)
    return area_data

# {
#     "name": "best area",
#     "description": "str",
#     "enable": false,
#     "is_public": false,
#     "action":
#         {
#             "action_id": 1,
#             "config": {}
#         },
#     "reactions":
#     [
#         {
#             "reaction_id": 1,
#             "config": {}
#         }
#     ]
# }