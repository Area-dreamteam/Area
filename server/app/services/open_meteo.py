from models import AreaAction
from sqlmodel import Session
from services.services_classes import Service, Action, get_component
from services.area_api import AreaApi
from core.categories import ServiceCategory
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

    def get_current_uv_index(
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

    def get_current_cloud_cover(
        self, latitude: str, longitude: str, timezone: str = "auto"
    ) -> float:
        res = self.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": "cloud_cover",
                "forecast_days": 1,
                "timezone": timezone,
            },
        )

        return float(res["current"]["cloud_cover"])

    def get_current_air_quality(
        self, latitude: str, longitude: str, timezone: str = "auto"
    ) -> int:
        res = self.get(
            "https://air-quality-api.open-meteo.com/v1/air-quality",
            params={
                "latitude": latitude,
                "longitude": longitude,
                "hourly": "european_aqi",
                "timezone": timezone,
            },
        )

        time_list = res["hourly"]["time"]
        time_objects = list(map(datetime.fromisoformat, time_list))
        current_time = datetime.now()

        time_index = time_objects.index(
            current_time.replace(minute=0, second=0, microsecond=0)
        )

        return int(res["hourly"]["european_aqi"][time_index])


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
    def __init__(self) -> None:
        super().__init__(
            "Service OpenMeteo", ServiceCategory.WEATHER, "#2596be", "", False
        )

    class if_temperature_rise_above(Action):
        def __init__(self) -> None:
            config_schema = [
                {
                    "name": "temperature_limit",
                    "type": "input",
                    "values": [],
                },
                *default_openmeteo_config_schema,
            ]
            super().__init__(
                "Check if temperature rise above a certain limit",
                config_schema,
            )

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            try:
                temperature_limit = int(
                    get_component(area_action.config, "temperature_limit", "values")
                )
            except ValueError as e:
                logger.error(f"Error in parameter conversion: {e}")
                return False
                
            longitude = get_component(area_action.config, "longitude", "values")
            latitude = get_component(area_action.config, "latitude", "values")
            timezone = get_component(area_action.config, "timezone", "values")

            current_temperature = open_meteo_api.get_current_temperature(
                latitude, longitude, timezone
            )

            return current_temperature > temperature_limit

    class if_temperature_fall_bellow(Action):
        def __init__(self) -> None:
            config_schema = [
                {
                    "name": "temperature_limit",
                    "type": "input",
                    "values": [],
                },
                *default_openmeteo_config_schema,
            ]
            super().__init__(
                "Check if temperature fall bellow a certain limit",
                config_schema,
            )

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            try:
                temperature_limit = int(
                    get_component(area_action.config, "temperature_limit", "values")
                )
            except ValueError as e:
                logger.error(f"Error in parameter conversion: {e}")
                return False
            
            longitude = get_component(area_action.config, "longitude", "values")
            latitude = get_component(area_action.config, "latitude", "values")
            timezone = get_component(area_action.config, "timezone", "values")

            current_temperature = open_meteo_api.get_current_temperature(
                latitude, longitude, timezone
            )

            return current_temperature < temperature_limit

    class if_visibility_fall_bellow(Action):
        def __init__(self) -> None:
            config_schema = [
                {
                    "name": "visibility_limit",
                    "type": "input",
                    "values": [],
                },
                *default_openmeteo_config_schema,
            ]
            super().__init__(
                "Check if visibility fall bellow a certain limit",
                config_schema,
            )

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            try:
                visibility_limit = int(
                    get_component(area_action.config, "visibility_limit", "values")
                )
            except ValueError as e:
                logger.error(f"Error in parameter conversion: {e}")
                return False
            
            longitude = get_component(area_action.config, "longitude", "values")
            latitude = get_component(area_action.config, "latitude", "values")
            timezone = get_component(area_action.config, "timezone", "values")

            current_visibility = open_meteo_api.get_current_visibility(
                latitude, longitude, timezone
            )

            return current_visibility < visibility_limit

    class if_humidity_fall_bellow(Action):
        def __init__(self) -> None:
            config_schema = [
                {
                    "name": "humidity_limit",
                    "type": "input",
                    "values": [],
                },
                *default_openmeteo_config_schema,
            ]
            super().__init__(
                "Check if humidity fall bellow a certain limit",
                config_schema,
            )

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            try:
                humidity_limit = int(
                    get_component(area_action.config, "humidity_limit", "values")
                )
            except ValueError as e:
                logger.error(f"Error in parameter conversion: {e}")
                return False
            
            longitude = get_component(area_action.config, "longitude", "values")
            latitude = get_component(area_action.config, "latitude", "values")
            timezone = get_component(area_action.config, "timezone", "values")

            current_humidity = open_meteo_api.get_current_humidity(
                latitude, longitude, timezone
            )

            return current_humidity < humidity_limit

    class if_humidity_rise_above(Action):
        def __init__(self) -> None:
            config_schema = [
                {
                    "name": "humidity_limit",
                    "type": "input",
                    "values": [],
                },
                *default_openmeteo_config_schema,
            ]
            super().__init__(
                "Check if humidity rise above a certain limit",
                config_schema,
            )

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            try:
                humidity_limit = int(
                    get_component(area_action.config, "humidity_limit", "values")
                )
            except ValueError as e:
                logger.error(f"Error in parameter conversion: {e}")
                return False
            
            longitude = get_component(area_action.config, "longitude", "values")
            latitude = get_component(area_action.config, "latitude", "values")
            timezone = get_component(area_action.config, "timezone", "values")

            current_humidity = open_meteo_api.get_current_humidity(
                latitude, longitude, timezone
            )

            return current_humidity > humidity_limit

    class if_wind_speed_rise_above(Action):
        def __init__(self) -> None:
            config_schema = [
                {
                    "name": "wind_speed_limit",
                    "type": "input",
                    "values": [],
                },
                *default_openmeteo_config_schema,
            ]
            super().__init__(
                "Check if wind speed rise above a certain limit",
                config_schema,
            )

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            try:
                wind_speed_limit = float(
                    get_component(area_action.config, "wind_speed_limit", "values")
                )
            except ValueError as e:
                logger.error(f"Error in parameter conversion: {e}")
                return False
            
            longitude = get_component(area_action.config, "longitude", "values")
            latitude = get_component(area_action.config, "latitude", "values")
            timezone = get_component(area_action.config, "timezone", "values")

            current_wind_speed = open_meteo_api.get_current_wind_speed(
                latitude, longitude, timezone
            )

            return current_wind_speed > wind_speed_limit

    class if_wind_speed_fall_bellow(Action):
        def __init__(self) -> None:
            config_schema = [
                {
                    "name": "wind_speed_limit",
                    "type": "input",
                    "values": [],
                },
                *default_openmeteo_config_schema,
            ]
            super().__init__(
                "Check if wind speed fall bellow a certain limit",
                config_schema,
            )

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            try:
                wind_speed_limit = float(
                    get_component(area_action.config, "wind_speed_limit", "values")
                )
            except ValueError as e:
                logger.error(f"Error in parameter conversion: {e}")
                return False
            
            longitude = get_component(area_action.config, "longitude", "values")
            latitude = get_component(area_action.config, "latitude", "values")
            timezone = get_component(area_action.config, "timezone", "values")

            current_wind_speed = open_meteo_api.get_current_wind_speed(
                latitude, longitude, timezone
            )

            return current_wind_speed < wind_speed_limit

    class if_uv_index_rise_above(Action):
        def __init__(self) -> None:
            config_schema = [
                {
                    "name": "uv_index_limit",
                    "type": "input",
                    "values": [],
                },
                *default_openmeteo_config_schema,
            ]
            super().__init__(
                "Check if uv index rise above a certain limit",
                config_schema,
            )

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            try:
                uv_index_limit = float(
                    get_component(area_action.config, "uv_index_limit", "values")
                )
            except ValueError as e:
                logger.error(f"Error in parameter conversion: {e}")
                return False
                
            longitude = get_component(area_action.config, "longitude", "values")
            latitude = get_component(area_action.config, "latitude", "values")
            timezone = get_component(area_action.config, "timezone", "values")

            current_uv_index = open_meteo_api.get_current_uv_index(
                latitude, longitude, timezone
            )

            return current_uv_index > uv_index_limit

    class if_uv_index_fall_bellow(Action):
        def __init__(self) -> None:
            config_schema = [
                {
                    "name": "uv_index_limit",
                    "type": "input",
                    "values": [],
                },
                *default_openmeteo_config_schema,
            ]
            super().__init__(
                "Check if uv index fall bellow a certain limit",
                config_schema,
            )

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            try:
                uv_index_limit = float(
                    get_component(area_action.config, "uv_index_limit", "values")
                )
            except ValueError as e:
                logger.error(f"Error in parameter conversion: {e}")
                return False
            
            longitude = get_component(area_action.config, "longitude", "values")
            latitude = get_component(area_action.config, "latitude", "values")
            timezone = get_component(area_action.config, "timezone", "values")

            current_uv_index = open_meteo_api.get_current_uv_index(
                latitude, longitude, timezone
            )

            return current_uv_index < uv_index_limit

    class if_cloud_cover_fall_bellow(Action):
        def __init__(self) -> None:
            config_schema = [
                {
                    "name": "cloud_cover_limit",
                    "type": "input",
                    "values": [],
                },
                *default_openmeteo_config_schema,
            ]
            super().__init__(
                "Check if cloud cover fall bellow a certain limit",
                config_schema,
            )

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            try:
                cloud_cover_limit = float(
                    get_component(area_action.config, "cloud_cover_limit", "values")
                )
            except ValueError as e:
                logger.error(f"Error in parameter conversion: {e}")
                return False
            
            longitude = get_component(area_action.config, "longitude", "values")
            latitude = get_component(area_action.config, "latitude", "values")
            timezone = get_component(area_action.config, "timezone", "values")

            current_cloud_cover = open_meteo_api.get_current_cloud_cover(
                latitude, longitude, timezone
            )

            return current_cloud_cover < cloud_cover_limit

    class if_cloud_cover_rise_above(Action):
        def __init__(self) -> None:
            config_schema = [
                {
                    "name": "cloud_cover_limit",
                    "type": "input",
                    "values": [],
                },
                *default_openmeteo_config_schema,
            ]
            super().__init__(
                "Check if cloud cover rise above a certain limit",
                config_schema,
            )

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            try:
                cloud_cover_limit = float(
                    get_component(area_action.config, "cloud_cover_limit", "values")
                )
            except ValueError as e:
                logger.error(f"Error in parameter conversion: {e}")
                return False
            
            longitude = get_component(area_action.config, "longitude", "values")
            latitude = get_component(area_action.config, "latitude", "values")
            timezone = get_component(area_action.config, "timezone", "values")

            current_cloud_cover = open_meteo_api.get_current_cloud_cover(
                latitude, longitude, timezone
            )

            return current_cloud_cover > cloud_cover_limit

    class check_air_quality(Action):
        air_quality_level = [
            ("Good", 20),
            ("Fair", 40),
            ("Moderate", 60),
            ("Poor", 80),
            ("Very Poor", 100),
        ]

        def __init__(self) -> None:
            config_schema = [
                {
                    "name": "alert_level",
                    "type": "select",
                    "values": ["Good", "Fair", "Moderate", "Poor", "Very Poor"],
                },
                *default_openmeteo_config_schema,
            ]
            super().__init__(
                "Check air quality attain or exceed an alert level",
                config_schema,
            )

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            air_quality_alert = get_component(area_action.config, "alert_level", "values")
            
            longitude = get_component(area_action.config, "longitude", "values")
            latitude = get_component(area_action.config, "latitude", "values")
            timezone = get_component(area_action.config, "timezone", "values")

            aqi = open_meteo_api.get_current_air_quality(latitude, longitude, timezone)

            aqi_alert_level = next(
                (
                    air_quality_threshold
                    for air_quality_tag, air_quality_threshold in self.air_quality_level
                    if air_quality_tag == air_quality_alert
                ),
                100,
            )

            return aqi >= aqi_alert_level
