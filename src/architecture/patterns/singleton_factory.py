#!/usr/bin/env python3
"""
Singleton and Factory Patterns - V2 Compliant
==============================================

Singleton and Factory pattern implementations for the Agent Cellphone V2 project.
Maintains V2 compliance with focused responsibility.

V2 Compliance: < 400 lines, single responsibility
Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

import threading
from typing import Any, TypeVar

from ...core.shared_logging import get_module_logger

logger = get_module_logger(__name__)

T = TypeVar("T")


class SingletonMeta(type):
    """Thread-safe singleton metaclass."""

    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class SingletonBase(metaclass=SingletonMeta):
    """Base class for singleton pattern."""

    pass


class ServiceFactory:
    """Factory for creating service instances."""

    _services: dict[str, Any] = {}
    _lock = threading.Lock()

    @classmethod
    def create_service(cls, service_type: str, *args, **kwargs) -> Any:
        """Create or get service instance."""
        with cls._lock:
            if service_type not in cls._services:
                cls._services[service_type] = cls._create_instance(service_type, *args, **kwargs)
            return cls._services[service_type]

    @classmethod
    def _create_instance(cls, service_type: str, *args, **kwargs) -> Any:
        """Create service instance based on type."""
        service_map = {
            "messaging": "src.services.consolidated_messaging_service.ConsolidatedMessagingService",
            "discord": "src.services.discord_bot.core.discord_bot.EnhancedDiscordAgentBot",
            "thea": "src.services.thea.thea_communication_interface.TheaCommunicationInterface",
            "vector_db": "src.services.vector_database.vector_database_integration.VectorDatabaseIntegration",
        }

        if service_type not in service_map:
            raise ValueError(f"Unknown service type: {service_type}")

        # Dynamic import and instantiation
        module_path, class_name = service_map[service_type].rsplit(".", 1)
        module = __import__(module_path, fromlist=[class_name])
        service_class = getattr(module, class_name)
        return service_class(*args, **kwargs)

    @classmethod
    def register_service_type(cls, service_type: str, module_path: str, class_name: str) -> None:
        """Register new service type."""
        with cls._lock:
            cls._services[f"{module_path}.{class_name}"] = (module_path, class_name)

    @classmethod
    def clear_cache(cls) -> None:
        """Clear service cache."""
        with cls._lock:
            cls._services.clear()


class ServiceLocator:
    """Service locator for dependency injection."""

    _services: dict[str, Any] = {}
    _lock = threading.Lock()

    @classmethod
    def register(cls, service_name: str, service_instance: Any) -> None:
        """Register service."""
        with cls._lock:
            cls._services[service_name] = service_instance
            logger.info(f"Service registered: {service_name}")

    @classmethod
    def get(cls, service_name: str) -> Any:
        """Get service."""
        with cls._lock:
            if service_name not in cls._services:
                raise ValueError(f"Service not found: {service_name}")
            return cls._services[service_name]

    @classmethod
    def is_registered(cls, service_name: str) -> bool:
        """Check if service is registered."""
        with cls._lock:
            return service_name in cls._services

    @classmethod
    def unregister(cls, service_name: str) -> bool:
        """Unregister service."""
        with cls._lock:
            if service_name in cls._services:
                del cls._services[service_name]
                logger.info(f"Service unregistered: {service_name}")
                return True
            return False

    @classmethod
    def list_services(cls) -> list:
        """List registered services."""
        with cls._lock:
            return list(cls._services.keys())

    @classmethod
    def clear_all(cls) -> None:
        """Clear all services."""
        with cls._lock:
            cls._services.clear()
            logger.info("All services cleared")
