from fastapi import APIRouter

from .router import router as reactions_router

router = APIRouter()
router.include_router(reactions_router)
