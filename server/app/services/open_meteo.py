from typing import Dict, Any
from models import User, AreaAction
from sqlmodel import Session
from services.services_classes import Service, Action, Reaction, get_component
from services.area_api import AreaApi
from datetime import datetime


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
    
    def get_current_visibility(
        self, latitude: str, longitude: str, timezone: str = "auto"
    ) -> int:
        res = self.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": latitude,
                "longitude": longitude,
                "hourly": "visibility",
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

        return int(res["hourly"]["visibility"][time_index])
    
    def get_current_humidity(
        self, latitude: str, longitude: str, timezone: str = "auto"
    ) -> int:
        res = self.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": "relative_humidity_2m",
                "timezone": timezone,
            },
        )

        return int(res["current"]["relative_humidity_2m"])
    
    def get_current_wind_speed(
        self, latitude: str, longitude: str, timezone: str = "auto"
    ) -> float:
        res = self.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": "relative_wind_speed_10m",
                "timezone": timezone,
            },
        )

        return float(res["current"]["relative_wind_speed_10m"])

    def get_current_uv(
        self, latitude: str, longitude: str, timezone: str = "auto"
    ) -> float:
        res = self.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": latitude,
                "longitude": longitude,
                "daily": "uv_index_max",
                "forecast_days": 1,
                "timezone": timezone,
            },
        )

        time_list = res["daily"]["time"]
        time_objects = list(map(datetime.fromisoformat, time_list))
        current_time = datetime.now()

        time_index = time_objects.index(
            current_time.replace(hour=0, minute=0, second=0, microsecond=0)
        )

        return float(res["daily"]["uv_index_max"][time_index])
    

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
                    "name": "temperature_limit",
                    "type": "input",
                    "values": [],
                },
                *default_openmeteo_config_schema
            ]
            super().__init__(
                "Check if temperature rise above a certain limit",
                config_schema,
            )

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            temperature_limit = int(
                get_component(area_action.config, "temperature_limit", "values")
            )
            longitude = get_component(area_action.config, "longitude", "values")
            latitude = get_component(area_action.config, "latitude", "values")
            timezone = get_component(area_action.config, "timezone", "values")

            current_temperature = open_meteo_api.get_current_temperature(latitude, longitude, timezone)

            return current_temperature > temperature_limit

    class if_temperature_fall_bellow(Action):
        def __init__(self) -> None:
            config_schema = [
                {
                    "name": "temperature_limit",
                    "type": "input",
                    "values": [],
                },
                *default_openmeteo_config_schema
            ]
            super().__init__(
                "Check if temperature fall bellow a certain limit",
                config_schema,
            )

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            temperature_limit = int(
                get_component(area_action.config, "temperature_limit", "values")
            )
            longitude = get_component(area_action.config, "longitude", "values")
            latitude = get_component(area_action.config, "latitude", "values")
            timezone = get_component(area_action.config, "timezone", "values")

            current_temperature = open_meteo_api.get_current_temperature(latitude, longitude, timezone)

            return current_temperature < temperature_limit

    class if_visibility_fall_bellow(Action):
        def __init__(self) -> None:
            config_schema = [
                {
                    "name": "visibility_limit",
                    "type": "input",
                    "values": [],
                },
                *default_openmeteo_config_schema
            ]
            super().__init__(
                "Check if visibility fall bellow a certain limit",
                config_schema,
            )

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            visibility_limit = int(
                get_component(area_action.config, "visibility_limit", "values")
            )
            longitude = get_component(area_action.config, "longitude", "values")
            latitude = get_component(area_action.config, "latitude", "values")
            timezone = get_component(area_action.config, "timezone", "values")

            current_visibility = open_meteo_api.get_current_visibility(latitude, longitude, timezone)

            return current_visibility < visibility_limit
        
    class if_humidity_fall_bellow(Action):
        def __init__(self) -> None:
            config_schema = [
                {
                    "name": "humidity_limit",
                    "type": "input",
                    "values": [],
                },
                *default_openmeteo_config_schema
            ]
            super().__init__(
                "Check if humidity fall bellow a certain limit",
                config_schema,
            )

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            humidity_limit = int(
                get_component(area_action.config, "humidity_limit", "values")
            )
            longitude = get_component(area_action.config, "longitude", "values")
            latitude = get_component(area_action.config, "latitude", "values")
            timezone = get_component(area_action.config, "timezone", "values")

            current_humidity = open_meteo_api.get_current_humidity(latitude, longitude, timezone)

            return current_humidity < humidity_limit

    class if_humidity_rise_above(Action):
        def __init__(self) -> None:
            config_schema = [
                {
                    "name": "humidity_limit",
                    "type": "input",
                    "values": [],
                },
                *default_openmeteo_config_schema
            ]
            super().__init__(
                "Check if humidity rise above a certain limit",
                config_schema,
            )

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            humidity_limit = int(
                get_component(area_action.config, "humidity_limit", "values")
            )
            longitude = get_component(area_action.config, "longitude", "values")
            latitude = get_component(area_action.config, "latitude", "values")
            timezone = get_component(area_action.config, "timezone", "values")

            current_humidity = open_meteo_api.get_current_humidity(latitude, longitude, timezone)

            return current_humidity > humidity_limit
        
    class if_wind_speed_rise_above(Action):
        def __init__(self) -> None:
            config_schema = [
                {
                    "name": "wind_speed_limit",
                    "type": "input",
                    "values": [],
                },
                *default_openmeteo_config_schema
            ]
            super().__init__(
                "Check if wind speed rise above a certain limit",
                config_schema,
            )

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            wind_speed_limit = float(
                get_component(area_action.config, "wind_speed_limit", "values")
            )
            longitude = get_component(area_action.config, "longitude", "values")
            latitude = get_component(area_action.config, "latitude", "values")
            timezone = get_component(area_action.config, "timezone", "values")

            current_wind_speed = open_meteo_api.get_current_wind_speed(latitude, longitude, timezone)

            return current_wind_speed > wind_speed_limit
        
    class if_wind_speed_fall_bellow(Action):
        def __init__(self) -> None:
            config_schema = [
                {
                    "name": "wind_speed_limit",
                    "type": "input",
                    "values": [],
                },
                *default_openmeteo_config_schema
            ]
            super().__init__(
                "Check if wind speed fall bellow a certain limit",
                config_schema,
            )

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            wind_speed_limit = float(
                get_component(area_action.config, "wind_speed_limit", "values")
            )
            longitude = get_component(area_action.config, "longitude", "values")
            latitude = get_component(area_action.config, "latitude", "values")
            timezone = get_component(area_action.config, "timezone", "values")

            current_wind_speed = open_meteo_api.get_current_wind_speed(latitude, longitude, timezone)

            return current_wind_speed < wind_speed_limit
        
    class if_uv_index_rise_above(Action):
        def __init__(self) -> None:
            config_schema = [
                {
                    "name": "uv_index_limit",
                    "type": "input",
                    "values": [],
                },
                *default_openmeteo_config_schema
            ]
            super().__init__(
                "Check if uv index rise above a certain limit",
                config_schema,
            )

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            uv_index_limit = float(
                get_component(area_action.config, "uv_index_limit", "values")
            )
            longitude = get_component(area_action.config, "longitude", "values")
            latitude = get_component(area_action.config, "latitude", "values")
            timezone = get_component(area_action.config, "timezone", "values")

            current_wind_speed = open_meteo_api.get_current_wind_speed(latitude, longitude, timezone)

            return current_wind_speed > uv_index_limit
        
    def __init__(self) -> None:
        super().__init__("Service OpenMeteo", "Meteo", "#2596be", "", False)
