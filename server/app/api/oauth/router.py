from models.services.service import Service
from dependencies.roles import CurrentUser, CurrentUserNoFail
from sqlmodel import select
from models import OAuthLogin, UserOAuthLogin, User
from services.services import services_oauth, services_dico
from dependencies.db import SessionDep
from fastapi import APIRouter, HTTPException, Request, Query
from schemas import OauthLoginGet
from core.utils import generate_state
from core.oauth_state import store_oauth_state, get_user_from_state
from core.security import decode_jwt
from core.logger import logger
from typing import Optional


router = APIRouter(prefix="/oauth", tags=["oauth"])


@router.get("/test_state")
def test_state(session: SessionDep, user: CurrentUser):
    """Test endpoint to verify state management works"""
    state = generate_state()
    store_oauth_state(state, user.id)
    logger.debug(f"Stored state {state} for user {user.id}")

    state_data = get_user_from_state(state)
    logger.debug(f"Retrieved state_data: {state_data}, type: {type(state_data)}")

    if state_data is None:
        return {"error": "Failed to retrieve user_id from state"}

    retrieved_id, is_mobile = state_data
    retrieved_user = session.get(User, int(retrieved_id))
    logger.debug(f"Retrieved user: {retrieved_user}, type: {type(retrieved_user)}")

    return {
        "status": "success",
        "original_user_id": user.id,
        "retrieved_user_id": retrieved_id,
        "is_mobile": is_mobile,
        "retrieved_user_email": retrieved_user.email if retrieved_user else None,
    }


@router.get(
    "/index/{service}",
    summary="Start OAuth flow",
    description="Redirect to service OAuth authorization",
)
def index(
    service: str,
    session: SessionDep,
    user: CurrentUserNoFail,
    mobile: bool = False,
    token: Optional[str] = Query(None),
):
    actual_user = user
    if mobile and token and actual_user is None:
        token_to_decode = token
        if token_to_decode.startswith("Bearer "):
            token_to_decode = token_to_decode[7:]
        payload = decode_jwt(token_to_decode)
        if not payload:
            raise HTTPException(status_code=403, detail="Invalid authorization token")
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=403, detail="Invalid token")
        actual_user = session.get(User, int(user_id))
        if actual_user is None:
            raise HTTPException(status_code=403, detail="User not found")
    elif actual_user is None:
        raise HTTPException(status_code=403, detail="Authentication required")

    if service not in services_dico:
        raise HTTPException(
            status_code=404,
            detail=f"{service} service not found",
        )

    state = generate_state()
    store_oauth_state(state, actual_user.id, is_mobile=mobile)
    oauth_url = services_dico[service].oauth_link(state=state)
    logger.debug(
        f"Stored state {state} for user {actual_user.id}, mobile={mobile}, redirecting to: {oauth_url}"
    )

    raise HTTPException(
        status_code=302,
        detail=f"Redirecting to {service} OAuth",
        headers={"Location": oauth_url},
    )


@router.get(
    "/login_index/{service}",
    summary="Start OAuth login flow",
    description="Redirect to service OAuth for login",
)
@router.get("/login_index/{service}")
def login_index(service: str, mobile: bool = False):
    if service not in services_oauth:
        raise HTTPException(
            status_code=404,
            detail=f"{service} service not found",
        )

    state = generate_state()
    store_oauth_state(state, user_id=-1, is_mobile=mobile)
    logger.debug(
        f"Stored login state {state}, mobile={mobile}, redirecting to {service} OAuth"
    )

    oauth_url = services_oauth[service].oauth_link(state=state)
    raise HTTPException(
        status_code=302,
        detail=f"Redirecting to {service} OAuth",
        headers={"Location": oauth_url},
    )


@router.get("/oauth_token/{service}")
def oauth_token(
    service: str,
    code: str,
    session: SessionDep,
    user: CurrentUserNoFail,
    request: Request,
    state: Optional[str] = None,
    mobile: bool = False,
):
    logger.debug(
        f"Callback received - service: {service}, state: {state}, has_cookie_user: {user is not None}"
    )

    actual_user = user
    is_mobile = mobile

    if state:
        logger.debug(f"Looking up state token: {state}")
        state_data = get_user_from_state(state)
        logger.debug(f"State lookup result: {state_data}")

        if state_data is None:
            if actual_user is None:
                raise HTTPException(
                    status_code=403,
                    detail="Invalid or expired OAuth state token and no cookie authentication",
                )
            logger.debug(
                f"State token invalid, using cookie authentication for user {actual_user.id}"
            )
        else:
            user_id, is_mobile = state_data
            logger.debug(f"Fetching user from database with id={user_id}")
            actual_user = session.get(User, int(user_id))
            logger.debug(
                f"Database query result: actual_user={actual_user}, type={type(actual_user)}"
            )
            if actual_user is None:
                raise HTTPException(status_code=403, detail="User not found")
            logger.debug(
                f"Successfully authenticated via state token for user {user_id}, is_mobile={is_mobile}"
            )
    elif actual_user is None:
        raise HTTPException(status_code=403, detail="Authentication required")

    return services_dico[service].oauth_callback(
        session, code, actual_user, request, is_mobile
    )


@router.get("/login_oauth_token/{service}")
def login_oauth_token(
    service: str,
    code: str,
    session: SessionDep,
    user: CurrentUserNoFail,
    request: Request,
    state: Optional[str] = None,
    mobile: bool = False,
):
    is_mobile = mobile

    if state:
        logger.debug(f"Login callback - Looking up state token: {state}")
        state_data = get_user_from_state(state)
        logger.debug(f"Login state lookup result: {state_data}")

        if state_data is not None:
            user_id, is_mobile = state_data
            logger.debug(
                f"Retrieved mobile flag from login state: is_mobile={is_mobile}"
            )

    return services_oauth[service].oauth_callback(
        session, code, user, request, is_mobile
    )


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
    user_oauth_login = session.exec(
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
