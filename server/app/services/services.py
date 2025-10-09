from typing import Dict
from services.services_classes import Service, create_service_dictionnary
from services.google import Google
from services.todoist import Todoist

services: Dict[str, Service] = create_service_dictionnary()
