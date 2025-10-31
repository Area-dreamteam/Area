from core.config import settings
from services.services import get_json_services, get_json_services_login
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager

from core.db import init_db
from core.logger import logger
from api.api import api_router
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: initialize DB, services and cron jobs."""
    logger.info("Server starting...")
    init_db(get_json_services(), get_json_services_login())
    logger.debug(get_json_services_login())
    yield
    logger.info("Server shutting down...")


templates = Jinja2Templates(directory="templates")

app = FastAPI(
    lifespan=lifespan,
    title="AREA API",
    version="1.0.0",
    description="Automation platform connecting services through action-reaction workflows",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    openapi_tags=[
        {"name": "auth", "description": "Authentication operations"},
        {"name": "oauth", "description": "OAuth service integration"},
        {"name": "users", "description": "User management"},
        {"name": "services", "description": "External service management"},
        {"name": "actions", "description": "Automation triggers"},
        {"name": "reactions", "description": "Automation responses"},
        {"name": "areas", "description": "Automation workflows"},
        {"name": "actions_process", "description": "Action processing"},
        {"name": "about", "description": "Application information"},
    ],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONT_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/images", StaticFiles(directory="./images"), name="images")

app.include_router(api_router, prefix="")
