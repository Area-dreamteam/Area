from fastapi import APIRouter

from .router import router as services_router

router = APIRouter()
router.include_router(services_router)
