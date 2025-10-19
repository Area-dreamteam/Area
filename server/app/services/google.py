from typing import Dict, Any
from models import User, AreaAction
from sqlmodel import Session
from services.services_classes import Service, Action, Reaction, get_component

class Google(Service):
    class new_email(Action):
        def __init__(self) -> None:
            config_schema = [
                {"name": "from", "type": "input", "values": []},
                {"name": "subject", "type": "input", "values": []},
            ]
            super().__init__("Déclenché lorsqu'un nouvel email arrive.", config_schema)

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            print(
                f"Checking for new email from: {get_component(area_action.config, 'from', 'anyone')}, subject: {get_component(area_action.config, 'subject', 'any')}"
            )
            return True

    class send_email(Reaction):
        def __init__(self) -> None:
            config_schema = [
                {"name": "to", "type": "input", "values": []},
                {"name": "subject", "type": "input", "values": []},
                {"name": "body", "type": "input", "values": []},
            ]
            super().__init__("Permet d'envoyer un email.", config_schema)

        def execute(self, session: Session, area_action: AreaAction, user_id: int):
            print(f"Sending email to: {area_action.config.get('to')}")
            print(f"Subject: {area_action.config.get('subject')}")
            print(f"Body: {area_action.config.get('body')}")

    def __init__(self) -> None:
        super().__init__("Service email de Google", "mail", "#000000", "", True)
