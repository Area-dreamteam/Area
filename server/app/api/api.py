from fastapi import APIRouter
from api import (
    about,
    services,
    areas,
    users,
    actions_process,
    oauth,
    auth,
    actions,
    reactions,
)
from core.oauth_state import cleanup_expired_states

api_router = APIRouter()


@api_router.get("/")
async def root():
    return {"message": "Welcome to AREA API"}


@api_router.get("/health")
async def health():
    cleanup_expired_states()
    return {"status": "ok"}


api_router.include_router(about.router)
api_router.include_router(auth.router)
api_router.include_router(oauth.router)
api_router.include_router(services.router)
api_router.include_router(actions.router)
api_router.include_router(reactions.router)
api_router.include_router(areas.router)
api_router.include_router(users.router)
api_router.include_router(actions_process.router)
