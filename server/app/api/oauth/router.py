from models.services.service import Service
from dependencies.roles import CurrentUser, CurrentUserNoFail
from sqlmodel import select
from models import OAuthLogin, UserOAuthLogin
from services.services import services_oauth, services_dico
from dependencies.db import SessionDep
from fastapi import APIRouter, HTTPException
from schemas import OauthLoginGet


router = APIRouter(prefix="/oauth", tags=["oauth"])


@router.post(
    "/index/{service}",
    summary="Start OAuth flow",
    description="Redirect to service OAuth authorization",
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


@router.post(
    "/login_index/{service}",
    summary="Start OAuth login flow",
    description="Redirect to service OAuth for login",
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


@router.post(
    "/oauth_token/{service}",
    summary="Handle OAuth callback",
    description="Process OAuth authorization code",
)
def oauth_token(service: str, code: str, session: SessionDep, user: CurrentUser):
    return services_dico[service].oauth_callback(session, code, user)


@router.post("/login_oauth_token/{service}")
def login_oauth_token(
    service: str, code: str, session: SessionDep, user: CurrentUserNoFail
):
    return services_oauth[service].oauth_callback(session, code, user)


@router.get(
    "/available_oauths",
    summary="List OAuth services",
    description="Get all services supporting OAuth integration",
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


@router.delete("/oauth_login/{id}/disconnect")
def disconnect_oauth_login(id: int, session: SessionDep, user: CurrentUser):
    user_oauth_login: UserOAuthLogin = session.exec(
        select(UserOAuthLogin).where(
            UserOAuthLogin.oauth_login_id == id, UserOAuthLogin.user_id == user.id
        )
    ).first()
    if not user_oauth_login:
        raise HTTPException(status_code=400, detail="User oauth login not found")

    session.delete(user_oauth_login)
    session.commit()
    return {
        "message": "Oauth login disconnected",
        "oauth_login_id": user_oauth_login.id,
        "user_id": user.id,
    }
