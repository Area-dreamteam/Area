"""OAuth state management for all authentication flows.

Provides in-memory storage for OAuth state tokens that map to user IDs.
State tokens are used to maintain user context during OAuth callbacks
for all platforms (web, mobile, etc.) as a secure alternative to relying
solely on cookies.
"""

import time
from typing import Dict, Optional, Tuple
from threading import Lock
from core.logger import logger

# In-memory state storage: state_token -> (user_id, expiry_timestamp)
_oauth_states: Dict[str, Tuple[int, float]] = {}
_state_lock = Lock()

# State tokens expire after 10 minutes
STATE_EXPIRY_SECONDS = 600


def store_oauth_state(state: str, user_id: int) -> None:
    """Store OAuth state token with associated user ID for all platforms.

    Args:
        state: Unique state token generated for the OAuth flow
        user_id: ID of the authenticated user initiating the OAuth flow
    """
    expiry = time.time() + STATE_EXPIRY_SECONDS
    with _state_lock:
        _oauth_states[state] = (user_id, expiry)
        logger.debug(
            f"Stored state: {state} -> user_id={user_id}, expires_in={STATE_EXPIRY_SECONDS}s, total_states={len(_oauth_states)}"
        )


def get_user_from_state(state: str) -> Optional[int]:
    """Retrieve user ID from OAuth state token and remove it.

    State tokens are single-use and automatically removed after retrieval.
    Expired tokens are also removed and return None.

    Args:
        state: OAuth state token from callback

    Returns:
        User ID if state is valid and not expired, None otherwise
    """
    with _state_lock:
        logger.debug(
            f"Looking up state: {state}, available_states={list(_oauth_states.keys())}"
        )
        if state not in _oauth_states:
            logger.debug(f"State not found: {state}")
            return None

        user_id, expiry = _oauth_states[state]

        # Remove the state (single-use)
        del _oauth_states[state]

        # Check if expired
        if time.time() > expiry:
            logger.debug(f"State expired: {state}")
            return None

        logger.debug(f"State valid: {state} -> user_id={user_id}")
        return user_id


def cleanup_expired_states() -> None:
    """Remove expired state tokens from storage.

    Should be called periodically to prevent memory leaks.
    """
    current_time = time.time()
    with _state_lock:
        expired = [
            state
            for state, (_, expiry) in _oauth_states.items()
            if current_time > expiry
        ]
        for state in expired:
            del _oauth_states[state]
