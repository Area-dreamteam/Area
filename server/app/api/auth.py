from fastapi import APIRouter, HTTPException
from sqlmodel import select

from models import User
from schemas import UserCreate, TokenResponse
from core.security import hash_password, verify_password, sign_jwt
from dependencies.db import SessionDep



router = APIRouter()



@router.post("/register")
def register(user: UserCreate, session: SessionDep):
    existing = session.exec(select(User).where(User.email == user.email)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password)
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return {"message": "User registered", "id": new_user.id, "email": new_user.email}


@router.post("/login", response_model=TokenResponse)
def login(user: UserCreate, session: SessionDep):
    db_user = session.exec(select(User).where(User.email == user.email)).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = sign_jwt(db_user.id)
    return TokenResponse(access_token=token)
