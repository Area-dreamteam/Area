from models.services.service import Service
from services.services import get_json_services_login
from dependencies.roles import CurrentUser, CurrentUserNoFail
from sqlmodel import select
from models.oauth.oauth_login import OAuthLogin
from pathlib import Path
from pydantic import BaseModel
from services.services import services_oauth, services_dico
from dependencies.db import SessionDep
from fastapi import APIRouter, HTTPException
from schemas import OauthLoginGet


router = APIRouter()


@router.get("/index/{service}")
def index(service: str):
    if service not in services_dico:
        raise HTTPException(
            status_code=404,
            detail=f"{service} service not found",
        )

    raise HTTPException(
        status_code=302,
        detail=f"Redirecting to {service} OAuth",
        headers={"Location": services_dico[service].oauth_link()},
    )


@router.get("/login_index/{service}")
def login_index(service: str):
    if service not in services_oauth:
        raise HTTPException(
            status_code=404,
            detail=f"{service} service not found",
        )
    raise HTTPException(
        status_code=302,
        detail=f"Redirecting to {service} OAuth",
        headers={"Location": services_oauth[service].oauth_link()},
    )


@router.get("/oauth_token/{service}")
def oauth_token(service: str, code: str, session: SessionDep, user: CurrentUser):
    return services_dico[service].oauth_callback(session, code, user)


@router.get("/login_oauth_token/{service}")
def login_oauth_token(
    service: str, code: str, session: SessionDep, user: CurrentUserNoFail
):
    return services_oauth[service].oauth_callback(session, code, user)


@router.get("/available_oauths")
def get_oauths(session: SessionDep) -> list[OauthLoginGet]:
    oauths = session.exec(select(Service)).all()
    return oauths


@router.get("/available_oauths_login")
def get_oauths_login(session: SessionDep) -> list[OauthLoginGet]:
    return list(get_json_services_login().values())
