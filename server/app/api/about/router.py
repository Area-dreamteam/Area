from fastapi import APIRouter, Request
from sqlmodel import select
from models import Service, Action, Reaction
from dependencies.db import SessionDep
from datetime import datetime

router = APIRouter(tags=["about"])

@router.get(
    "/about.json",
    summary="Get application info",
    description="Returns client/server info and available services for mobile app"
)
def get_about(request: Request, session: SessionDep):
    host = request.headers.get("host", "localhost:8080")
    services = session.exec(select(Service)).all()

    services_data = []
    for service in services:
        actions = session.exec(select(Action).where(Action.service_id == service.id)).all()
        actions_data = []
        for action in actions:
            actions_data.append(
                {
                    "name": action.name,
                    "description": action.description or ""
                }
            )

        reactions = session.exec(select(Reaction).where(Reaction.service_id == service.id)).all()
        reactions_data = []
        for reaction in reactions:
            reactions_data.append(
                {
                    "name": reaction.name,
                    "description": reaction.description or ""
                }
            )

        services_data.append({
            "name": service.name,
            "description": service.description or "",
            "actions": actions_data,
            "reactions": reactions_data
        })

    return {
        "client": {
            "host": host
        },
        "server": {
            "current_time": int(datetime.now().timestamp()),
            "services": services_data
        }
    }
