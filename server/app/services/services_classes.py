from typing import Dict, Optional, Any
from models.users.user import User
from sqlmodel import Session


class Action:
    def __init__(self, description: str, config: list[Dict[str, Any]] = None) -> None:
        self.name: str = self.__class__.__name__
        self.desc: str = description
        self.config: list[Dict[str, Any]] = config if config is not None else []

    def check(self, params: Dict[str, Any] = None):
        pass

    def to_dict(self) -> Dict[str, Any]:
        """Convert action to dictionary representation."""
        return {"name": self.name, "description": self.desc, "config": self.config}


class Reaction:
    def __init__(self, description: str, config: list[Dict[str, Any]] = None) -> None:
        self.name: str = self.__class__.__name__
        self.desc: str = description
        self.config: list[Dict[str, Any]] = config if config is not None else []

    def execute(self, params: Dict[str, Any] = None):
        pass

    def to_dict(self) -> Dict[str, Any]:
        """Convert reaction to dictionary representation."""
        return {"name": self.name, "description": self.desc, "config": self.config}


class Service:
    def __init__(self, description: str) -> None:
        self.name: str = self.__class__.__name__
        self.desc: str = description
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

    def execute(
        self, action_name: str, params: Dict[str, Any] = None
    ) -> Optional[Action]:
        """Search for an action by name and execute check with parameters."""
        action = self.actions.get(action_name)
        if action:
            action.check(params)
            return action
        print(f"Action '{action_name}' not found in {self.name}")
        return None

    def check(
        self, reaction_name: str, params: Dict[str, Any] = None
    ) -> Optional[Reaction]:
        """Search for a reaction by name and execute it with parameters."""
        reaction = self.reactions.get(reaction_name)
        if reaction:
            reaction.execute(params)
            return reaction
        print(f"Reaction '{reaction_name}' not found in {self.name}")
        return None

    def get_actions_dict(self) -> Dict[str, Dict[str, Any]]:
        """Build a dictionary with all actions and their details."""
        return {name: action.to_dict() for name, action in self.actions.items()}

    def get_reactions_dict(self) -> Dict[str, Dict[str, Any]]:
        """Build a dictionary with all reactions and their details."""
        return {name: reaction.to_dict() for name, reaction in self.reactions.items()}

    def to_dict(self) -> Dict[str, Any]:
        """Convert the entire service to a dictionary representation."""
        return {
            "name": self.name,
            "description": self.desc,
            "actions": self.get_actions_dict(),
            "reactions": self.get_reactions_dict(),
        }

    def is_connected(self, session: Session) -> bool:
        pass

    def oauth_link(self) -> str:
        pass

    def oauth_callback(self, session: Session, code: str, user: User) -> None:
        pass


class oauth_service:
    def oauth_link(self) -> str:
        pass

    def oauth_callback(self, session: Session, code: str, user: User) -> None:
        pass


def create_service_dictionnary() -> Dict[str, Service]:
    """Get all available Services and put them in a dictionary with [key=name, value=service instance]."""
    service_dict = {}

    def get_all_subclasses(cls):
        all_subclasses = []
        for subclass in cls.__subclasses__():
            all_subclasses.append(subclass)
            all_subclasses.extend(get_all_subclasses(subclass))
        return all_subclasses

    for service_class in get_all_subclasses(Service):
        instance = service_class()
        service_dict[instance.name] = instance

    return service_dict
