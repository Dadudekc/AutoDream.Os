"""Helpers for mutating status information."""

from __future__ import annotations

import logging
from typing import Dict, Optional, Any

from .health_monitor import HealthMonitor
from .status_registry import StatusRegistry
from .status_types import HealthStatus, StatusLevel

logger = logging.getLogger(__name__)


class StatusUpdater:
    """Provide write operations for status management."""

    def __init__(self, registry: StatusRegistry, health_monitor: HealthMonitor):
        self._registry = registry
        self._health_monitor = health_monitor

    def add_status(
        self,
        component: str,
        status: str,
        level: StatusLevel,
        message: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Add a new status item."""
        status_id = self._registry.add_status(
            component, status, level, message, metadata
        )
        logger.info(f"Added status for {component}: {status} ({level.value})")
        return status_id

    def resolve_status(
        self, status_id: str, resolution_message: str = "Resolved"
    ) -> bool:
        """Mark a status item as resolved."""
        resolved = self._registry.resolve_status(status_id, resolution_message)
        if resolved:
            logger.info(f"Resolved status: {status_id}")
        else:
            logger.warning(f"Status not found: {status_id}")
        return resolved

    def run_health_checks(self) -> Dict[str, HealthStatus]:
        """Run all registered health checks."""
        results = self._health_monitor.run_checks()
        logger.info(f"Completed {len(results)} health checks")
        return results


__all__ = ["StatusUpdater"]
