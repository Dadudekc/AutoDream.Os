#!/usr/bin/env python3
"""
Service Layer Architecture
==========================

Service layer implementation with proper separation of concerns.
Implements service patterns for the growing Agent Cellphone V2 project.

V2 Compliance: < 400 lines, single responsibility
Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

import threading
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any

from ..core.shared_logging import get_module_logger
from .design_patterns_v2 import ServiceLocator

logger = get_module_logger(__name__)


class ServiceStatus(Enum):
    """Service status enumeration."""

    INITIALIZING = "initializing"
    RUNNING = "running"
    STOPPED = "stopped"
    ERROR = "error"


@dataclass
class ServiceConfig:
    """Service configuration."""

    name: str
    dependencies: list[str] = None
    auto_start: bool = True
    retry_count: int = 3
    timeout: int = 30

    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []


class ServiceBase(ABC):
    """Base service class with common functionality."""

    def __init__(self, config: ServiceConfig):
        self.config = config
        self.status = ServiceStatus.INITIALIZING
        self.dependencies: dict[str, Any] = {}
        self._lock = threading.Lock()
        self._start_time: datetime | None = None
        self._error_count = 0

    @abstractmethod
    def initialize(self) -> bool:
        """Initialize service."""
        pass

    @abstractmethod
    def start(self) -> bool:
        """Start service."""
        pass

    @abstractmethod
    def stop(self) -> bool:
        """Stop service."""
        pass

    @abstractmethod
    def health_check(self) -> bool:
        """Check service health."""
        pass

    def get_status(self) -> dict[str, Any]:
        """Get service status."""
        with self._lock:
            return {
                "name": self.config.name,
                "status": self.status.value,
                "start_time": self._start_time.isoformat() if self._start_time else None,
                "error_count": self._error_count,
                "dependencies": list(self.dependencies.keys()),
            }

    def _resolve_dependencies(self) -> bool:
        """Resolve service dependencies."""
        try:
            for dep_name in self.config.dependencies:
                if not ServiceLocator.is_registered(dep_name):
                    logger.error(f"Dependency not found: {dep_name}")
                    return False
                self.dependencies[dep_name] = ServiceLocator.get(dep_name)
            return True
        except Exception as e:
            logger.error(f"Failed to resolve dependencies: {e}")
            return False


class MessagingService(ServiceBase):
    """Messaging service implementation."""

    def __init__(self, config: ServiceConfig):
        super().__init__(config)
        self.messaging_service = None

    def initialize(self) -> bool:
        """Initialize messaging service."""
        try:
            if not self._resolve_dependencies():
                return False

            # Import and initialize messaging service
            from ...services.consolidated_messaging_service import ConsolidatedMessagingService

            self.messaging_service = ConsolidatedMessagingService()

            self.status = ServiceStatus.RUNNING
            self._start_time = datetime.now()
            logger.info(f"Messaging service initialized: {self.config.name}")
            return True

        except Exception as e:
            logger.error(f"Failed to initialize messaging service: {e}")
            self.status = ServiceStatus.ERROR
            return False

    def start(self) -> bool:
        """Start messaging service."""
        if self.status == ServiceStatus.RUNNING:
            return True

        if not self.initialize():
            return False

        self.status = ServiceStatus.RUNNING
        return True

    def stop(self) -> bool:
        """Stop messaging service."""
        self.status = ServiceStatus.STOPPED
        logger.info(f"Messaging service stopped: {self.config.name}")
        return True

    def health_check(self) -> bool:
        """Check messaging service health."""
        return self.messaging_service is not None and self.status == ServiceStatus.RUNNING

    def send_message(
        self, agent_id: str, message: str, from_agent: str = "Agent-2", priority: str = "NORMAL"
    ) -> bool:
        """Send message through messaging service."""
        if not self.health_check():
            return False

        try:
            return self.messaging_service.send_message(agent_id, message, from_agent, priority)
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            self._error_count += 1
            return False


class DiscordService(ServiceBase):
    """Discord service implementation."""

    def __init__(self, config: ServiceConfig):
        super().__init__(config)
        self.discord_bot = None

    def initialize(self) -> bool:
        """Initialize Discord service."""
        try:
            if not self._resolve_dependencies():
                return False

            # Import and initialize Discord bot
            from ...services.discord_bot.core.discord_bot import EnhancedDiscordAgentBot

            self.discord_bot = EnhancedDiscordAgentBot()

            self.status = ServiceStatus.RUNNING
            self._start_time = datetime.now()
            logger.info(f"Discord service initialized: {self.config.name}")
            return True

        except Exception as e:
            logger.error(f"Failed to initialize Discord service: {e}")
            self.status = ServiceStatus.ERROR
            return False

    def start(self) -> bool:
        """Start Discord service."""
        if self.status == ServiceStatus.RUNNING:
            return True

        if not self.initialize():
            return False

        self.status = ServiceStatus.RUNNING
        return True

    def stop(self) -> bool:
        """Stop Discord service."""
        if self.discord_bot:
            # Stop Discord bot gracefully
            pass

        self.status = ServiceStatus.STOPPED
        logger.info(f"Discord service stopped: {self.config.name}")
        return True

    def health_check(self) -> bool:
        """Check Discord service health."""
        return self.discord_bot is not None and self.status == ServiceStatus.RUNNING


class TheaService(ServiceBase):
    """Thea communication service implementation."""

    def __init__(self, config: ServiceConfig):
        super().__init__(config)
        self.thea_interface = None

    def initialize(self) -> bool:
        """Initialize Thea service."""
        try:
            if not self._resolve_dependencies():
                return False

            # Import and initialize Thea interface
            from ...services.thea.thea_communication_interface import TheaCommunicationInterface

            self.thea_interface = TheaCommunicationInterface()

            self.status = ServiceStatus.RUNNING
            self._start_time = datetime.now()
            logger.info(f"Thea service initialized: {self.config.name}")
            return True

        except Exception as e:
            logger.error(f"Failed to initialize Thea service: {e}")
            self.status = ServiceStatus.ERROR
            return False

    def start(self) -> bool:
        """Start Thea service."""
        if self.status == ServiceStatus.RUNNING:
            return True

        if not self.initialize():
            return False

        self.status = ServiceStatus.RUNNING
        return True

    def stop(self) -> bool:
        """Stop Thea service."""
        self.status = ServiceStatus.STOPPED
        logger.info(f"Thea service stopped: {self.config.name}")
        return True

    def health_check(self) -> bool:
        """Check Thea service health."""
        return self.thea_interface is not None and self.status == ServiceStatus.RUNNING


class ServiceManager:
    """Service manager for orchestrating services."""

    def __init__(self):
        self.services: dict[str, ServiceBase] = {}
        self._lock = threading.Lock()

    def register_service(self, service: ServiceBase) -> bool:
        """Register service."""
        with self._lock:
            self.services[service.config.name] = service
            ServiceLocator.register(service.config.name, service)
            logger.info(f"Service registered: {service.config.name}")
            return True

    def start_service(self, service_name: str) -> bool:
        """Start specific service."""
        with self._lock:
            if service_name not in self.services:
                logger.error(f"Service not found: {service_name}")
                return False

            service = self.services[service_name]
            return service.start()

    def stop_service(self, service_name: str) -> bool:
        """Stop specific service."""
        with self._lock:
            if service_name not in self.services:
                logger.error(f"Service not found: {service_name}")
                return False

            service = self.services[service_name]
            return service.stop()

    def start_all_services(self) -> dict[str, bool]:
        """Start all registered services."""
        results = {}
        with self._lock:
            for service_name, service in self.services.items():
                results[service_name] = service.start()
        return results

    def stop_all_services(self) -> dict[str, bool]:
        """Stop all registered services."""
        results = {}
        with self._lock:
            for service_name, service in self.services.items():
                results[service_name] = service.stop()
        return results

    def get_service_status(self, service_name: str) -> dict[str, Any] | None:
        """Get service status."""
        with self._lock:
            if service_name not in self.services:
                return None
            return self.services[service_name].get_status()

    def get_all_status(self) -> dict[str, dict[str, Any]]:
        """Get status of all services."""
        with self._lock:
            return {name: service.get_status() for name, service in self.services.items()}

    def health_check_all(self) -> dict[str, bool]:
        """Health check all services."""
        with self._lock:
            return {name: service.health_check() for name, service in self.services.items()}
