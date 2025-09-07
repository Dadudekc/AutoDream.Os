"""Backward-compatible wrapper for the new service coordinator."""

from __future__ import annotations

from .core_service_coordinator import CoreServiceCoordinator


class CoreServiceManager(CoreServiceCoordinator):
    """Maintains historical import path for service manager."""

    pass
