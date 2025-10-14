from cron.cron import print_jobs
from services.services import get_json_services, get_json_services_login
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager

from core.db import init_db
from core.logger import logger

from fastapi.middleware.cors import CORSMiddleware
from api import (
    about,
    auth,
    services,
    actions,
    reactions,
    areas,
    users,
    actions_process,
    oauth,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Server starting...")
    init_db(get_json_services(), get_json_services_login())
    print_jobs()
    logger.debug(get_json_services_login())
    yield
    logger.info("Server shutting down...")


templates = Jinja2Templates(directory="templates")

app = FastAPI(lifespan=lifespan, title="AREA API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/images", StaticFiles(directory="./images"), name="images")


@app.get("/")
async def root():
    return {"message": "Welcome to AREA API"}


app.include_router(services.router)
app.include_router(about.router, tags=["about"])
app.include_router(auth.router, tags=["auth"], prefix="/auth")
app.include_router(oauth.router, tags=["oauth"], prefix="/oauth")
app.include_router(services.router, tags=["services"])
app.include_router(actions.router, tags=["actions"])
app.include_router(reactions.router, tags=["reactions"])
app.include_router(areas.router, tags=["areas"])
app.include_router(users.router, tags=["users"])
app.include_router(actions_process.router, tags=["actions_process"])
