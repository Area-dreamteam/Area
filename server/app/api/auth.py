# from fastapi import APIRouter, HTTPException
# from sqlmodel import select

# from models_test import UserCreate, User, TokenResponse
# from core.security import hash_password, verify_password, create_token
# from dependencies.db import SessionDep



# router = APIRouter()



# @router.post("/register/")
# def register(user: UserCreate, session: SessionDep):
#     existing = session.exec(select(User).where(User.username == user.username)).first()
#     if existing:
#         raise HTTPException(status_code=400, detail="Username already exists")

#     new_user = User(
#         username=user.username,
#         hashed_password=hash_password(user.password)
#     )
#     session.add(new_user)
#     session.commit()
#     return {"msg": "User registered"}


# @router.post("/login/", response_model=TokenResponse)
# def login(user: UserCreate, session: SessionDep):
#     db_user = session.exec(select(User).where(User.username == user.username)).first()
#     if not db_user or not verify_password(user.password, db_user.hashed_password):
#         raise HTTPException(status_code=400, detail="Invalid username or password")
    
#     return TokenResponse(token=create_token(user.username))
