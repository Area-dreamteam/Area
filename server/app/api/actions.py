from fastapi import APIRouter, HTTPException
from sqlmodel import select
from models import Action, Service
from schemas import ActionIdGet, ServiceGet
from dependencies.db import SessionDep
from dependencies.roles import CurrentUser

router = APIRouter()

@router.get("/actions/{id}", response_model=ActionIdGet)
def get_action_by_id(id: int, session: SessionDep, _: CurrentUser) -> ActionIdGet:
    action: Action = session.exec(select(Action).where(Action.id == id)).first()
    if not action:
        raise HTTPException(status_code=404, detail="Data not found")

    service: Service = session.exec(select(Service).where(Service.id == action.service_id)).first()
    if not service:
        raise HTTPException(status_code=404, detail="Data not found")

    service_data = ServiceGet(id=service.id, name=service.name, image_url=service.image_url, color=service.color)
    action_data = ActionIdGet(id=action.id, name=action.name, description=action.description, config_schema=action.config_schema, service=service_data)
    return action_data
