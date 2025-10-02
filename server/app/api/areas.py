from fastapi import APIRouter
from sqlmodel import select
from models import Area
from schemas import AreaGet, AreaIdGet, AreaGetPublic, AreaIdGetPublic
from dependencies.db import SessionDep

router = APIRouter()

@router.get("/areas", response_model=list[AreaGet])
def get_areas(session: SessionDep):
    return

@router.get("/areas/{id}", response_model=AreaIdGet)
def get_area_by_id(session: SessionDep):
    return

@router.get("/areas/public", response_model=list[AreaGetPublic])
def get_areas_public(session: SessionDep):
    return

@router.get("/areas/public/{id}", response_model=AreaIdGetPublic)
def get_area_public_by_id(session: SessionDep):
    return
