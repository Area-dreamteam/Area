from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from contextlib import asynccontextmanager

from core.loader import load_services_catalog, load_services_config
from core.db import init_db
from core.logger import logger
from api import about
from api import auth

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
 
app.mount("/images", StaticFiles(directory="/images"), name='images')

@app.get("/")
async def root():
    return {"message": "Welcome to AREA API"}

app.include_router(about.router, tags=["about"])
app.include_router(auth.router, tags=["auth"], prefix="/auth")
