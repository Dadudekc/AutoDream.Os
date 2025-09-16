#!/usr/bin/env python3
"""
Unified Core Interfaces - Basic
===============================

This module contains basic core system interfaces including core system,
configuration, coordination, and communication interfaces.

Author: Agent-2 (Architecture & Design Specialist)
Mission: Modularize unified_core_interfaces.py for V2 compliance
License: MIT
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Protocol, Union

# ============================================================================
# CORE SYSTEM INTERFACES
# ============================================================================


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

    def shutdown(self) -> None:
        """Shutdown the system."""
        ...

    def get_status(self) -> dict[str, Any]:
        """Get system status."""
        ...


class IConfigurable(Protocol):
    """Interface for configurable components."""

    def configure(self, config: dict[str, Any]) -> bool:
        """Configure the component."""
        ...

    def get_configuration(self) -> dict[str, Any]:
        """Get current configuration."""
        ...

    def validate_configuration(self, config: dict[str, Any]) -> list[str]:
        """Validate configuration, return list of errors."""
        ...


class IObservable(Protocol):
    """Interface for observable components (Observer pattern)."""

    def add_observer(self, observer: IObserver) -> None:
        """Add an observer."""
        ...

    def remove_observer(self, observer: IObserver) -> None:
        """Remove an observer."""
        ...

    def notify_observers(self, event: str, data: Any = None) -> None:
        """Notify all observers of an event."""
        ...


class IObserver(Protocol):
    """Interface for observer components."""

    def on_event(self, event: str, data: Any = None) -> None:
        """Handle observed event."""
        ...


# ============================================================================
# CONFIGURATION INTERFACES
# ============================================================================


class IConfigurationProvider(Protocol):
    """Interface for configuration providers."""

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        ...

    def set(self, key: str, value: Any) -> None:
        """Set configuration value."""
        ...

    def has(self, key: str) -> bool:
        """Check if configuration key exists."""
        ...

    def get_section(self, section: str) -> dict[str, Any]:
        """Get configuration section."""
        ...

    def reload(self) -> bool:
        """Reload configuration."""
        ...


class IConfigurationValidator(Protocol):
    """Interface for configuration validators."""

    def validate(self, config: dict[str, Any]) -> list[str]:
        """Validate configuration, return validation errors."""
        ...

    def get_schema(self) -> dict[str, Any]:
        """Get validation schema."""
        ...


# ============================================================================
# COORDINATION INTERFACES
# ============================================================================


class ICoordinator(ABC):
    """Abstract base class for all coordinators."""

    @property
    def coordinator_id(self) -> str:
        """Get coordinator ID."""
        ...

    @abstractmethod
    def get_coordinator_type(self) -> str:
        """Return the type of this coordinator."""
        ...

    @abstractmethod
    async def coordinate(self, **kwargs) -> Any:
        """Execute coordination logic."""
        ...


class ICoordinatorRegistry(Protocol):
    """Interface for coordinator registries."""

    def register_coordinator(self, coordinator: ICoordinator) -> None:
        """Register a coordinator."""
        ...

    def get_coordinator(self, coordinator_id: str) -> ICoordinator | None:
        """Get coordinator by ID."""
        ...

    def unregister_coordinator(self, coordinator_id: str) -> bool:
        """Unregister coordinator."""
        ...

    def list_coordinators(self, coordinator_type: str | None = None) -> list[ICoordinator]:
        """List coordinators."""
        ...


class ICoordinatorFactory(Protocol):
    """Interface for coordinator factories."""

    def create_coordinator(self, coordinator_type: str, **kwargs) -> ICoordinator:
        """Create a coordinator instance."""
        ...


# ============================================================================
# COMMUNICATION INTERFACES
# ============================================================================


class IMessageHandler(Protocol):
    """Interface for message handlers."""

    def can_handle(self, message: Any) -> bool:
        """Check if handler can process message."""
        ...

    async def handle_message(self, message: Any) -> Any:
        """Handle message."""
        ...


class ICommunicationChannel(ABC):
    """Abstract base class for communication channels."""

    @property
    def channel_id(self) -> str:
        """Get channel ID."""
        ...

    @abstractmethod
    def get_protocol(self) -> str:
        """Return the protocol this channel supports."""
        ...

    @abstractmethod
    async def send_message(self, message: Any) -> Any:
        """Send a message through this channel."""
        ...

    @abstractmethod
    async def receive_messages(self, recipient: str) -> list[Any]:
        """Receive messages for a recipient."""
        ...


class ICommunicationSystem(Protocol):
    """Interface for communication systems."""

    def register_channel(self, channel: ICommunicationChannel) -> None:
        """Register communication channel."""
        ...

    def register_handler(self, handler: IMessageHandler) -> None:
        """Register message handler."""
        ...

    async def send_message(self, message: Any, channel_id: str = None) -> Any:
        """Send message."""
        ...

    async def broadcast_message(self, message: Any, channel_ids: list[str] = None) -> list[Any]:
        """Broadcast message."""
        ...

    async def receive_messages(self, recipient: str, channel_ids: list[str] = None) -> list[Any]:
        """Receive messages."""
        ...


# ============================================================================
# TYPE HINTS AND ALIASES
# ============================================================================

CoreSystemType = Union[
    ICoreSystem,
    IConfigurable,
    IObservable,
]

CommunicationType = Union[ICommunicationChannel, ICommunicationSystem, IMessageHandler]

CoordinationType = Union[ICoordinator, ICoordinatorRegistry, ICoordinatorFactory]

# Export all interfaces
__all__ = [
    # Core system interfaces
    "ICoreSystem",
    "IConfigurable",
    "IObservable",
    "IObserver",
    # Configuration interfaces
    "IConfigurationProvider",
    "IConfigurationValidator",
    # Coordination interfaces
    "ICoordinator",
    "ICoordinatorRegistry",
    "ICoordinatorFactory",
    # Communication interfaces
    "IMessageHandler",
    "ICommunicationChannel",
    "ICommunicationSystem",
    # Types
    "CoreSystemType",
    "CommunicationType",
    "CoordinationType",
]


if __name__ == "__main__":
    """Demonstrate module functionality with practical examples."""
    print("🐝 Unified Core Interfaces - Basic Module")
    print("=" * 50)
    print("✅ Basic core system interfaces loaded successfully")
    print("✅ Configuration interfaces loaded successfully")
    print("✅ Coordination interfaces loaded successfully")
    print("✅ Communication interfaces loaded successfully")
    print("🐝 WE ARE SWARM - Basic interfaces ready!")
