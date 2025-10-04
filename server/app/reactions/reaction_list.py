from typing import Callable, Dict, List

from reactions import debug_reaction


reaction: List[Dict[str, Callable[[str], None]]] = [
    {"Debug_reaction": debug_reaction},
]
