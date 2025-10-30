from typing import Dict, Any
from models import User, AreaAction
from sqlmodel import Session
from services.services_classes import Service, Action, Reaction, get_component
from services.area_api import AreaApi
from datetime import datetime
from core.logger import logger


class OpenMeteoApiError(Exception):
    """OpenMeteo API-specific errors."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class OpenMeteoApi(AreaApi):
    def __init__(self):
        super().__init__(OpenMeteoApiError)

    def get_current_temperature(
        self, latitude: str, longitude: str, timezone: str = "auto"
    ) -> int:
        res = self.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": latitude,
                "longitude": longitude,
                "hourly": "temperature_2m",
                "forecast_days": 1,
                "timezone": timezone,
            },
        )

        time_list = res["hourly"]["time"]
        time_objects = list(map(datetime.fromisoformat, time_list))
        current_time = datetime.now()

        time_index = time_objects.index(
            current_time.replace(minute=0, second=0, microsecond=0)
        )

        return int(res["hourly"]["temperature_2m"][time_index])


open_meteo_api = OpenMeteoApi()

default_openmeteo_config_schema = [
    {
        "name": "latitude",
        "type": "input",
        "values": [],
    },
    {
        "name": "longitude",
        "type": "input",
        "values": [],
    },
    {
        "name": "timezone",
        "type": "select",
        "values": [
            "auto",
            "GMT",
            "America/Anchorage",
            "America/Los_Angeles",
            "America/Denver",
            "America/Chicago",
            "America/New_York",
            "America/Sao_Paulo",
            "Europe/London",
            "Europe/Berlin",
            "Europe/Moscow",
            "Africa/Cairo",
            "Asia/Bangkok",
            "Asia/Singapore",
            "Asia/Tokyo",
            "Australia/Sydney",
            "Pacific/Auckland",
        ],
    },
]


class OpenMeteo(Service):
    class if_temperature_rise_above(Action):
        def __init__(self) -> None:
            config_schema = [
                {
                    "name": "temperature_limite",
                    "type": "input",
                    "values": [],
                },
                *default_openmeteo_config_schema
            ]
            super().__init__(
                "Vérifie si la temperature est supérieure a une limite",
                config_schema,
            )

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            temperature_limite = int(
                get_component(area_action.config, "temperature_limite", "values")
            )
            longitude = get_component(area_action.config, "longitude", "values")
            latitude = get_component(area_action.config, "latitude", "values")
            timezone = get_component(area_action.config, "timezone", "values")

            current_temperature = int(
                open_meteo_api.get_current_temperature(latitude, longitude, timezone)
            )

            return current_temperature > temperature_limite
    
    class if_temperature_drop_bellow(Action):
        def __init__(self) -> None:
            config_schema = [
                {
                    "name": "temperature_limite",
                    "type": "input",
                    "values": [],
                },
                *default_openmeteo_config_schema
            ]
            super().__init__(
                "Vérifie si la temperature est inferieure a une limite",
                config_schema,
            )

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            temperature_limite = int(
                get_component(area_action.config, "temperature_limite", "values")
            )
            longitude = get_component(area_action.config, "longitude", "values")
            latitude = get_component(area_action.config, "latitude", "values")
            timezone = get_component(area_action.config, "timezone", "values")

            current_temperature = int(
                open_meteo_api.get_current_temperature(latitude, longitude, timezone)
            )

            return current_temperature < temperature_limite

    def __init__(self) -> None:
        super().__init__("Service OpenMeteo", "Meteo", "#2596be", "", False)
