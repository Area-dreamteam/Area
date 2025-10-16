from fastapi import APIRouter

from .router import router as users_router
from .areas import router as user_areas_router

router = APIRouter()
router.include_router(users_router)
router.include_router(user_areas_router)
