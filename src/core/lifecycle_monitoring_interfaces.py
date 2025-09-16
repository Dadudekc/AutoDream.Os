#!/usr/bin/env python3
"""
Lifecycle and Monitoring Interfaces - Lifecycle and Monitoring Protocol Definitions
=================================================================================

Lifecycle and monitoring interface definitions for system components.
Part of the modularization of unified_core_interfaces.py for V2 compliance.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

from __future__ import annotations

from typing import Any, Protocol


class ILifecycleAware(Protocol):
    """Interface for components with lifecycle management."""

    def start(self) -> bool:
        """Start the component."""
        ...

    def stop(self) -> bool:
        """Stop the component."""
        ...

    def pause(self) -> bool:
        """Pause the component."""
        ...

    def resume(self) -> bool:
        """Resume the component."""
        ...

    def restart(self) -> bool:
        """Restart the component."""
        ...

    @property
    def is_running(self) -> bool:
        """Check if component is running."""
        ...


class IInitializable(Protocol):
    """Interface for components that can be initialized."""

    def initialize(self) -> bool:
        """Initialize the component."""
        ...

    def is_initialized(self) -> bool:
        """Check if component is initialized."""
        ...


class IDisposable(Protocol):
    """Interface for components that can be disposed."""

    def dispose(self) -> bool:
        """Dispose of the component and release resources."""
        ...

    def is_disposed(self) -> bool:
        """Check if component is disposed."""
        ...


class IMonitor(Protocol):
    """Interface for monitoring components."""

    def start_monitoring(self) -> bool:
        """Start monitoring."""
        ...

    def stop_monitoring(self) -> bool:
        """Stop monitoring."""
        ...

    def get_metrics(self) -> dict[str, Any]:
        """Get monitoring metrics."""
        ...

    def is_monitoring(self) -> bool:
        """Check if monitoring is active."""
        ...


class IHealthCheck(Protocol):
    """Interface for health check capabilities."""

    def health_check(self) -> dict[str, Any]:
        """Perform health check and return status."""
        ...

    def is_healthy(self) -> bool:
        """Check if component is healthy."""
        ...

    def get_health_status(self) -> str:
        """Get health status as string."""
        ...

