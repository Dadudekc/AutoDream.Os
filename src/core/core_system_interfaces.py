#!/usr/bin/env python3
"""
Core System Interfaces - Core System Protocol Definitions
========================================================

Core system interface definitions consolidating fundamental system protocols.
Part of the modularization of unified_core_interfaces.py for V2 compliance.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Protocol


class ICoreSystem(Protocol):
    """Core system interface for all major system components."""

    @property
    def system_name(self) -> str:
        """Return the system name."""
        ...

    @property
    def version(self) -> str:
        """Return the system version."""
        ...

    def initialize(self) -> bool:
        """Initialize the system."""
        ...

    def shutdown(self) -> bool:
        """Shutdown the system."""
        ...

    def get_status(self) -> Dict[str, Any]:
        """Get system status information."""
        ...


class IConfigurable(Protocol):
    """Interface for configurable components."""

    def configure(self, config: Dict[str, Any]) -> bool:
        """Configure the component with provided settings."""
        ...

    def get_config(self) -> Dict[str, Any]:
        """Get current configuration."""
        ...

    def validate_config(self, config: Dict[str, Any]) -> bool:
        """Validate configuration settings."""
        ...


class IObservable(Protocol):
    """Interface for observable components."""

    def add_observer(self, observer: IObserver) -> bool:
        """Add an observer to the component."""
        ...

    def remove_observer(self, observer: IObserver) -> bool:
        """Remove an observer from the component."""
        ...

    def notify_observers(self, event: str, data: Any) -> None:
        """Notify all observers of an event."""
        ...


class IObserver(Protocol):
    """Interface for observer components."""

    def update(self, event: str, data: Any) -> None:
        """Handle updates from observed components."""
        ...


@dataclass
class CoreSystemMetadata:
    """Metadata for core system components."""
    name: str
    version: str
    description: str
    author: str
    created_at: str
    updated_at: str


class IUnifiedCoreSystem(ICoreSystem, IConfigurable, IObservable, ILifecycleAware, IHealthCheck, IMonitor):
    """Unified interface combining all core system capabilities."""
    
    @property
    def metadata(self) -> CoreSystemMetadata:
        """Get system metadata."""
        ...
    
    def get_capabilities(self) -> List[str]:
        """Get list of system capabilities."""
        ...
    
    def is_operational(self) -> bool:
        """Check if system is operational."""
        ...
