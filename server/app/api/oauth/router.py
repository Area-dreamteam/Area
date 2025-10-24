from models.services.service import Service
from services.services import get_json_services_login
from dependencies.roles import CurrentUser, CurrentUserNoFail
from sqlmodel import select
from models.oauth.oauth_login import OAuthLogin
from services.services import services_oauth, services_dico
from dependencies.db import SessionDep
from fastapi import APIRouter, HTTPException, Request
from schemas import OauthLoginGet


router = APIRouter(prefix="/oauth", tags=["oauth"])


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
def login_index(service: str, mobile: bool = False):
    if service not in services_oauth:
        raise HTTPException(
            status_code=404,
            detail=f"{service} service not found",
        )
    
    # Generate OAuth URL with mobile indicator if needed
    oauth_url = services_oauth[service].oauth_link()
    if mobile:
        # Add mobile indicator to the OAuth state or redirect URL
        separator = "&" if "?" in oauth_url else "?"
        oauth_url += f"{separator}state=mobile"
    
    raise HTTPException(
        status_code=302,
        detail=f"Redirecting to {service} OAuth",
        headers={"Location": oauth_url},
    )


@router.get("/oauth_token/{service}")
def oauth_token(service: str, code: str, session: SessionDep, user: CurrentUser, request: Request):
    return services_dico[service].oauth_callback(session, code, user, request)


@router.get("/login_oauth_token/{service}")
def login_oauth_token(
    service: str, code: str, session: SessionDep, user: CurrentUserNoFail, request: Request, state: str = None
):
    # Check if this is a mobile OAuth flow
    is_mobile = state == "mobile"
    return services_oauth[service].oauth_callback(session, code, user, request, is_mobile)


@router.get("/available_oauths")
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
