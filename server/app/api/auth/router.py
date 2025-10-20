from fastapi.responses import RedirectResponse
from fastapi import APIRouter, HTTPException, Cookie, Response
from sqlmodel import select
from urllib.parse import urlencode
from pydantic_core import ValidationError
from core.config import settings
import requests


from models import User
from schemas import UserCreate, TokenResponse, MessageResponse, UserRegistrationResponse
from core.security import hash_password, verify_password, sign_jwt
from dependencies.db import SessionDep
from core.config import settings


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=UserRegistrationResponse,
    summary="Register new user",
    responses={400: {"description": "Email already registered"}}
)
def register(user: UserCreate, session: SessionDep) -> UserRegistrationResponse:
    existing = session.exec(select(User).where(User.email == user.email)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        name=user.email.split("@")[0],
        email=user.email,
        password=hash_password(user.password),
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return UserRegistrationResponse(
        message="User registered",
        id=new_user.id,
        email=new_user.email
    )


@router.post(
    "/login",
    response_model=MessageResponse,
    summary="Authenticate user",
    description="Sets JWT token as httpOnly cookie",
    responses={400: {"description": "Invalid credentials"}}
)
def login(user: UserCreate, session: SessionDep, response: Response) -> MessageResponse:
    db_user = session.exec(select(User).where(User.email == user.email)).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = sign_jwt(db_user.id)

    response.set_cookie(
        key="access_token",
        value=f"Bearer {token}",
        httponly=True,
        secure=True,
        max_age=settings.ACCESS_TOKEN_EXPIRE_HOURS * 3600,
    )
    return MessageResponse(message="Logged successfully")


@router.post(
    "/logout",
    response_model=MessageResponse,
    summary="Logout user",
    description="Clears authentication cookie"
)
def logout(response: Response) -> MessageResponse:
    response.delete_cookie(key="access_token")
    return MessageResponse(message="Logged out successfully")
