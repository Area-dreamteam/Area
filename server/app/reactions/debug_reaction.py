from core.logger import logger
from typing import Any
from dependencies.db import SessionDep

def debug_reaction(session: SessionDep, user_id: int, config: list) -> None:
    logger.debug(f"REACTION SUCCESS: {user_id}")
