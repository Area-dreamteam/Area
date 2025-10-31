"""Service registry and catalog management.

Centralized service discovery and JSON serialization for all available services.
Used by the database initialization process and API endpoints.
"""

from typing import Dict
from services.services_classes import Service, create_service_dictionnary, oauth_service

from services.clash_royale import ClashRoyale
from services.date_and_time import DateAndTime
from services.github import Github
from services.google import Gmail
from services.microsoft import Outlook
from services.open_meteo import OpenMeteo
from services.reddit import Reddit
from services.spotify import Spotify
from services.strava import Strava
from services.todoist import Todoist
from services.twitch import Twitch

__all__ = [
    "ClashRoyale",
    "DateAndTime",
    "Github",
    "Gmail",
    "Outlook",
    "OpenMeteo",
    "Reddit",
    "Spotify",
    "Strava",
    "Todoist",
    "Twitch",
]

# Service registries - automatically populated with all Service/oauth_service subclasses
services_dico: Dict[str, Service] = create_service_dictionnary(Service)
services_oauth: Dict[str, oauth_service] = create_service_dictionnary(oauth_service)


def get_json_services() -> Dict[str, Dict]:
    """Get all automation services as JSON for database sync."""
    json_services = {}
    for service_name, service in services_dico.items():
        json_services[service_name] = service.to_dict()
    return json_services


def get_json_services_login() -> Dict[str, Dict]:
    """Get OAuth login services as JSON for database sync."""
    json_services = {}
    for service_name, service in services_oauth.items():
        json_services[service_name] = service.to_dict()
    return json_services
