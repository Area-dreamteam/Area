from fastapi import APIRouter
from sqlmodel import select
from models import Service
from schemas import ServiceGet, ServiceIdGet, ActionShortInfo, ReactionShortInfo
from dependencies.db import SessionDep

router = APIRouter()

@router.get("/services", response_model=list[ServiceGet])
def get_service(session: SessionDep):
    services = session.exec(select(
        Service.id,
        Service.name,
        Service.image_url,
        Service.color)
    ).all()
    return services

@router.get("/services/{id}", response_model=ServiceIdGet)
def get_service_by_id(session: SessionDep):
    return

@router.get("/services/{id}/actions", response_model=list[ActionShortInfo])
def get_actions_of_service(session: SessionDep):
    return

@router.get("/services/{id}/reactions", response_model=list[ReactionShortInfo])
def get_reactions_of_service(session: SessionDep):
    return
