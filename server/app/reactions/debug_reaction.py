from core.logger import logger
from typing import Any


def debug_reaction(fields: Any, service_name: str) -> None:
    logger.debug(f"REACTION SUCCESS: {service_name}")
