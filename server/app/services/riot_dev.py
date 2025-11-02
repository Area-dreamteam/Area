from models import AreaAction
from sqlmodel import Session
from services.services_classes import Service, Action, get_component
from services.area_api import AreaApi
from core.categories import ServiceCategory
from core.logger import logger


class RiotDevApiError(Exception):
    """RiotDev API-specific errors."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class RiotDevApi(AreaApi):
    def __init__(self):
        super().__init__(RiotDevApiError)
        
    def get_puuid(self, api_key: str, game_name: str, tag_line: str):
        res = self.get(
            f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}",
            params={
                "api_key": api_key
            },
        )
        
        return res["puuid"]
    
    def _get_last_match_id(self, api_key: str, puuid: str):
        res = self.get(
            f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids",
            params={
                "api_key": api_key
            },
        )
        
        return res[0] if res else None

    def _get_match_info(self, api_key: str, match_id: str):
        res = self.get(
            f"https://europe.api.riotgames.com/lol/match/v5/matches/{match_id}",
            params={
                "api_key": api_key
            },
        )
        
        return res
    
    def _get_last_match_info_complete(self, api_key: str, game_name: str, tag_line: str):
        player_puuid = self.get_puuid(api_key, game_name, tag_line)
        
        last_match_id = self._get_last_match_id(api_key, player_puuid)
        if last_match_id is None:
            return None
        
        return self._get_match_info(api_key, last_match_id)
    
    def get_last_match_info(self, api_key: str, game_name: str, tag_line: str) -> tuple[str, str] | None:
        player_puuid = self.get_puuid(api_key, game_name, tag_line)
        match_info = self._get_last_match_info_complete(api_key, game_name, tag_line)
        
        if match_info is None:
            return None
        
        match_id = match_info["info"]["gameId"]
        player_index = match_info["metadata"]["participants"].index(player_puuid)

        return match_id, match_info["info"]["participants"][player_index]["win"]



riot_dev_api = RiotDevApi()

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


class RiotDev(Service):
    def __init__(self) -> None:
        super().__init__(
            "Service RiotDev", ServiceCategory.WEATHER, "#000000", "images/RiotDev_logo.png", False
        )

    class win_game(Action):
        def __init__(self) -> None:
            config_schema = [
                {
                    "name": "dev_api_key",
                    "type": "input",
                    "values": [],
                },
                {
                    "name": "player_game_name",
                    "type": "input",
                    "values": [],
                },
                {
                    "name": "player_tag_line",
                    "type": "input",
                    "values": [],
                },
            ]
            super().__init__(
                "Trigger if last game was win",
                config_schema,
            )

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            dev_api_key = get_component(area_action.config, "dev_api_key", "values")
            player_game_name = get_component(area_action.config, "player_game_name", "values")
            player_tag_line = get_component(area_action.config, "player_tag_line", "values")
            last_state = area_action.last_state

            match_info = riot_dev_api.get_last_match_info(dev_api_key, player_game_name, player_tag_line)
            if match_info is None:
                return False

            match_id, is_win = match_info
            
            if (
                last_state is None
                or "last_game_id" not in last_state
                or last_state["last_game_id"] != match_id
            ):
                area_action.last_state = {"last_game_id": match_id}
                session.add(area_action)
                session.commit()
                return is_win

            return False

    class lose_game(Action):
        def __init__(self) -> None:
            config_schema = [
                {
                    "name": "dev_api_key",
                    "type": "input",
                    "values": [],
                },
                {
                    "name": "player_game_name",
                    "type": "input",
                    "values": [],
                },
                {
                    "name": "player_tag_line",
                    "type": "input",
                    "values": [],
                },
            ]
            super().__init__(
                "Trigger if last game was lose",
                config_schema,
            )

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            dev_api_key = get_component(area_action.config, "dev_api_key", "values")
            player_game_name = get_component(area_action.config, "player_game_name", "values")
            player_tag_line = get_component(area_action.config, "player_tag_line", "values")
            last_state = area_action.last_state

            match_info = riot_dev_api.get_last_match_info(dev_api_key, player_game_name, player_tag_line)
            if match_info is None:
                return False

            match_id, is_win = match_info
            
            if (
                last_state is None
                or "last_game_id" not in last_state
                or last_state["last_game_id"] != match_id
            ):
                area_action.last_state = {"last_game_id": match_id}
                session.add(area_action)
                session.commit()
                return not is_win

            return False

    class new_game(Action):
        def __init__(self) -> None:
            config_schema = [
                {
                    "name": "dev_api_key",
                    "type": "input",
                    "values": [],
                },
                {
                    "name": "player_game_name",
                    "type": "input",
                    "values": [],
                },
                {
                    "name": "player_tag_line",
                    "type": "input",
                    "values": [],
                },
            ]
            super().__init__(
                "Trigger if a new game was played",
                config_schema,
            )

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            dev_api_key = get_component(area_action.config, "dev_api_key", "values")
            player_game_name = get_component(area_action.config, "player_game_name", "values")
            player_tag_line = get_component(area_action.config, "player_tag_line", "values")
            last_state = area_action.last_state

            match_info = riot_dev_api.get_last_match_info(dev_api_key, player_game_name, player_tag_line)
            if match_info is None:
                return False

            match_id, _ = match_info
            
            if (
                last_state is None
                or "last_game_id" not in last_state
                or last_state["last_game_id"] != match_id
            ):
                area_action.last_state = {"last_game_id": match_id}
                session.add(area_action)
                session.commit()
                return True

            return False
