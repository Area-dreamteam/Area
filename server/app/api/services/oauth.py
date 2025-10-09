from dependencies.roles import CurrentUserNoFail
from services.service import services
from dependencies.db import SessionDep
from fastapi import APIRouter, HTTPException


router = APIRouter(tags=["services"], prefix="")


@router.get("/index/{service}")
def index(service: str):
    raise HTTPException(
        status_code=302,
        detail="Redirecting to GitHub OAuth",
        headers={"Location": services[service].oauth_link()},
    )


@router.get("/login_index/{service}")
def login_index(service: str):
    raise HTTPException(
        status_code=302,
        detail="Redirecting to GitHub OAuth",
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
