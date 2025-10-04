from fastapi.security import APIKeyHeader
from fastapi import HTTPException, status, Security
from datetime import datetime

from core.security import decode_jwt



api_key_header = APIKeyHeader(name="Authorization", auto_error=False)



def get_current_user(token: str = Security(api_key_header)) -> str:
    payload = decode_jwt(token)
    
    if not payload:
        return HTTPException(status_code=403, detail="Invalid authorization token.")

    #TODO : check if the user_id is on the database

    return payload["user_id"]
