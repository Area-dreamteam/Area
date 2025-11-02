"""OAuth state management for all authentication flows."""

import time
from typing import Dict, Optional, Tuple
from threading import Lock
from core.logger import logger

_oauth_states: Dict[str, Tuple[int, float, bool]] = {}
_state_lock = Lock()

STATE_EXPIRY_SECONDS = 600


def store_oauth_state(state: str, user_id: int, is_mobile: bool = False) -> None:
    """Store OAuth state token with associated user ID and platform info."""
    expiry = time.time() + STATE_EXPIRY_SECONDS
    with _state_lock:
        _oauth_states[state] = (user_id, expiry, is_mobile)
        logger.debug(
            f"Stored state: {state} -> user_id={user_id}, is_mobile={is_mobile}, expires_in={STATE_EXPIRY_SECONDS}s, total_states={len(_oauth_states)}"
        )


def get_user_from_state(state: str) -> Optional[Tuple[int, bool]]:
    """Retrieve user ID and mobile flag from OAuth state token and remove it.

    State tokens are single-use and automatically removed after retrieval.
    Expired tokens are also removed and return None.

    Args:
        state: OAuth state token from callback

    Returns:
        Tuple of (user_id, is_mobile) if state is valid and not expired, None otherwise
    """
    with _state_lock:
        logger.debug(
            f"Looking up state: {state}, available_states={list(_oauth_states.keys())}"
        )
        if state not in _oauth_states:
            logger.debug(f"State not found: {state}")
            return None

        user_id, expiry, is_mobile = _oauth_states[state]

        del _oauth_states[state]

        if time.time() > expiry:
            logger.debug(f"State expired: {state}")
            return None

        logger.debug(
            f"State valid: {state} -> user_id={user_id}, is_mobile={is_mobile}"
        )
        return (user_id, is_mobile)


def cleanup_expired_states() -> None:
    """Remove expired state tokens from storage."""
    current_time = time.time()
    with _state_lock:
        expired = []
        for state, (_, expiry, _) in _oauth_states.items():
            if current_time > expiry:
                expired.append(state)
        for state in expired:
            del _oauth_states[state]
