from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Annotated
from sqlmodel import select

from dependencies.db import SessionDep
from dependencies.auth import get_current_user
from models import Hero



router = APIRouter()



@router.post("/heroes/")
def create_hero(
    hero: Hero,
    session: SessionDep,
    username: str = Depends(get_current_user)
) -> Hero:
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero


@router.get("/heroes/")
def read_heroes(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
    username: str = Depends(get_current_user)
) -> list[Hero]:
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes


@router.get("/heroes/{hero_id}")
def read_hero(
    hero_id: int,
    session: SessionDep,
    username: str = Depends(get_current_user)
) -> Hero:
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero


@router.delete("/heroes/{hero_id}")
def delete_hero(
    hero_id: int,
    session: SessionDep,
    username: str = Depends(get_current_user)
):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return {"ok": True}
