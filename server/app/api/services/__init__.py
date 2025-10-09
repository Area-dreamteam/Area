from fastapi import APIRouter


router = APIRouter(prefix="/services")

from . import services

router.include_router(services.router)
