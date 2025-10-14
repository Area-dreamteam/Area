from typing import Dict
from services.services_classes import Service, create_service_dictionnary, oauth_service
from services.google import Google
from services.todoist import Todoist
from services.github import github_oauth

services_dico: Dict[str, Service] = create_service_dictionnary(Service)

services_oauth: Dict[str, Service] = create_service_dictionnary(oauth_service)


def get_json_services():
    json_services = {}
    for service_name, service in services_dico.items():
        json_services[service_name] = service.to_dict()
    return json_services


def get_json_services_login():
    json_services = {}
    for service_name, service in services_oauth.items():
        json_services[service_name] = service.to_dict()
    return json_services
