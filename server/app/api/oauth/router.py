from models.services.service import Service
from services.services import get_json_services_login
from dependencies.roles import CurrentUser, CurrentUserNoFail
from sqlmodel import select
from models import OAuthLogin, UserOAuthLogin
from services.services import services_oauth, services_dico
from dependencies.db import SessionDep
from fastapi import APIRouter, HTTPException
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
    if not oauths:
        raise HTTPException(status_code=404, detail="Data not found")
    return oauths


@router.get("/available_oauths_login")
def get_oauths_login(session: SessionDep) -> list[OauthLoginGet]:
    oauths = session.exec(select(OAuthLogin)).all()
    if not oauths:
        raise HTTPException(status_code=404, detail="Data not found")
    return oauths

@router.get("/oauth_login/{id}/disconnect")
def disconnect_oauth_login(id: int, session: SessionDep, user: CurrentUser):
    user_oauth_login: UserOAuthLogin = session.exec(
        select(UserOAuthLogin)
        .where(UserOAuthLogin.oauth_login_id == id, UserOAuthLogin.user_id == user.id)
    ).first()
    if not user_oauth_login:
        raise HTTPException(status_code=400, detail="User oauth login not found")

    session.delete(user_oauth_login)
    session.commit()
    return {"message": "Oauth login disconnected", "oauth_login_id": user_oauth_login.id, "user_id": user.id}
