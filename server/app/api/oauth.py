from services.services import get_json_services_login
from dependencies.roles import CurrentUserNoFail
from sqlmodel import select
from models.oauth.oauth_login import OAuthLogin
from pathlib import Path
from pydantic import BaseModel
from services import services
from dependencies.db import SessionDep
from fastapi import APIRouter, HTTPException
from schemas import OauthLoginGet


router = APIRouter()


@router.get("/index/{service}")
def index(service: str):
    raise HTTPException(
        status_code=302,
        detail=f"Redirecting to {service} OAuth",
        headers={"Location": services[service].oauth_link()},
    )


@router.get("/login_index/{service}")
def login_index(service: str):
    raise HTTPException(
        status_code=302,
        detail=f"Redirecting to {service} OAuth",
        headers={"Location": services[service].oauth_link()},
    )


@router.get("/oauth_token/{service}")
def oauth_token(service: str, code: str, session: SessionDep, user: CurrentUserNoFail):
    services[service].oauth_callback(session, code, user)


@router.get("/login_oauth_token/{service}")
def login_oauth_token(
    service: str, code: str, session: SessionDep, user: CurrentUserNoFail
):
    services[service].oauth_callback(session, code, user)


@router.get("/available_oauths")
def get_oauths(session: SessionDep) -> list[OauthLoginGet]:
    oauth_login: list[OAuthLogin] = session.exec(select(OAuthLogin)).all()
    return oauth_login


@router.get("/available_oauths_login")
def get_oauths_login(session: SessionDep) -> list[OauthLoginGet]:
    return get_json_services_login()
