"""Base classes for service architecture.

Defines the core service system with automatic action/reaction discovery,
OAuth integration, and JSON serialization for API and database operations.
"""

from typing import Dict, Optional, Any, Union
from core.logger import logger
from models import User, AreaAction, AreaReaction
from sqlmodel import Session
from fastapi import Response, Request


class Action:
    """Base class for automation triggers.

    Actions are periodic checks that can trigger reactions when conditions are met.
    Each action defines a cron interval and configuration schema.
    """

    def __init__(
        self,
        description: str,
        config_schema: list[Dict[str, Any]] = None,
        interval: str = "* * * * *",
    ) -> None:
        self.name: str = self.__class__.__name__
        self.description: str = description
        self.interval: str = interval  # Cron expression
        self.config_schema: list[Dict[str, Any]] = (
            config_schema if config_schema is not None else []
        )
        self.service: Service = None

    def check(self, session: Session, area_action: AreaAction, user_id: int) -> bool:
        """Check if action condition is met. Override in subclasses."""
        pass

    def to_dict(self) -> Dict[str, Any]:
        """Convert action to dictionary representation."""
        return {
            "name": self.name,
            "description": self.description,
            "interval": self.interval,
            "config_schema": self.config_schema,
        }


class Reaction:
    """Base class for automation responses.

    Reactions are executed when their paired action triggers.
    Each reaction defines a configuration schema for user customization.
    """

    def __init__(
        self, description: str, config_schema: list[Dict[str, Any]] = None
    ) -> None:
        self.name: str = self.__class__.__name__
        self.description: str = description
        self.config_schema: list[Dict[str, Any]] = (
            config_schema if config_schema is not None else []
        )
        self.service: Service = None

    def execute(self, session: Session, area_action: AreaReaction, user_id: int):
        """Execute reaction with user configuration. Override in subclasses."""
        pass

    def to_dict(self) -> Dict[str, Any]:
        """Convert reaction to dictionary representation."""
        return {
            "name": self.name,
            "description": self.description,
            "config_schema": self.config_schema,
        }


class Service:
    """Base class for external service integrations.

    Services automatically discover their nested Action/Reaction classes
    and provide OAuth integration, API management, and JSON serialization.
    """

    def __init__(
        self,
        description: str,
        category: str,
        color: str = "#000000",
        img_url: str = "",
        oauth: bool = False,
    ) -> None:
        self.name: str = self.__class__.__name__
        self.description: str = description
        self.color: str = color  # UI theme color
        self.image_url: str = img_url
        self.category: str = category
        self.oauth: bool = oauth
        self.actions: Dict[str, Action] = {}  # Auto-populated
        self.reactions: Dict[str, Reaction] = {}  # Auto-populated
        self._auto_register()

    def _auto_register(self):
        """Automatically register all Action and Reaction subclasses as nested classes."""
        for attr_name in dir(self.__class__):
            attr = getattr(self.__class__, attr_name)
            if isinstance(attr, type):
                if issubclass(attr, Action) and attr is not Action:
                    instance = attr()
                    instance.service = self
                    self.actions[instance.name] = instance
                elif issubclass(attr, Reaction) and attr is not Reaction:
                    instance = attr()
                    instance.service = self
                    self.reactions[instance.name] = instance

    def check(
        self, action_name: str, session: Session, area_action: AreaAction, user_id: int
    ) -> bool:
        """Search for an action by name and execute check with parameters."""
        action = self.actions.get(action_name)
        if action:
            return action.check(session, area_action, user_id)
        logger.error(f"Action '{action_name}' not found in {self.name}")
        return False

    def execute(
        self,
        reaction_name: str,
        session: Session,
        area_reaction: AreaReaction,
        user_id: int,
    ) -> Optional[Reaction]:
        """Search for a reaction by name and execute it with parameters."""
        reaction = self.reactions.get(reaction_name)
        if reaction:
            reaction.execute(session, area_reaction, user_id)
            return reaction
        logger.error(f"Reaction '{reaction_name}' not found in {self.name}")
        return None

    def get_actions_dict(self) -> Dict[str, Dict[str, Any]]:
        """Build a dictionary with all actions and their details."""
        return [action.to_dict() for action in self.actions.values()]

    def get_reactions_dict(self) -> Dict[str, Dict[str, Any]]:
        """Build a dictionary with all reactions and their details."""
        return [reaction.to_dict() for reaction in self.reactions.values()]

    def to_dict(self) -> Dict[str, Any]:
        """Convert the entire service to a dictionary representation."""
        return {
            "name": self.name,
            "description": self.description,
            "color": self.color,
            "image_url": self.image_url,
            "category": self.category,
            "actions": self.get_actions_dict(),
            "reactions": self.get_reactions_dict(),
            "oauth_required": self.oauth,
        }

    def is_connected(self, session: Session, user_id: int) -> bool:
        """Check if service is connected for current user."""
        return False

    def oauth_link(self, state: str = None) -> str:
        """Generate OAuth authorization URL.
        
        Args:
            state: Optional OAuth state token for mobile flows
        """
        return ""

    def oauth_callback(
        self,
        session: Session,
        code: str,
        user: User | None,
        request: Request = None,
        is_mobile: bool = False,
    ) -> Response:
        pass


class oauth_service:
    """Base class for OAuth-only services (login without automation).

    Simplified service class for services that only provide OAuth login
    functionality without actions/reactions.
    """

    def __init__(self, color: str = "#000000", img_url: str = "") -> None:
        self.name: str = self.__class__.__name__
        self.color: str = color
        self.image_url: str = img_url

    def oauth_link(self, state: str = None) -> str:
        """Generate OAuth authorization URL.
        
        Args:
            state: Optional OAuth state token for mobile flows
        """
        return ""

    def oauth_callback(
        self,
        session: Session,
        code: str,
        user: User | None,
        request: Request = None,
        is_mobile: bool = False,
    ) -> Response:
        """Handle OAuth callback for login flow."""
        pass

    def to_dict(self) -> Dict[str, Any]:
        """Convert the entire service to a dictionary representation."""
        return {
            "name": self.name,
            "color": self.color,
            "image_url": self.image_url,
        }


def create_service_dictionnary(
    service_type: type,
) -> Dict[str, Union[Service, oauth_service]]:
    """Auto-discover and instantiate all service subclasses.

    Recursively finds all subclasses of the given service type
    and creates a registry dictionary for service discovery.
    """
    logger.info(f"Type class: {service_type.__name__}")
    service_dict = {}

    def get_all_subclasses(cls):
        """Recursively collect all subclasses."""
        all_subclasses = []
        for subclass in cls.__subclasses__():
            all_subclasses.append(subclass)
            all_subclasses.extend(get_all_subclasses(subclass))
        return all_subclasses

    for service_class in get_all_subclasses(service_type):
        instance = service_class()
        logger.info(instance.name)
        service_dict[instance.name] = instance

    return service_dict


def get_component(config: list, name: str, key: str):
    for comp in config:
        if comp.get("name") == name:
            if key:
                return comp.get(key, None)
            return comp
    return None
