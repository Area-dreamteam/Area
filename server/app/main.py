from fastapi import FastAPI

from core.db import create_db_and_tables
from api import auth, heroes



app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()



app.include_router(auth.router, tags=["auth"])
app.include_router(heroes.router, tags=["heroes"])
