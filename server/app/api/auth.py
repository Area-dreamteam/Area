from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from sqlmodel import select
from urllib.parse import urlencode
from pydantic_core import ValidationError
from core.config import settings
import requests


from models import User
from schemas.user import UserCreate, TokenResponse
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


@router.get("/login/oauth")
def login_oauth():
    base_url = "https://github.com/login/oauth/authorize"
    params = {
        "client_id": settings.GITHUB_CLIENT_ID,
        "redirect_uri": "http://127.0.0.1:8080/callback"
    }
    
    return RedirectResponse(f"{base_url}?{urlencode(params)}")

from pydantic import BaseModel
class OAuthTokenRes(BaseModel):
    access_token: str
    expires_in: int
    refresh_token: str
    refresh_token_expires_in: int

@router.get("/login/oauth_token")
def login_oauth_token(code: str):
    base_url = "https://github.com/login/oauth/access_token"
    params = {
        "client_id": settings.GITHUB_CLIENT_ID,
        "client_secret": settings.GITHUB_CLIENT_SECRET,
        "code": code
    }
    
    r = requests.post(f"{base_url}?{urlencode(params)}", headers={"Accept": "application/json"})
    if not r:
        return HTTPException(status_code=400, detail="Invalid code")
    
    try:
        data = OAuthTokenRes.model_validate(r.json())
        base_url = "https://api.github.com/user/emails"
        r = requests.get(f"{base_url}", headers={"Authorization": f"token {data.access_token}", "Accept": "application/json"})
        
        return f"test {r.json()}"
    except ValidationError:
        return HTTPException(status_code=400, detail="Invalid oauth return")
