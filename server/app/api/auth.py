from fastapi import APIRouter, HTTPException, Cookie, Response
from sqlmodel import select

from models import User
from schemas import UserCreate, TokenResponse
from core.security import hash_password, verify_password, sign_jwt
from dependencies.db import SessionDep
from core.config import settings


router = APIRouter()



@router.post("/register")
def register(user: UserCreate, session: SessionDep):
    existing = session.exec(select(User).where(User.email == user.email)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        name=user.email.split("@")[0],
        email=user.email,
        password=hash_password(user.password)
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return {"message": "User registered", "id": new_user.id, "email": new_user.email}

@router.post("/login")
def login(user: UserCreate, session: SessionDep, response: Response):
    db_user = session.exec(select(User).where(User.email == user.email)).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = sign_jwt(db_user.id)
    response.set_cookie(
        key="access_token",
        value=f"Bearer {token}",
        httponly=True,
        secure=True,
        max_age=settings.ACCESS_TOKEN_EXPIRE_HOURS * 3600
    )
    return {"message": "Logged successfully"}

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"message": "Logged out successfully"}
