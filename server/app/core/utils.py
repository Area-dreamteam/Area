import uuid



def generate_state() -> str:
    """Generate unique state for OAuth flows."""
    return str(uuid.uuid4())
