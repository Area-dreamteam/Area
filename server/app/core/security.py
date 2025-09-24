from datetime import datetime, timedelta
from passlib.context import CryptContext
from typing import Dict, Tuple
from uuid import uuid4



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

active_tokens: Dict[str, Tuple[str, datetime]] = {}



def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_token(username: str, expires_in_minutes=30) -> str:
    token = str(uuid4())
    expires_at = datetime.utcnow() + timedelta(minutes=expires_in_minutes)
    active_tokens[token] = (username, expires_at)
    return token


def get_username_from_token(token: str) -> str | None:
    data = active_tokens.get(token)
    if not data:
        return None
    username, expires_at = data
    if datetime.utcnow() > expires_at:
        del active_tokens[token]
        return None
    return username
