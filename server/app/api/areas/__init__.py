from fastapi import APIRouter

from .router import router as areas_router

router = APIRouter()
router.include_router(areas_router)
