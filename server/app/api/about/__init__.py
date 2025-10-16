from fastapi import APIRouter

from .router import router as about_router

router = APIRouter()
router.include_router(about_router)
