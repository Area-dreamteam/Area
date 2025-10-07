from typing import Callable, Dict, List, Any

from reactions.debug_reaction import debug_reaction


reaction_list: Dict[str, Callable[[Any, str], None]] = {
    "Debug_reaction": debug_reaction
}
