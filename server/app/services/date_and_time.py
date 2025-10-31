from models import AreaAction
from sqlmodel import Session
from services.services_classes import Service, Action, get_component
from datetime import datetime


class DateAndTime(Service):
    class every_hour_at(Action):
        def __init__(self) -> None:
            config_schema = [
                {
                    "name": "Select interval",
                    "type": "select",
                    "values": ["00", "15", "30", "45"],
                },
            ]
            super().__init__(
                "Déclenché une fois par heure à :00, :15, :30 ou :45 minutes après l'heure.",
                config_schema,
                "* * * * *",
            )

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            current_time = datetime.now()
            selected_minute: int = int(
                get_component(area_action.config, "Select interval", "values")
            )
            if selected_minute == current_time.minute:
                return True
            return False

    class reaction_debug(Reaction):
        from models import AreaReaction
        def __init__(self) -> None:
            config_schema = []
            super().__init__(
                "Reacion debug.",
                config_schema,
            )

        def execute(self, session: Session, area_action: AreaReaction, user_id: int):
            logger.debug("Reaction debug")
            pass

    def __init__(self) -> None:
        super().__init__(
            "Service Date&Time",
            "Time",
            "#4a4d4b",
            "/images/DateAndTime_logo.webp",
            False,
        )
