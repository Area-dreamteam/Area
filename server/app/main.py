from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from contextlib import asynccontextmanager

from core.loader import load_services_catalog, load_services_config
from core.db import init_db
from core.logger import logger
from api import about, auth, services, actions, reactions, areas, users
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Server starting...")
    catalog: list[dict]= load_services_catalog()
    config: list[dict] = load_services_config()
    app.state.services_config = config
    init_db(catalog)
    yield
    logger.info("Server shutting down...")

app = FastAPI(lifespan=lifespan, title="AREA API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 
app.mount("/images", StaticFiles(directory="/images"), name='images')

@app.get("/")
async def root():
    return {"message": "Welcome to AREA API"}

app.include_router(about.router, tags=["about"])
app.include_router(auth.router, tags=["auth"], prefix="/auth")
app.include_router(services.router, tags=["services"])
app.include_router(actions.router, tags=["actions"])
app.include_router(reactions.router, tags=["reactions"])
app.include_router(areas.router, tags=["areas"])
app.include_router(users.router, tags=["users"])
