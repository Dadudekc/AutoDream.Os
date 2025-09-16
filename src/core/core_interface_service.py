#!/usr/bin/env python3
"""
Core Interface Service - Service Layer Implementation
===================================================

Service layer implementation for core system interfaces.
Provides business logic and orchestration for interface operations.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

from __future__ import annotations

import logging
from typing import Any

from .core_interface_factory import CoreInterfaceFactory, InterfaceBuilder
from .core_interface_repository import IInterfaceRepository, InMemoryInterfaceRepository

logger = logging.getLogger(__name__)


class CoreInterfaceService:
    """Service layer for core system interfaces."""

    def __init__(self, repository: IInterfaceRepository | None = None) -> None:
        self._repository = repository or InMemoryInterfaceRepository()
        self._factory = CoreInterfaceFactory()

    def create_interface(self, interface_name: str, interface_id: str, **kwargs) -> Any | None:
        """Create and store a new interface."""
        try:
            # Create interface using factory
            interface = self._factory.create_interface(interface_name, **kwargs)

            # Store in repository
            if self._repository.save_interface(interface_id, interface):
                logger.info(f"Created and stored interface: {interface_name} ({interface_id})")
                return interface
            else:
                logger.error(f"Failed to store interface: {interface_name} ({interface_id})")
                return None

        except Exception as e:
            logger.error(f"Failed to create interface {interface_name}: {e}")
            return None

    def get_interface(self, interface_id: str) -> Any | None:
        """Get an interface by ID."""
        interface = self._repository.get_interface(interface_id)
        if interface:
            logger.debug(f"Retrieved interface: {interface_id}")
        else:
            logger.warning(f"Interface not found: {interface_id}")
        return interface

    def update_interface(self, interface_id: str, **kwargs) -> bool:
        """Update an existing interface."""
        existing_interface = self._repository.get_interface(interface_id)
        if not existing_interface:
            logger.warning(f"Cannot update non-existent interface: {interface_id}")
            return False

        try:
            # Update interface properties
            for key, value in kwargs.items():
                if hasattr(existing_interface, key):
                    setattr(existing_interface, key, value)
                else:
                    logger.warning(f"Property {key} not found on interface {interface_id}")

            # Save updated interface
            if self._repository.save_interface(interface_id, existing_interface):
                logger.info(f"Updated interface: {interface_id}")
                return True
            else:
                logger.error(f"Failed to save updated interface: {interface_id}")
                return False

        except Exception as e:
            logger.error(f"Failed to update interface {interface_id}: {e}")
            return False

    def delete_interface(self, interface_id: str) -> bool:
        """Delete an interface."""
        if self._repository.delete_interface(interface_id):
            logger.info(f"Deleted interface: {interface_id}")
            return True
        else:
            logger.warning(f"Failed to delete interface: {interface_id}")
            return False

    def list_interfaces(self) -> list[str]:
        """List all interface IDs."""
        return self._repository.list_interfaces()

    def get_available_interface_types(self) -> list[str]:
        """Get list of available interface types."""
        return self._factory.get_available_interfaces()

    def create_interface_with_builder(
        self, interface_name: str, interface_id: str, config: dict[str, Any]
    ) -> Any | None:
        """Create interface using builder pattern."""
        try:
            builder = InterfaceBuilder()
            interface = builder.with_config(config).build(interface_name)

            if self._repository.save_interface(interface_id, interface):
                logger.info(f"Created interface with builder: {interface_name} ({interface_id})")
                return interface
            else:
                logger.error(
                    f"Failed to store builder-created interface: {interface_name} ({interface_id})"
                )
                return None

        except Exception as e:
            logger.error(f"Failed to create interface with builder {interface_name}: {e}")
            return None

    def validate_interface(self, interface: Any) -> bool:
        """Validate an interface instance."""
        try:
            # Basic validation - check if interface has required methods
            required_methods = ["system_name", "version"]

            for method_name in required_methods:
                if not hasattr(interface, method_name):
                    logger.warning(f"Interface missing required method: {method_name}")
                    return False

            logger.debug("Interface validation passed")
            return True

        except Exception as e:
            logger.error(f"Interface validation failed: {e}")
            return False

    def get_interface_statistics(self) -> dict[str, Any]:
        """Get statistics about stored interfaces."""
        interface_ids = self._repository.list_interfaces()

        stats = {
            "total_interfaces": len(interface_ids),
            "available_types": len(self._factory.get_available_interfaces()),
            "interface_ids": interface_ids,
        }

        logger.debug(f"Interface statistics: {stats}")
        return stats

