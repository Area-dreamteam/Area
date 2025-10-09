from typing import Callable, Dict, Any
from dependencies.db import SessionDep

from reactions.debug_reaction import debug_reaction
from reactions.create_task import create_task

reaction_list: Dict[str, Callable[[SessionDep, int, list], None]] = {
    "Debug_reaction": debug_reaction,
    "create_task": create_task
}
