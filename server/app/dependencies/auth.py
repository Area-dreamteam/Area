from fastapi.security import APIKeyHeader
from fastapi import HTTPException, status, Security
from datetime import datetime

from core.security import active_tokens



api_key_header = APIKeyHeader(name="Authorization", auto_error=False)



def get_current_user(token: str = Security( api_key_header)) -> str:
    if not token or token not in active_tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token",
        )

    username, expires_at = active_tokens[token]
    if datetime.utcnow() > expires_at:
        del active_tokens[token]
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )

    return username
