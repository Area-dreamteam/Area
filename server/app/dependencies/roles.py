from schemas import Role
from fastapi import HTTPException, Depends
from typing import Annotated
from .auth import get_current_user, get_current_user_no_fail

from models import User


def check_admin(user: Annotated[User, Depends(get_current_user)]) -> User:
    if user.role != Role.ADMIN:
        raise HTTPException(status_code=403, detail="Permission Denied.")
    return user


def check_user(user: Annotated[User, Depends(get_current_user)]) -> User:
    if user.role not in Role:
        raise HTTPException(status_code=403, detail="Permission Denied.")
    return user


CurrentAdmin = Annotated[User, Depends(check_admin)]
CurrentUser = Annotated[User, Depends(check_user)]
CurrentUserNoFail = Annotated[User, Depends(get_current_user_no_fail)]
