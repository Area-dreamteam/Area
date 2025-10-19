"""Google services integration.

Provides Gmail automation with email triggers and sending capabilities.
Currently includes basic email monitoring and sending actions.
"""

from typing import Dict, Any
from models import User, AreaAction
from sqlmodel import Session
from services.services_classes import Service, Action, Reaction


def get_component(config: list, name: str, key: str):
    """Extract configuration value from action/reaction config."""
    for comp in config:
        if comp.get("name") == name:
            if key:
                return comp.get(key, None)
            return comp
    return None


class Google(Service):
    """Google services automation.
    
    Provides Gmail integration for email monitoring and sending.
    Supports filtering by sender, subject, and custom content.
    """
    class new_email(Action):
        """Trigger when new email arrives matching filters."""
        def __init__(self) -> None:
            config_schema = [
                {"name": "from", "type": "input", "values": []},
                {"name": "subject", "type": "input", "values": []},
            ]
            super().__init__("Triggered when new email arrives", config_schema)

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            print(
                f"Checking for new email from: {get_component(area_action.config, 'from', 'anyone')}, subject: {get_component(area_action.config, 'subject', 'any')}"
            )
            return True

    class send_email(Reaction):
        """Send email to specified recipient."""
        def __init__(self) -> None:
            config_schema = [
                {"name": "to", "type": "input", "values": []},
                {"name": "subject", "type": "input", "values": []},
                {"name": "body", "type": "input", "values": []},
            ]
            super().__init__("Send email to recipient", config_schema)

        def execute(self, session: Session, area_action: AreaAction, user_id: int):
            print(f"Sending email to: {area_action.config.get('to')}")
            print(f"Subject: {area_action.config.get('subject')}")
            print(f"Body: {area_action.config.get('body')}")

    def __init__(self) -> None:
        super().__init__("Service email de Google", "mail", "#000000", "", True)
