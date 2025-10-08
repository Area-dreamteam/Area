from fastapi.security import APIKeyCookie
from fastapi import HTTPException, Security
from typing import Optional
from dependencies.db import SessionDep

from core.security import decode_jwt
from models import User

cookie_scheme = APIKeyCookie(name="access_token", auto_error=False)


def get_current_user(
    session: SessionDep, token: Optional[str] = Security(cookie_scheme)
) -> User:
    if not token:
        raise HTTPException(status_code=403, detail="Token missing.")

    if token.startswith("Bearer "):
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
