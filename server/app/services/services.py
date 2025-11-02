"""Service registry and catalog management.

Centralized service discovery and JSON serialization for all available services.
Used by the database initialization process and API endpoints.
"""

from typing import Dict
from services.services_classes import Service, create_service_dictionnary, oauth_service

from services.clash_royale import ClashRoyale
from services.date_and_time import DateAndTime
from services.discord import Discord
from services.email import Email
from services.github import Github
from services.ign import IGN
from services.google import Gmail
from services.microsoft import Outlook
from services.open_meteo import OpenMeteo
from services.podcast import Podcast
from services.reddit import Reddit
from services.spotify import Spotify
from services.strava import Strava
from services.todoist import Todoist
from services.twitch import Twitch
from services.google_calendar import GoogleCalendar
from services.trakt import Trakt
from services.youtube import Youtube
from services.dropbox import Dropbox
from services.notion import Notion
from services.linkedin import LinkedIn
from services.figma import Figma
from services.calendly import Calendly

__all__ = [
    "ClashRoyale",
    "DateAndTime",
    "Discord",
    "Email",
    "Github",
    "IGN",
    "Gmail",
    "Outlook",
    "OpenMeteo",
    "Podcast",
    "Reddit",
    "Spotify",
    "Strava",
    "Todoist",
    "Twitch",
    "GoogleCalendar",
    "Trakt",
    "Youtube",
    "LinkedIn",
    "Dropbox",
    "Notion",
    "Figma",
    "Calendly"
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
