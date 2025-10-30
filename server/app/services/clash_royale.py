"""Clash Royale service integration.
Uses RoyaleAPI proxy (https://proxy.royaleapi.dev) for API access.
Requires Clash Royale API key with IP whitelist: 45.79.218.79
"""

from typing import Dict, Any, Optional, cast, List
from urllib.parse import quote
from services.services_classes import (
    Service as ServiceClass,
    Action,
    get_component,
)
from models.areas import AreaAction
from core.config import settings
from sqlmodel import Session
from pydantic import BaseModel
import requests
from core.logger import logger


class ClashRoyaleApiError(Exception):
    """Clash Royale API-specific errors."""

    def __init__(self, message: str, status_code: Optional[int] = None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class Battle(BaseModel):
    """Battle information from battlelog."""

    battleTime: str
    type: str
    isLadderTournament: Optional[bool] = None
    arena: Optional[Dict[str, Any]] = None
    gameMode: Optional[Dict[str, Any]] = None
    team: Optional[list] = None
    opponent: Optional[list] = None


class BattleResult(BaseModel):
    """Battle result with victory/defeat information."""

    battleTime: str
    type: str
    team: list
    opponent: list
    is_victory: bool
    crowns_won: int = 0
    crowns_lost: int = 0


class PlayerInfo(BaseModel):
    """Player profile information."""

    tag: str
    name: str
    expLevel: int
    trophies: int
    bestTrophies: int
    wins: int
    losses: int
    battleCount: int
    threeCrownWins: int


class ClashRoyale(ServiceClass):
    """Clash Royale automation service.

    Comprehensive battle tracking and player monitoring:
    - Battle outcomes (victories, defeats, three crowns)
    - Trophy changes (gains, losses, thresholds)
    - Win streak tracking
    - Player statistics

    Uses JWT Bearer token authentication via shared API key.
    """

    def __init__(self) -> None:
        super().__init__(
            "Track player statistics and battle logs from Clash Royale",
            "Gaming",
            "#09304D",
            "/images/ClashRoyale_logo.png",
        )

    class new_battle(Action):
        """Trigger when a new battle is recorded in player's battlelog."""

        def __init__(self) -> None:
            config_schema = [
                {
                    "name": "player_tag",
                    "type": "input",
                    "values": [],
                }
            ]
            super().__init__(
                "Triggers when a new battle appears in player's battlelog",
                config_schema,
                interval="*/5 * * * *",
            )

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            logger.debug("Clashroyal action trigger")
            service = cast("ClashRoyale", self.service)

            player_tag = get_component(
                cast(List, area_action.config), "player_tag", "values"
            )
            if not player_tag:
                logger.error("Player tag not configured")
                return False

            try:
                battles = service._get_player_battlelog(str(player_tag))

                if not battles:
                    return False

                latest_battle = battles[0]

                last_state = area_action.last_state
                if last_state is None or "last_battle_time" not in last_state:
                    area_action.last_state = {
                        "last_battle_time": latest_battle.battleTime
                    }
                    session.add(area_action)
                    session.commit()
                    return True

                last_battle_time_str = last_state.get("last_battle_time", "")
                if latest_battle.battleTime != last_battle_time_str:
                    area_action.last_state = {
                        "last_battle_time": latest_battle.battleTime
                    }
                    session.add(area_action)
                    session.commit()
                    return True

                return False

            except ClashRoyaleApiError as e:
                logger.error(f"Error checking battles: {e.message}")
                return False

    class battle_victory(Action):
        """Trigger when player wins a battle."""

        def __init__(self) -> None:
            config_schema = [
                {
                    "name": "player_tag",
                    "type": "input",
                    "values": [],
                }
            ]
            super().__init__(
                "Triggers when player wins a battle",
                config_schema,
                interval="*/5 * * * *",
            )

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            service = cast("ClashRoyale", self.service)

            player_tag = get_component(
                cast(List, area_action.config), "player_tag", "values"
            )
            if not player_tag:
                logger.error("Player tag not configured")
                return False

            try:
                battle_result = service._get_latest_battle_result(str(player_tag))

                if not battle_result:
                    return False

                last_state = area_action.last_state
                if last_state is None or "last_battle_time" not in last_state:
                    area_action.last_state = {
                        "last_battle_time": battle_result.battleTime
                    }
                    session.add(area_action)
                    session.commit()
                    return battle_result.is_victory

                last_battle_time_str = last_state.get("last_battle_time", "")
                if battle_result.battleTime != last_battle_time_str:
                    area_action.last_state = {
                        "last_battle_time": battle_result.battleTime
                    }
                    session.add(area_action)
                    session.commit()
                    return battle_result.is_victory

                return False

            except ClashRoyaleApiError as e:
                logger.error(f"Error checking battle victory: {e.message}")
                return False

    class battle_defeat(Action):
        """Trigger when player loses a battle."""

        def __init__(self) -> None:
            config_schema = [
                {
                    "name": "player_tag",
                    "type": "input",
                    "values": [],
                }
            ]
            super().__init__(
                "Triggers when player loses a battle",
                config_schema,
                interval="*/5 * * * *",
            )

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            service = cast("ClashRoyale", self.service)

            player_tag = get_component(
                cast(List, area_action.config), "player_tag", "values"
            )
            if not player_tag:
                logger.error("Player tag not configured")
                return False

            try:
                battle_result = service._get_latest_battle_result(str(player_tag))

                if not battle_result:
                    return False

                last_state = area_action.last_state
                if last_state is None or "last_battle_time" not in last_state:
                    area_action.last_state = {
                        "last_battle_time": battle_result.battleTime
                    }
                    session.add(area_action)
                    session.commit()
                    return not battle_result.is_victory

                last_battle_time_str = last_state.get("last_battle_time", "")
                if battle_result.battleTime != last_battle_time_str:
                    area_action.last_state = {
                        "last_battle_time": battle_result.battleTime
                    }
                    session.add(area_action)
                    session.commit()
                    return not battle_result.is_victory

                return False

            except ClashRoyaleApiError as e:
                logger.error(f"Error checking battle defeat: {e.message}")
                return False

    class three_crown_win(Action):
        """Trigger when player achieves a three crown victory."""

        def __init__(self) -> None:
            config_schema = [
                {
                    "name": "player_tag",
                    "type": "input",
                    "values": [],
                }
            ]
            super().__init__(
                "Triggers when player wins with three crowns",
                config_schema,
                interval="*/5 * * * *",
            )

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            service = cast("ClashRoyale", self.service)

            player_tag = get_component(
                cast(List, area_action.config), "player_tag", "values"
            )
            if not player_tag:
                logger.error("Player tag not configured")
                return False

            try:
                battle_result = service._get_latest_battle_result(str(player_tag))

                if not battle_result:
                    return False

                last_state = area_action.last_state
                if last_state is None or "last_battle_time" not in last_state:
                    area_action.last_state = {
                        "last_battle_time": battle_result.battleTime
                    }
                    session.add(area_action)
                    session.commit()
                    return battle_result.is_victory and battle_result.crowns_won == 3

                last_battle_time_str = last_state.get("last_battle_time", "")
                if battle_result.battleTime != last_battle_time_str:
                    area_action.last_state = {
                        "last_battle_time": battle_result.battleTime
                    }
                    session.add(area_action)
                    session.commit()
                    return battle_result.is_victory and battle_result.crowns_won == 3

                return False

            except ClashRoyaleApiError as e:
                logger.error(f"Error checking three crown win: {e.message}")
                return False

    class win_streak(Action):
        """Trigger when player reaches a win streak threshold."""

        def __init__(self) -> None:
            config_schema = [
                {"name": "player_tag", "type": "input", "values": []},
                {"name": "streak_count", "type": "input", "values": []},
            ]
            super().__init__(
                "Triggers when player reaches a specified win streak",
                config_schema,
                interval="*/5 * * * *",
            )

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            service = cast("ClashRoyale", self.service)

            player_tag = get_component(
                cast(List, area_action.config), "player_tag", "values"
            )
            streak_threshold = get_component(
                cast(List, area_action.config), "streak_count", "values"
            )

            if not player_tag or not streak_threshold:
                logger.error("Player tag or streak count not configured")
                return False

            try:
                threshold = int(streak_threshold)
                battles = service._get_player_battlelog(str(player_tag))

                if not battles:
                    return False

                current_streak = service._calculate_win_streak(battles)

                last_state = area_action.last_state
                previous_streak = last_state.get("win_streak", 0) if last_state else 0

                area_action.last_state = {"win_streak": current_streak}
                session.add(area_action)
                session.commit()

                return current_streak >= threshold and previous_streak < threshold

            except (ValueError, ClashRoyaleApiError) as e:
                logger.error(f"Error checking win streak: {e}")
                return False

    class trophy_gain(Action):
        """Trigger when player gains trophies above threshold."""

        def __init__(self) -> None:
            config_schema = [
                {"name": "player_tag", "type": "input", "values": []},
                {"name": "trophy_gain_threshold", "type": "input", "values": []},
            ]
            super().__init__(
                "Triggers when player gains more trophies than threshold",
                config_schema,
                interval="*/10 * * * *",
            )

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            service = cast("ClashRoyale", self.service)

            player_tag = get_component(
                cast(List, area_action.config), "player_tag", "values"
            )
            trophy_gain_threshold = get_component(
                cast(List, area_action.config), "trophy_gain_threshold", "values"
            )

            if not player_tag or not trophy_gain_threshold:
                logger.error("Player tag or trophy gain threshold not configured")
                return False

            try:
                threshold = int(trophy_gain_threshold)
                player_info = service._get_player_info(str(player_tag))

                last_state = area_action.last_state
                if last_state is None or "last_trophy_count" not in last_state:
                    area_action.last_state = {"last_trophy_count": player_info.trophies}
                    session.add(area_action)
                    session.commit()
                    return False

                last_trophy_count = last_state.get("last_trophy_count", 0)
                trophy_gain = player_info.trophies - last_trophy_count

                area_action.last_state = {"last_trophy_count": player_info.trophies}
                session.add(area_action)
                session.commit()

                return trophy_gain >= threshold

            except (ValueError, ClashRoyaleApiError) as e:
                logger.error(f"Error checking trophy gain: {e}")
                return False

    class trophy_loss(Action):
        """Trigger when player loses trophies below threshold."""

        def __init__(self) -> None:
            config_schema = [
                {"name": "player_tag", "type": "input", "values": []},
                {"name": "trophy_loss_threshold", "type": "input", "values": []},
            ]
            super().__init__(
                "Triggers when player loses more trophies than threshold",
                config_schema,
                interval="*/10 * * * *",
            )

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            service = cast("ClashRoyale", self.service)

            player_tag = get_component(
                cast(List, area_action.config), "player_tag", "values"
            )
            trophy_loss_threshold = get_component(
                cast(List, area_action.config), "trophy_loss_threshold", "values"
            )

            if not player_tag or not trophy_loss_threshold:
                logger.error("Player tag or trophy loss threshold not configured")
                return False

            try:
                threshold = int(trophy_loss_threshold)
                player_info = service._get_player_info(str(player_tag))

                last_state = area_action.last_state
                if last_state is None or "last_trophy_count" not in last_state:
                    area_action.last_state = {"last_trophy_count": player_info.trophies}
                    session.add(area_action)
                    session.commit()
                    return False

                last_trophy_count = last_state.get("last_trophy_count", 0)
                trophy_loss = last_trophy_count - player_info.trophies

                area_action.last_state = {"last_trophy_count": player_info.trophies}
                session.add(area_action)
                session.commit()

                return trophy_loss >= threshold

            except (ValueError, ClashRoyaleApiError) as e:
                logger.error(f"Error checking trophy loss: {e}")
                return False

    class trophy_threshold(Action):
        """Trigger when player reaches a trophy threshold."""

        def __init__(self) -> None:
            config_schema = [
                {"name": "player_tag", "type": "input", "values": []},
                {"name": "trophy_count", "type": "input", "values": []},
            ]
            super().__init__(
                "Triggers when player reaches a specific trophy count",
                config_schema,
                interval="*/10 * * * *",
            )

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            service = cast("ClashRoyale", self.service)

            player_tag = get_component(
                cast(List, area_action.config), "player_tag", "values"
            )
            trophy_threshold = get_component(
                cast(List, area_action.config), "trophy_count", "values"
            )

            if not player_tag or not trophy_threshold:
                logger.error("Player tag or trophy count not configured")
                return False

            try:
                threshold = int(trophy_threshold)
                player_info = service._get_player_info(str(player_tag))
                return player_info.trophies >= threshold

            except (ValueError, ClashRoyaleApiError) as e:
                logger.error(f"Error checking trophy threshold: {e}")
                return False

    def _format_player_tag(self, tag: str) -> str:
        """Format player tag for API requests.

        Tags must start with # and be URL encoded as %23
        """
        tag = tag.strip()
        if not tag.startswith("#"):
            tag = f"#{tag}"
        return quote(tag, safe="")

    def _api_request(self, endpoint: str) -> Dict[str, Any]:
        """Make authenticated API request via RoyaleAPI proxy using shared API key."""
        base_url = "https://proxy.royaleapi.dev/v1"
        headers = {
            "Authorization": f"Bearer {settings.CLASHROYALE_API_KEY}",
            "Accept": "application/json",
        }

        try:
            response = requests.get(
                f"{base_url}{endpoint}", headers=headers, timeout=10
            )

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 400:
                raise ClashRoyaleApiError(
                    "Invalid request parameters", response.status_code
                )
            elif response.status_code == 403:
                raise ClashRoyaleApiError("Invalid API token", response.status_code)
            elif response.status_code == 404:
                raise ClashRoyaleApiError("Player not found", response.status_code)
            elif response.status_code == 429:
                raise ClashRoyaleApiError("Rate limit exceeded", response.status_code)
            elif response.status_code == 503:
                raise ClashRoyaleApiError(
                    "Service temporarily unavailable", response.status_code
                )
            else:
                raise ClashRoyaleApiError(
                    f"API error: {response.status_code}", response.status_code
                )

        except requests.RequestException as e:
            raise ClashRoyaleApiError(f"Network error: {str(e)}")

    def _get_player_info(self, player_tag: str) -> PlayerInfo:
        """Get player profile information."""
        formatted_tag = self._format_player_tag(player_tag)
        data = self._api_request(f"/players/{formatted_tag}")
        return PlayerInfo(**data)

    def _get_player_battlelog(self, player_tag: str) -> list[Battle]:
        """Get player's recent battles."""
        formatted_tag = self._format_player_tag(player_tag)
        data = self._api_request(f"/players/{formatted_tag}/battlelog")

        battle_list = []
        if isinstance(data, list):
            battles_data = data
        elif isinstance(data, dict) and "items" in data:
            battles_data = data["items"]
        else:
            return battle_list

        for battle_data in battles_data:
            try:
                if isinstance(battle_data, dict):
                    battle_list.append(Battle(**battle_data))
            except Exception as e:
                logger.warning(f"Failed to parse battle data: {e}")
                continue

        return battle_list

    def _is_token_valid(self) -> bool:
        """Check if the shared API key is valid."""
        try:
            test_tag = "%232PP"
            self._api_request(f"/players/{test_tag}")
            return True
        except ClashRoyaleApiError:
            return False

    def _get_latest_battle_result(self, player_tag: str) -> Optional[BattleResult]:
        """Get the latest battle result with victory/defeat status."""
        battles = self._get_player_battlelog(player_tag)

        if not battles:
            return None

        latest_battle = battles[0]

        if not latest_battle.team or not latest_battle.opponent:
            return None

        player_team = latest_battle.team[0]
        opponent_team = latest_battle.opponent[0]

        player_crowns = player_team.get("crowns", 0)
        opponent_crowns = opponent_team.get("crowns", 0)

        is_victory = player_crowns > opponent_crowns

        return BattleResult(
            battleTime=latest_battle.battleTime,
            type=latest_battle.type,
            team=latest_battle.team,
            opponent=latest_battle.opponent,
            is_victory=is_victory,
            crowns_won=player_crowns,
            crowns_lost=opponent_crowns,
        )

    def _calculate_win_streak(self, battles: list[Battle]) -> int:
        """Calculate current win streak from recent battles."""
        win_streak = 0

        for battle in battles:
            if not battle.team or not battle.opponent:
                continue

            player_team = battle.team[0]
            opponent_team = battle.opponent[0]

            player_crowns = player_team.get("crowns", 0)
            opponent_crowns = opponent_team.get("crowns", 0)

            if player_crowns > opponent_crowns:
                win_streak += 1
            else:
                break

        return win_streak

    def is_connected(self, session: Session, user_id: int) -> bool:
        """Check if service API key is configured and valid.

        Note: Clash Royale uses a shared API key, not per-user OAuth tokens.
        """
        if not settings.CLASHROYALE_API_KEY:
            return False

        return self._is_token_valid()
