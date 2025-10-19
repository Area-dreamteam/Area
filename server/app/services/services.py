"""Service registry and catalog management.

Centralized service discovery and JSON serialization for all available services.
Used by the database initialization process and API endpoints.
"""

from typing import Dict
from services.services_classes import Service, create_service_dictionnary, oauth_service
from services.google import Google
from services.todoist import Todoist
from services.github import github_oauth

# Service registries - automatically populated with all Service/oauth_service subclasses
services_dico: Dict[str, Service] = create_service_dictionnary(Service)
services_oauth: Dict[str, Service] = create_service_dictionnary(oauth_service)


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
