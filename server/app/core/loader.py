import json


def load_services_catalog():
    path = "./configs/services.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_services_config():
    path = "./configs/services_config.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
