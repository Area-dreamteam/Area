from models.services.service import Service
from services.services import get_json_services_login
from dependencies.roles import CurrentUser, CurrentUserNoFail
from sqlmodel import select
from models.oauth.oauth_login import OAuthLogin
from services.services import services_oauth, services_dico
from dependencies.db import SessionDep
from fastapi import APIRouter, HTTPException
from schemas import OauthLoginGet


router = APIRouter(prefix="/oauth", tags=["oauth"])


@router.get(
    "/index/{service}",
    summary="Start OAuth flow",
    description="Redirect to service OAuth authorization"
)
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


@router.get(
    "/login_index/{service}",
    summary="Start OAuth login flow",
    description="Redirect to service OAuth for login"
)
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


@router.get(
    "/oauth_token/{service}",
    summary="Handle OAuth callback",
    description="Process OAuth authorization code"
)
def oauth_token(service: str, code: str, session: SessionDep, user: CurrentUser):
    return services_dico[service].oauth_callback(session, code, user)


@router.get("/login_oauth_token/{service}")
def login_oauth_token(
    service: str, code: str, session: SessionDep, user: CurrentUserNoFail
):
    return services_oauth[service].oauth_callback(session, code, user)


@router.get(
    "/available_oauths",
    summary="List OAuth services",
    description="Get all services supporting OAuth integration"
)
def get_oauths(session: SessionDep) -> list[OauthLoginGet]:
    oauths = session.exec(select(Service)).all()
    if not oauths:
        raise HTTPException(status_code=404, detail="Data not found")
    return oauths


@router.get("/available_oauths_login")
def get_oauths_login(session: SessionDep) -> list[OauthLoginGet]:
    oauths = session.exec(select(OAuthLogin)).all()
    if not oauths:
        raise HTTPException(status_code=404, detail="Data not found")
    return oauths
