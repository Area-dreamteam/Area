from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Annotated
from sqlmodel import select

from dependencies.db import SessionDep
from dependencies.auth import get_current_user
from sqlmodel import SQLModel, Field, Column, JSON, UniqueConstraint, Relationship



router = APIRouter()

class Hero(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str

@router.post("/heroes/")
def create_hero(
    hero: Hero,
    session: SessionDep
) -> Hero:
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero


@router.get("/heroes/")
def read_heroes(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100
) -> list[Hero]:
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes


@router.get("/heroes/{hero_id}")
def read_hero(
    hero_id: int,
    session: SessionDep
) -> Hero:
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero


@router.delete("/heroes/{hero_id}")
def delete_hero(
    hero_id: int,
    session: SessionDep
):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return {"ok": True}


# @router.delete("/heroes/{hero_id}")
# def delete_hero(
#     hero_id: int,
#     session: SessionDep,
#     user_id: str = Depends(get_current_user)
# ):
#     hero = session.get(Hero, hero_id)
#     if not hero:
#         raise HTTPException(status_code=404, detail="Hero not found")
#     session.delete(hero)
#     session.commit()
#     return {"ok": True}
