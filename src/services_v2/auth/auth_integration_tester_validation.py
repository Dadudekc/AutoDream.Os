"""Validation utilities for auth integration tests."""
from typing import Tuple


def validate_environment() -> Tuple[bool, str]:
    """Ensure core services required for testing are operational."""
    try:
        from .auth_service import AuthService  # local import to avoid heavy load
    except Exception as exc:  # pragma: no cover - import check
        return False, f"AuthService import failed: {exc}"

    try:
        service = AuthService()
        service.get_security_status()
    except Exception as exc:
        return False, f"AuthService not operational: {exc}"

    return True, "environment ready"
