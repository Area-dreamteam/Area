from fastapi import APIRouter


router = APIRouter(prefix="/services")


from . import github

router.include_router(github.router)

from . import todoist

router.include_router(todoist.router)

from . import services

router.include_router(services.router)
