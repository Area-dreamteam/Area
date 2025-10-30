from fastapi import APIRouter

from .router import router as oauth_router

router = APIRouter()
router.include_router(oauth_router)
