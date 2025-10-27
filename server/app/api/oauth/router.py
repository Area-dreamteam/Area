from models.services.service import Service
from dependencies.roles import CurrentUser, CurrentUserNoFail
from sqlmodel import select
from models import OAuthLogin, UserOAuthLogin
from services.services import services_oauth, services_dico
from dependencies.db import SessionDep
from fastapi import APIRouter, HTTPException, Request
from schemas import OauthLoginGet


router = APIRouter(prefix="/oauth", tags=["oauth"])


@router.get(
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


<<<<<<< HEAD
@router.get(
    "/login_index/{service}",
    summary="Start OAuth login flow",
    description="Redirect to service OAuth for login",
)
def login_index(service: str):
=======
@router.get("/login_index/{service}")
def login_index(service: str, mobile: bool = False):
>>>>>>> 1a57a9f2bf7dce6211034b5ae7db745a8e4de84c
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


<<<<<<< HEAD
@router.get(
    "/oauth_token/{service}",
    summary="Handle OAuth callback",
    description="Process OAuth authorization code",
)
def oauth_token(service: str, code: str, session: SessionDep, user: CurrentUser):
    return services_dico[service].oauth_callback(session, code, user)
=======
@router.get("/oauth_token/{service}")
def oauth_token(service: str, code: str, session: SessionDep, user: CurrentUser, request: Request):
    return services_dico[service].oauth_callback(session, code, user, request)
>>>>>>> 1a57a9f2bf7dce6211034b5ae7db745a8e4de84c


@router.get("/login_oauth_token/{service}")
def login_oauth_token(
    service: str, code: str, session: SessionDep, user: CurrentUserNoFail, request: Request, state: str = None
):
    # Check if this is a mobile OAuth flow
    is_mobile = state == "mobile"
    return services_oauth[service].oauth_callback(session, code, user, request, is_mobile)


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
