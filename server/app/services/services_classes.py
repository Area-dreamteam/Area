import json
from typing import Dict, Optional, Any, Union
from core.logger import logger
from models import User, AreaAction, AreaReaction
from sqlmodel import Session
from fastapi import Response


class Action:
    def __init__(
        self,
        description: str,
        config_schema: list[Dict[str, Any]] = None,
        interval: str = "* * * * *",
    ) -> None:
        self.name: str = self.__class__.__name__
        self.description: str = description
        self.interval: str = interval
        self.config_schema: list[Dict[str, Any]] = (
            config_schema if config_schema is not None else []
        )

    def check(self, session: Session, area_action: AreaAction, user_id: int) -> bool:
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
    def __init__(
        self, description: str, config_schema: list[Dict[str, Any]] = None
    ) -> None:
        self.name: str = self.__class__.__name__
        self.description: str = description
        self.config_schema: list[Dict[str, Any]] = (
            config_schema if config_schema is not None else []
        )

    def execute(self, session: Session, area_action: AreaReaction, user_id: int):
        pass

    def to_dict(self) -> Dict[str, Any]:
        """Convert reaction to dictionary representation."""
        return {
            "name": self.name,
            "description": self.description,
            "config_schema": self.config_schema,
        }


class Service:
    def __init__(
        self,
        description: str,
        category: str,
        color: str = "#000000",
        img_url: str = "",
        oauth: str = False,
    ) -> None:
        self.name: str = self.__class__.__name__
        self.description: str = description
        self.color: str = color
        self.image_url: str = img_url
        self.category: str = category
        self.oauth: bool = oauth
        self.actions: Dict[str, Action] = {}
        self.reactions: Dict[str, Reaction] = {}
        self._auto_register()

    def _auto_register(self):
        """Automatically register all Action and Reaction subclasses as nested classes."""
        for attr_name in dir(self.__class__):
            attr = getattr(self.__class__, attr_name)
            if isinstance(attr, type):
                if issubclass(attr, Action) and attr is not Action:
                    instance = attr()
                    self.actions[instance.name] = instance
                elif issubclass(attr, Reaction) and attr is not Reaction:
                    instance = attr()
                    self.reactions[instance.name] = instance

    def check(
        self, action_name: str, session: Session, area_action: AreaAction, user_id: int
    ) -> Optional[Action]:
        """Search for an action by name and execute check with parameters."""
        action = self.actions.get(action_name)
        if action:
            action.check(session, area_action, user_id)
            return action
        logger.error(f"Action '{action_name}' not found in {self.name}")
        return None

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
            "aouth_required": self.oauth,
        }

    def is_connected(self, session: Session) -> bool:
        return False

    def oauth_link(self) -> str:
        return ""

    def oauth_callback(self, session: Session, code: str, user: User) -> Response:
        pass


class oauth_service:
    def __init__(self, color: str = "#000000", img_url: str = "") -> None:
        self.name: str = self.__class__.__name__
        self.color: str = color
        self.image_url: str = img_url

    def oauth_link(self) -> str:
        return ""

    def oauth_callback(
        self, session: Session, code: str, user: User | None
    ) -> Response:
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
    """Get all available Services and put them in a dictionary with [key=name, value=service instance]."""
    service_dict = {}

    def get_all_subclasses(cls):
        all_subclasses = []
        for subclass in cls.__subclasses__():
            all_subclasses.append(subclass)
            all_subclasses.extend(get_all_subclasses(subclass))
        return all_subclasses

    for service_class in get_all_subclasses(service_type):
        instance = service_class()
        service_dict[instance.name] = instance

    return service_dict
