from typing import Dict, Any
from models import User, AreaAction
from sqlmodel import Session
from services.services_classes import Service, Action, Reaction, get_component
from datetime import datetime
from core.logger import logger


class DateAndTime(Service):
    class every_hour_at(Action):
        def __init__(self) -> None:
            config_schema = [
                {
                    "name": "select_interval",
                    "type": "select",
                    "values": ["00", "15", "30", "45"],
                },
            ]
            super().__init__(
                "Déclenché une fois par heure à :00, :15, :30 ou :45 minutes après l'heure.",
                config_schema,
            )

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            current_time = datetime.now()
            selected_minute: int = int(
                get_component(area_action.config, "select_interval", "values")
            )
            return True
            # if selected_minute == current_time.minute:
            #     return True
            # return False

    def __init__(self) -> None:
        super().__init__(
            "Service Date&Time", "Time", "#4a4d4b", "/images/Time_logo.png", False
        )
