from datetime import datetime
import uuid


def generate_id() -> str:
    """Generate a unique identifier."""
    return uuid.uuid4().hex


def current_timestamp() -> datetime:
    """Return the current UTC timestamp."""
    return datetime.utcnow()
