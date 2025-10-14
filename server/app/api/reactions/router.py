from fastapi import APIRouter, HTTPException
from sqlmodel import select
from models import Reaction, Service
from schemas import ReactionIdGet, ServiceGet
from dependencies.db import SessionDep
from dependencies.roles import CurrentUser

router = APIRouter(prefix="/reactions", tags=["reactions"])

@router.get("/{id}", response_model=ReactionIdGet)
def get_reaction_by_id(id: int, session: SessionDep, _: CurrentUser) -> ReactionIdGet:
    reaction: Reaction = session.exec(select(Reaction).where(Reaction.id == id)).first()
    if not reaction:
        raise HTTPException(status_code=404, detail="Data not found")

    service: Service = session.exec(select(Service).where(Service.id == reaction.service_id)).first()
    if not service:
        raise HTTPException(status_code=404, detail="Data not found")

    service_data = ServiceGet(id=service.id, name=service.name, image_url=service.image_url, category=service.category, color=service.color)
    reaction_data = ReactionIdGet(id=reaction.id, name=reaction.name, description=reaction.description, config_schema=reaction.config_schema, service=service_data)
    return reaction_data
