from fastapi.security import APIKeyHeader
from fastapi import HTTPException, Security, Depends
from typing import Annotated
from dependencies.db import SessionDep
from sqlmodel import Session

from core.security import decode_jwt
from models import User


api_key_header = APIKeyHeader(name="Authorization", auto_error=False)



def get_current_user(session: SessionDep, token: str = Security( api_key_header)) -> User:
    if not token:
        raise HTTPException(status_code=403, detail="Token missing.")

    if token.startswith("bearer "):
        token = token[7:]
    payload = decode_jwt(token)

    if not payload:
        raise HTTPException(status_code=403, detail="Invalid authorization token.")

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=403, detail="Invalid token.")
    user_id = int(user_id)

    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=403, detail="User not found.")
    return user
