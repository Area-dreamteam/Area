from urllib.parse import urlencode
from fastapi import HTTPException, Request, Response
import requests
from typing import Dict, Any, List
from sqlmodel import Session, select
from pydantic import BaseModel

from models.services.service import Service
from models.users.user import User
from models.users.user_service import UserService
from services.oauth_lib import oauth_add_link
from core.config import settings
from core.logger import logger
from core.categories import ServiceCategory
from services.services_classes import (
    Service as ServiceClass,
    Action,
    Reaction,
    get_component,
)
from models import AreaAction, AreaReaction


class DiscordApiError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class DiscordOAuthTokenRes(BaseModel):
    """Discord OAuth2 token response."""

    access_token: str
    token_type: str
    refresh_token: str
    expires_in: int
    scope: str


class Discord(ServiceClass):
    def __init__(self) -> None:
        super().__init__(
            description=f"Discord Bot for server and channel automation. Invite the bot after connecting: [here]({self.get_bot_invite_link()})",
            category=ServiceCategory.COMMUNICATION,
            color="#5865F2",
            img_url="images/Discord_logo.webp",
            oauth=True,
        )

    class new_message_in_channel(Action):
        def __init__(self):
            config_schema = [
                {"name": "Channel ID", "type": "input", "values": []},
                {"name": "Keyword Filter", "type": "input", "values": []},
            ]
            super().__init__(
                "Triggered when a new message is posted in a channel (optional keyword filter)",
                config_schema,
                "*/1 * * * *",
            )

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            try:
                channel_id = get_component(area_action.config, "Channel ID", "values")
                keyword = get_component(area_action.config, "Keyword Filter", "values")

                messages = self.service._get_channel_messages(channel_id, limit=10)

                if not messages:
                    return False

                message_ids = {msg["id"] for msg in messages}
                previous_ids = set(
                    area_action.last_state.get("message_ids", [])
                    if area_action.last_state
                    else []
                )

                if (
                    not area_action.last_state
                    or "message_ids" not in area_action.last_state
                ):
                    area_action.last_state = {"message_ids": list(message_ids)}
                    session.add(area_action)
                    session.commit()
                    return False

                new_ids = message_ids - previous_ids
                area_action.last_state = {"message_ids": list(message_ids)}
                session.add(area_action)
                session.commit()

                if not new_ids:
                    return False

                if keyword and keyword.strip():
                    for msg in messages:
                        if (
                            msg["id"] in new_ids
                            and keyword.lower() in msg.get("content", "").lower()
                        ):
                            return True
                    return False

                return len(new_ids) > 0

            except DiscordApiError as e:
                logger.error(f"{self.service.name}: {e.message}")
                return False

    class user_joined_server(Action):
        def __init__(self):
            config_schema = []
            super().__init__(
                "Triggered when a new user joins the Discord server",
                config_schema,
                "*/5 * * * *",
            )

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            try:
                guild_id = self.service.get_user_guild_id(session, user_id)
                if not guild_id:
                    return False
                guild_info = self.service._get_guild(guild_id)

                current_count = guild_info.get("approximate_member_count", 0)
                previous_count = (
                    area_action.last_state.get("member_count", 0)
                    if area_action.last_state
                    else 0
                )

                if (
                    not area_action.last_state
                    or "member_count" not in area_action.last_state
                ):
                    area_action.last_state = {"member_count": current_count}
                    session.add(area_action)
                    session.commit()
                    return False

                area_action.last_state = {"member_count": current_count}
                session.add(area_action)
                session.commit()

                return current_count > previous_count

            except DiscordApiError as e:
                logger.error(f"{self.service.name}: {e.message}")
                return False

    class message_contains_keyword(Action):
        def __init__(self):
            config_schema = [
                {"name": "Channel ID", "type": "input", "values": []},
                {"name": "Keywords", "type": "input", "values": []},
            ]
            super().__init__(
                "Triggered when a message contains specific keywords (comma-separated)",
                config_schema,
                "*/1 * * * *",
            )

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            try:
                channel_id = get_component(area_action.config, "Channel ID", "values")
                keywords_str = get_component(area_action.config, "Keywords", "values")

                if not keywords_str:
                    return False

                keywords = [k.strip().lower() for k in keywords_str.split(",")]
                messages = self.service._get_channel_messages(channel_id, limit=10)

                if not messages:
                    return False

                message_ids = {msg["id"] for msg in messages}
                previous_ids = set(
                    area_action.last_state.get("message_ids", [])
                    if area_action.last_state
                    else []
                )

                if (
                    not area_action.last_state
                    or "message_ids" not in area_action.last_state
                ):
                    area_action.last_state = {"message_ids": list(message_ids)}
                    session.add(area_action)
                    session.commit()
                    return False

                new_ids = message_ids - previous_ids
                area_action.last_state = {"message_ids": list(message_ids)}
                session.add(area_action)
                session.commit()

                for msg in messages:
                    if msg["id"] in new_ids:
                        content = msg.get("content", "").lower()
                        for keyword in keywords:
                            if keyword in content:
                                return True

                return False

            except DiscordApiError as e:
                logger.error(f"{self.service.name}: {e.message}")
                return False

    class channel_created(Action):
        def __init__(self):
            config_schema = []
            super().__init__(
                "Triggered when a new channel is created in the server",
                config_schema,
                "*/5 * * * *",
            )

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            try:
                guild_id = self.service.get_user_guild_id(session, user_id)
                if not guild_id:
                    return False
                channels = self.service._get_guild_channels(guild_id)

                channel_ids = {ch["id"] for ch in channels}
                previous_ids = set(
                    area_action.last_state.get("channel_ids", [])
                    if area_action.last_state
                    else []
                )

                if (
                    not area_action.last_state
                    or "channel_ids" not in area_action.last_state
                ):
                    area_action.last_state = {"channel_ids": list(channel_ids)}
                    session.add(area_action)
                    session.commit()
                    return False

                area_action.last_state = {"channel_ids": list(channel_ids)}
                session.add(area_action)
                session.commit()

                new_channels = channel_ids - previous_ids
                return len(new_channels) > 0

            except DiscordApiError as e:
                logger.error(f"{self.service.name}: {e.message}")
                return False

    class user_mentioned(Action):
        def __init__(self):
            config_schema = [
                {"name": "Channel ID", "type": "input", "values": []},
                {"name": "User ID", "type": "input", "values": []},
            ]
            super().__init__(
                "Triggered when a specific user is mentioned in a channel",
                config_schema,
                "*/2 * * * *",
            )

        def check(
            self, session: Session, area_action: AreaAction, user_id: int
        ) -> bool:
            try:
                channel_id = get_component(area_action.config, "Channel ID", "values")
                target_user_id = get_component(area_action.config, "User ID", "values")

                messages = self.service._get_channel_messages(channel_id, limit=10)

                if not messages:
                    return False

                message_ids = {msg["id"] for msg in messages}
                previous_ids = set(
                    area_action.last_state.get("message_ids", [])
                    if area_action.last_state
                    else []
                )

                if (
                    not area_action.last_state
                    or "message_ids" not in area_action.last_state
                ):
                    area_action.last_state = {"message_ids": list(message_ids)}
                    session.add(area_action)
                    session.commit()
                    return False

                new_ids = message_ids - previous_ids
                area_action.last_state = {"message_ids": list(message_ids)}
                session.add(area_action)
                session.commit()

                for msg in messages:
                    if msg["id"] in new_ids:
                        mentions = msg.get("mentions", [])
                        for mention in mentions:
                            if str(mention.get("id")) == str(target_user_id):
                                return True

                return False

            except DiscordApiError as e:
                logger.error(f"{self.service.name}: {e.message}")
                return False

    class send_message_to_channel(Reaction):
        def __init__(self):
            config_schema = [
                {"name": "Channel ID", "type": "input", "values": []},
                {"name": "Message Content", "type": "input", "values": []},
            ]
            super().__init__("Send a message to a Discord channel", config_schema)

        def execute(self, session: Session, area_action: AreaReaction, user_id: int):
            try:
                channel_id = get_component(area_action.config, "Channel ID", "values")
                content = get_component(
                    area_action.config,
                    "Message Content",
                    "values",
                )

                self.service._send_message(channel_id, content)
                logger.info(f"Discord: Sent message to channel {channel_id}")

            except DiscordApiError as e:
                logger.error(f"{self.service.name}: {e.message}")

    class create_channel(Reaction):
        def __init__(self):
            config_schema = [
                {"name": "Channel Name", "type": "input", "values": []},
                {
                    "name": "Channel Type",
                    "type": "select",
                    "values": ["text", "voice", "announcement"],
                },
            ]
            super().__init__("Create a new channel in a Discord server", config_schema)

        def execute(self, session: Session, area_action: AreaReaction, user_id: int):
            try:
                guild_id = self.service.get_user_guild_id(session, user_id)
                if not guild_id:
                    logger.error("Discord: No guild linked for user")
                    return
                name = get_component(area_action.config, "Channel Name", "values")
                channel_type = get_component(
                    area_action.config,
                    "Channel Type",
                    "values",
                )

                type_map = {"text": 0, "voice": 2, "announcement": 5}
                type_int = type_map.get(channel_type, 0)

                self.service._create_channel(guild_id, name, type_int)
                logger.info(f"Discord: Created channel '{name}' in guild {guild_id}")

            except DiscordApiError as e:
                logger.error(f"{self.service.name}: {e.message}")

    class add_role_to_user(Reaction):
        def __init__(self):
            config_schema = [
                {"name": "User ID", "type": "input", "values": []},
                {"name": "Role ID", "type": "input", "values": []},
            ]
            super().__init__("Add a role to a user in a Discord server", config_schema)

        def execute(self, session: Session, area_action: AreaReaction, user_id: int):
            try:
                guild_id = self.service.get_user_guild_id(session, user_id)
                if not guild_id:
                    logger.error("Discord: No guild linked for user")
                    return
                target_user_id = get_component(
                    area_action.config,
                    "User ID",
                    "values",
                )
                role_id = get_component(area_action.config, "Role ID", "values")

                self.service._add_role_to_member(guild_id, target_user_id, role_id)
                logger.info(f"Discord: Added role {role_id} to user {target_user_id}")

            except DiscordApiError as e:
                logger.error(f"{self.service.name}: {e.message}")

    class add_reaction_to_message(Reaction):
        def __init__(self):
            config_schema = [
                {"name": "Channel ID", "type": "input", "values": []},
                {"name": "Message ID", "type": "input", "values": []},
                {"name": "Emoji", "type": "input", "values": []},
            ]
            super().__init__(
                "Add a reaction emoji to a message (use unicode emoji like 👍 or custom emoji ID)",
                config_schema,
            )

        def execute(self, session: Session, area_action: AreaReaction, user_id: int):
            try:
                channel_id = get_component(area_action.config, "Channel ID", "values")
                message_id = get_component(area_action.config, "Message ID", "values")
                emoji = get_component(area_action.config, "Emoji", "values")

                self.service._add_reaction(channel_id, message_id, emoji)
                logger.info(f"Discord: Added reaction {emoji} to message {message_id}")

            except DiscordApiError as e:
                logger.error(f"{self.service.name}: {e.message}")

    class delete_message(Reaction):
        def __init__(self):
            config_schema = [
                {"name": "Channel ID", "type": "input", "values": []},
                {"name": "Message ID", "type": "input", "values": []},
            ]
            super().__init__("Delete a message from a channel", config_schema)

        def execute(self, session: Session, area_action: AreaReaction, user_id: int):
            try:
                channel_id = get_component(area_action.config, "Channel ID", "values")
                message_id = get_component(area_action.config, "Message ID", "values")

                self.service._delete_message(channel_id, message_id)
                logger.info(
                    f"Discord: Deleted message {message_id} from channel {channel_id}"
                )

            except DiscordApiError as e:
                logger.error(f"{self.service.name}: {e.message}")

    class send_embed_message(Reaction):
        def __init__(self):
            config_schema = [
                {"name": "Channel ID", "type": "input", "values": []},
                {"name": "Embed Title", "type": "input", "values": []},
                {"name": "Embed Description", "type": "input", "values": []},
                {"name": "Embed Color", "type": "input", "values": []},
            ]
            super().__init__(
                "Send a rich embed message to a channel (color in hex like 5865F2)",
                config_schema,
            )

        def execute(self, session: Session, area_action: AreaReaction, user_id: int):
            try:
                channel_id = get_component(area_action.config, "Channel ID", "values")
                title = get_component(area_action.config, "Embed Title", "values")
                description = get_component(
                    area_action.config,
                    "Embed Description",
                    "values",
                )
                color_hex = get_component(area_action.config, "Embed Color", "values")

                try:
                    color = (
                        int(color_hex.replace("#", ""), 16) if color_hex else 5865714
                    )
                except (ValueError, AttributeError):
                    color = 5865714

                self.service._send_embed_message(channel_id, title, description, color)
                logger.info(f"Discord: Sent embed message to channel {channel_id}")

            except DiscordApiError as e:
                logger.error(f"{self.service.name}: {e.message}")

    def _get_bot_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bot {settings.DISCORD_BOT_TOKEN}",
            "Content-Type": "application/json",
        }

    def _make_bot_request(
        self,
        endpoint: str,
        method: str = "GET",
        data: Dict[str, Any] | None = None,
    ) -> Any:
        url = f"https://discord.com/api/v10{endpoint}"
        headers = self._get_bot_headers()

        try:
            if method == "GET":
                r = requests.get(url, headers=headers, timeout=10)
            elif method == "POST":
                r = requests.post(url, headers=headers, json=data, timeout=10)
            elif method == "PUT":
                r = requests.put(url, headers=headers, json=data, timeout=10)
            elif method == "PATCH":
                r = requests.patch(url, headers=headers, json=data, timeout=10)
            elif method == "DELETE":
                r = requests.delete(url, headers=headers, timeout=10)
            else:
                raise DiscordApiError(f"Unsupported HTTP method: {method}")

            if r.status_code == 429:
                retry_after = r.json().get("retry_after", 5)
                raise DiscordApiError(f"Rate limited. Retry after {retry_after}s")

            if r.status_code == 204:
                return {}

            if r.status_code not in [200, 201, 204]:
                error_msg = r.text if r.text else f"Status code: {r.status_code}"
                raise DiscordApiError(f"Discord API error: {error_msg}")

            return r.json() if r.text else {}

        except requests.RequestException as e:
            raise DiscordApiError(f"Request failed: {str(e)}")

    def _get_channel_messages(
        self, channel_id: str, limit: int = 100
    ) -> List[Dict[str, Any]]:
        return self._make_bot_request(f"/channels/{channel_id}/messages?limit={limit}")

    def _send_message(self, channel_id: str, content: str) -> Dict[str, Any]:
        data = {"content": content}
        return self._make_bot_request(f"/channels/{channel_id}/messages", "POST", data)

    def _send_embed_message(
        self, channel_id: str, title: str, description: str, color: int
    ) -> Dict[str, Any]:
        data = {
            "embeds": [{"title": title, "description": description, "color": color}]
        }
        return self._make_bot_request(f"/channels/{channel_id}/messages", "POST", data)

    def _get_guild(self, guild_id: str) -> Dict[str, Any]:
        return self._make_bot_request(f"/guilds/{guild_id}?with_counts=true")

    def _get_guild_channels(self, guild_id: str) -> List[Dict[str, Any]]:
        return self._make_bot_request(f"/guilds/{guild_id}/channels")

    def _create_channel(
        self, guild_id: str, name: str, channel_type: int
    ) -> Dict[str, Any]:
        data = {"name": name, "type": channel_type}
        return self._make_bot_request(f"/guilds/{guild_id}/channels", "POST", data)

    def _add_role_to_member(
        self, guild_id: str, user_id: str, role_id: str
    ) -> Dict[str, Any]:
        return self._make_bot_request(
            f"/guilds/{guild_id}/members/{user_id}/roles/{role_id}", "PUT"
        )

    def _add_reaction(
        self, channel_id: str, message_id: str, emoji: str
    ) -> Dict[str, Any]:
        from urllib.parse import quote

        emoji_encoded = quote(emoji)
        return self._make_bot_request(
            f"/channels/{channel_id}/messages/{message_id}/reactions/{emoji_encoded}/@me",
            "PUT",
        )

    def _delete_message(self, channel_id: str, message_id: str) -> Dict[str, Any]:
        return self._make_bot_request(
            f"/channels/{channel_id}/messages/{message_id}", "DELETE"
        )

    def _get_token(self, code: str) -> DiscordOAuthTokenRes:
        """Exchange authorization code for access token."""
        url = "https://discord.com/api/v10/oauth2/token"
        redirect_uri = f"{settings.FRONT_URL}/callbacks/link/{self.name}"

        data = {
            "client_id": settings.DISCORD_CLIENT_ID,
            "client_secret": settings.DISCORD_CLIENT_SECRET,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
        }

        try:
            r = requests.post(url, data=data, timeout=10)
            if r.status_code != 200:
                error_msg = r.text if r.text else f"Status code: {r.status_code}"
                raise DiscordApiError(f"Token exchange failed: {error_msg}")

            token_data = r.json()
            return DiscordOAuthTokenRes(**token_data)
        except requests.RequestException as e:
            raise DiscordApiError(f"Token request failed: {str(e)}")

    def _get_user_headers(self, session: Session, user_id: int) -> Dict[str, str]:
        """Get headers with user's OAuth token."""
        user_service = session.exec(
            select(UserService)
            .join(Service)
            .where(
                UserService.user_id == user_id,
                Service.name == self.name,
            )
        ).first()

        if not user_service or not user_service.access_token:
            raise DiscordApiError("User not connected to Discord")

        return {
            "Authorization": f"Bearer {user_service.access_token}",
            "Content-Type": "application/json",
        }

    def _refresh_token(self, session: Session, user_id: int) -> bool:
        """Refresh user's OAuth token."""
        user_service = session.exec(
            select(UserService)
            .join(Service)
            .where(
                UserService.user_id == user_id,
                Service.name == self.name,
            )
        ).first()

        if not user_service or not user_service.refresh_token:
            return False

        url = "https://discord.com/api/v10/oauth2/token"
        data = {
            "client_id": settings.DISCORD_CLIENT_ID,
            "client_secret": settings.DISCORD_CLIENT_SECRET,
            "grant_type": "refresh_token",
            "refresh_token": user_service.refresh_token,
        }

        try:
            r = requests.post(url, data=data, timeout=10)
            if r.status_code != 200:
                logger.error(f"Token refresh failed: {r.text}")
                return False

            token_data = r.json()
            user_service.access_token = token_data["access_token"]
            user_service.refresh_token = token_data.get(
                "refresh_token", user_service.refresh_token
            )
            session.add(user_service)
            session.commit()
            logger.info(f"Refreshed Discord token for user {user_id}")
            return True
        except Exception as e:
            logger.error(f"Token refresh failed: {str(e)}")
            return False

    def is_connected(self, session: Session, user_id: int) -> bool:
        """Check if user has a valid OAuth token and bot has access to at least one mutual guild."""
        user_service = session.exec(
            select(UserService)
            .join(Service)
            .where(
                UserService.user_id == user_id,
                Service.name == self.name,
            )
        ).first()

        if not user_service or not user_service.access_token:
            return False

        metadata = (
            user_service.service_metadata if user_service.service_metadata else {}
        )
        guild_id = metadata.get("guild_id") if isinstance(metadata, dict) else None

        if guild_id:
            try:
                self._get_guild(guild_id)
                return True
            except DiscordApiError:
                current_metadata = user_service.service_metadata or {}
                if isinstance(current_metadata, dict):
                    new_metadata = {**current_metadata}
                    new_metadata.pop("guild_id", None)
                    user_service.service_metadata = new_metadata
                    session.add(user_service)
                    session.commit()

        available_guilds = self.get_available_guilds(
            session, user_id, filter_bot_present=True
        )

        if available_guilds:
            first_guild_id = available_guilds[0]["id"]
            self.set_guild_id(session, user_id, first_guild_id)
            return True

        return False

    def get_bot_invite_link(self, guild_id: str | None = None) -> str:
        base_url = "https://discord.com/oauth2/authorize"
        params = {
            "client_id": settings.DISCORD_CLIENT_ID,
            "permissions": "268527616",
            "scope": "bot",
        }
        if guild_id:
            params["guild_id"] = guild_id
        return f"{base_url}?{urlencode(params)}"

    def oauth_link(self, state: str = "") -> str:
        """Generate Discord OAuth URL to get user's guilds."""
        base_url = "https://discord.com/oauth2/authorize"
        redirect_uri = f"{settings.FRONT_URL}/callbacks/link/{self.name}"
        params = {
            "client_id": settings.DISCORD_CLIENT_ID,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": "identify guilds",
            "state": state,
        }
        return f"{base_url}?{urlencode(params)}"

    def oauth_callback(
        self,
        session: Session,
        code: str,
        user: User | None,
        request: Request | None = None,
        is_mobile: bool = False,
    ) -> Response:
        """Handle Discord OAuth callback and exchange code for tokens."""
        if not user:
            raise HTTPException(status_code=400, detail="User must be authenticated")

        try:
            token_response = self._get_token(code)

            user_service = session.exec(
                select(UserService)
                .join(Service)
                .where(
                    UserService.user_id == user.id,
                    Service.name == self.name,
                )
            ).first()

            if user_service:
                user_service.access_token = token_response.access_token
                user_service.refresh_token = token_response.refresh_token
                session.add(user_service)
                session.commit()
            else:
                response = oauth_add_link(
                    session,
                    self.name,
                    user,
                    token_response.access_token,
                    request,
                    is_mobile,
                )

                user_service = session.exec(
                    select(UserService)
                    .join(Service)
                    .where(
                        UserService.user_id == user.id,
                        Service.name == self.name,
                    )
                ).first()

                if user_service:
                    user_service.refresh_token = token_response.refresh_token
                    session.add(user_service)
                    session.commit()

                return response

            return oauth_add_link(
                session,
                self.name,
                user,
                token_response.access_token,
                request,
                is_mobile,
            )

        except DiscordApiError as e:
            logger.error(f"Discord OAuth callback failed: {e.message}")
            raise HTTPException(status_code=400, detail=f"OAuth failed: {e.message}")

    def get_available_guilds(
        self, session: Session, user_id: int, filter_bot_present: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Get list of guilds the user has access to.

        Args:
            session: Database session
            user_id: User ID
            filter_bot_present: If True, only return guilds where the bot is present
        """
        try:
            headers = self._get_user_headers(session, user_id)

            url = "https://discord.com/api/v10/users/@me/guilds"
            r = requests.get(url, headers=headers, timeout=10)

            if r.status_code == 401:
                if self._refresh_token(session, user_id):
                    headers = self._get_user_headers(session, user_id)
                    r = requests.get(url, headers=headers, timeout=10)

            if r.status_code != 200:
                raise DiscordApiError(f"Failed to fetch guilds: {r.text}")

            user_guilds = r.json()

            if filter_bot_present:
                try:
                    bot_guilds_data = self._make_bot_request("/users/@me/guilds")
                    bot_guild_ids = {guild["id"] for guild in bot_guilds_data}

                    user_guilds = [
                        guild for guild in user_guilds if guild["id"] in bot_guild_ids
                    ]
                except DiscordApiError as e:
                    logger.error(f"Failed to fetch bot guilds: {e.message}")
                    return []

            return [
                {
                    "id": guild["id"],
                    "name": guild["name"],
                    "icon": f"https://cdn.discordapp.com/icons/{guild['id']}/{guild['icon']}.png"
                    if guild.get("icon")
                    else None,
                    "bot_present": True,
                }
                for guild in user_guilds
            ]
        except DiscordApiError as e:
            logger.error(f"Failed to fetch guilds: {e.message}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error fetching guilds: {str(e)}")
            return []

    def set_guild_id(self, session: Session, user_id: int, guild_id: str) -> bool:
        """Link a specific guild to the user's Discord service connection."""
        try:
            guild = self._get_guild(guild_id)
            if not guild:
                return False

            user_service = session.exec(
                select(UserService)
                .join(Service)
                .where(
                    UserService.user_id == user_id,
                    Service.name == self.name,
                )
            ).first()

            if not user_service:
                logger.error(
                    f"UserService not found for user {user_id}. User must authenticate first."
                )
                return False

            current_metadata = (
                user_service.service_metadata if user_service.service_metadata else {}
            )
            if isinstance(current_metadata, dict):
                new_metadata = {**current_metadata, "guild_id": guild_id}
            else:
                new_metadata = {"guild_id": guild_id}

            user_service.service_metadata = new_metadata
            session.add(user_service)
            session.commit()

            logger.info(f"Linked guild {guild_id} to user {user_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to set guild_id: {str(e)}")
            return False

    def get_user_guild_id(self, session: Session, user_id: int) -> str | None:
        """Get the guild_id associated with this user."""
        user_service = session.exec(
            select(UserService)
            .join(Service)
            .where(
                UserService.user_id == user_id,
                Service.name == self.name,
            )
        ).first()

        if not user_service:
            return None

        metadata = (
            user_service.service_metadata if user_service.service_metadata else {}
        )
        if isinstance(metadata, dict):
            return metadata.get("guild_id")

        return None
