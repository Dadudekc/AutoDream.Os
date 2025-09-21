#!/usr/bin/env python3
"""
Application Layer Architecture
==============================

Application layer implementation with business logic and use cases.
Implements clean architecture principles for the Agent Cellphone V2 project.

V2 Compliance: < 400 lines, single responsibility
Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

import logging
from typing import Any, Dict, List, Optional, Callable
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
import threading
from datetime import datetime

from ..core.shared_logging import get_module_logger
from .design_patterns_v2 import ServiceLocator, Command, CommandInvoker
from .repository_layer import RepositoryManager, AgentEntity, MessageEntity, TaskEntity
from .service_layer import ServiceManager

logger = get_module_logger(__name__)


class UseCaseResult:
    """Use case result wrapper."""
    
    def __init__(self, success: bool, data: Any = None, error: str = None):
        self.success = success
        self.data = data
        self.error = error
        self.timestamp = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "success": self.success,
            "data": self.data,
            "error": self.error,
            "timestamp": self.timestamp.isoformat()
        }


class UseCase(ABC):
    """Base use case interface."""
    
    @abstractmethod
    def execute(self, *args, **kwargs) -> UseCaseResult:
        """Execute use case."""
        pass


class SendMessageUseCase(UseCase):
    """Send message use case."""
    
    def __init__(self):
        self.repository_manager = RepositoryManager()
        self.service_manager = ServiceManager()
    
    def execute(self, from_agent: str, to_agent: str, message: str, priority: str = "NORMAL") -> UseCaseResult:
        """Execute send message use case."""
        try:
            # Validate inputs
            if not from_agent or not to_agent or not message:
                return UseCaseResult(False, error="Invalid input parameters")
            
            # Create message entity
            message_entity = MessageEntity(
                id=f"msg_{datetime.now().timestamp()}",
                from_agent=from_agent,
                to_agent=to_agent,
                content=message,
                priority=priority
            )
            
            # Save to repository
            message_repo = self.repository_manager.get_message_repository()
            saved_message = message_repo.save(message_entity)
            
            # Send through messaging service
            messaging_service = ServiceLocator.get("messaging")
            send_success = messaging_service.send_message(to_agent, message, from_agent, priority)
            
            if send_success:
                # Update message status
                saved_message.status = "sent"
                message_repo.save(saved_message)
                
                return UseCaseResult(True, data=saved_message)
            else:
                # Update message status
                saved_message.status = "failed"
                message_repo.save(saved_message)
                
                return UseCaseResult(False, error="Failed to send message")
                
        except Exception as e:
            logger.error(f"Send message use case failed: {e}")
            return UseCaseResult(False, error=str(e))


class GetAgentStatusUseCase(UseCase):
    """Get agent status use case."""
    
    def __init__(self):
        self.repository_manager = RepositoryManager()
    
    def execute(self, agent_id: str) -> UseCaseResult:
        """Execute get agent status use case."""
        try:
            agent_repo = self.repository_manager.get_agent_repository()
            agent = agent_repo.find_by_id(agent_id)
            
            if not agent:
                return UseCaseResult(False, error="Agent not found")
            
            # Update last seen
            agent_repo.update_last_seen(agent_id)
            
            return UseCaseResult(True, data=agent)
            
        except Exception as e:
            logger.error(f"Get agent status use case failed: {e}")
            return UseCaseResult(False, error=str(e))


class CreateTaskUseCase(UseCase):
    """Create task use case."""
    
    def __init__(self):
        self.repository_manager = RepositoryManager()
    
    def execute(self, title: str, description: str, assigned_agent: str, priority: str = "NORMAL", due_date: Optional[datetime] = None) -> UseCaseResult:
        """Execute create task use case."""
        try:
            # Validate inputs
            if not title or not description or not assigned_agent:
                return UseCaseResult(False, error="Invalid input parameters")
            
            # Create task entity
            task_entity = TaskEntity(
                id=f"task_{datetime.now().timestamp()}",
                title=title,
                description=description,
                assigned_agent=assigned_agent,
                priority=priority,
                due_date=due_date
            )
            
            # Save to repository
            task_repo = self.repository_manager.get_task_repository()
            saved_task = task_repo.save(task_entity)
            
            return UseCaseResult(True, data=saved_task)
            
        except Exception as e:
            logger.error(f"Create task use case failed: {e}")
            return UseCaseResult(False, error=str(e))


class GetSystemStatusUseCase(UseCase):
    """Get system status use case."""
    
    def __init__(self):
        self.service_manager = ServiceManager()
        self.repository_manager = RepositoryManager()
    
    def execute(self) -> UseCaseResult:
        """Execute get system status use case."""
        try:
            # Get service statuses
            service_statuses = self.service_manager.get_all_status()
            service_health = self.service_manager.health_check_all()
            
            # Get repository counts
            agent_repo = self.repository_manager.get_agent_repository()
            message_repo = self.repository_manager.get_message_repository()
            task_repo = self.repository_manager.get_task_repository()
            
            system_status = {
                "services": {
                    "statuses": service_statuses,
                    "health": service_health
                },
                "repositories": {
                    "agents": agent_repo.count(),
                    "messages": message_repo.count(),
                    "tasks": task_repo.count()
                },
                "timestamp": datetime.now().isoformat()
            }
            
            return UseCaseResult(True, data=system_status)
            
        except Exception as e:
            logger.error(f"Get system status use case failed: {e}")
            return UseCaseResult(False, error=str(e))


class ApplicationService:
    """Application service orchestrating use cases."""
    
    def __init__(self):
        self.use_cases: Dict[str, UseCase] = {}
        self.command_invoker = CommandInvoker()
        self._lock = threading.Lock()
        self._initialize_use_cases()
    
    def _initialize_use_cases(self) -> None:
        """Initialize use cases."""
        with self._lock:
            self.use_cases = {
                "send_message": SendMessageUseCase(),
                "get_agent_status": GetAgentStatusUseCase(),
                "create_task": CreateTaskUseCase(),
                "get_system_status": GetSystemStatusUseCase()
            }
    
    def execute_use_case(self, use_case_name: str, *args, **kwargs) -> UseCaseResult:
        """Execute use case by name."""
        with self._lock:
            if use_case_name not in self.use_cases:
                return UseCaseResult(False, error=f"Use case not found: {use_case_name}")
            
            use_case = self.use_cases[use_case_name]
            return use_case.execute(*args, **kwargs)
    
    def send_message(self, from_agent: str, to_agent: str, message: str, priority: str = "NORMAL") -> UseCaseResult:
        """Send message through use case."""
        return self.execute_use_case("send_message", from_agent, to_agent, message, priority)
    
    def get_agent_status(self, agent_id: str) -> UseCaseResult:
        """Get agent status through use case."""
        return self.execute_use_case("get_agent_status", agent_id)
    
    def create_task(self, title: str, description: str, assigned_agent: str, priority: str = "NORMAL", due_date: Optional[datetime] = None) -> UseCaseResult:
        """Create task through use case."""
        return self.execute_use_case("create_task", title, description, assigned_agent, priority, due_date)
    
    def get_system_status(self) -> UseCaseResult:
        """Get system status through use case."""
        return self.execute_use_case("get_system_status")
    
    def list_use_cases(self) -> List[str]:
        """List available use cases."""
        with self._lock:
            return list(self.use_cases.keys())


class ApplicationFacade:
    """Application facade providing simplified interface."""
    
    def __init__(self):
        self.application_service = ApplicationService()
        self.service_manager = ServiceManager()
        self.repository_manager = RepositoryManager()
    
    def initialize(self) -> bool:
        """Initialize application facade."""
        try:
            # Register core services
            from .service_layer import MessagingService, DiscordService, TheaService
            from .service_layer import ServiceConfig
            
            messaging_config = ServiceConfig("messaging", auto_start=True)
            discord_config = ServiceConfig("discord", dependencies=["messaging"], auto_start=True)
            thea_config = ServiceConfig("thea", dependencies=["messaging"], auto_start=True)
            
            self.service_manager.register_service(MessagingService(messaging_config))
            self.service_manager.register_service(DiscordService(discord_config))
            self.service_manager.register_service(TheaService(thea_config))
            
            # Start services
            start_results = self.service_manager.start_all_services()
            
            # Register services in service locator
            for service_name, service in self.service_manager.services.items():
                ServiceLocator.register(service_name, service)
            
            logger.info("Application facade initialized successfully")
            return all(start_results.values())
            
        except Exception as e:
            logger.error(f"Failed to initialize application facade: {e}")
            return False
    
    def shutdown(self) -> bool:
        """Shutdown application facade."""
        try:
            stop_results = self.service_manager.stop_all_services()
            logger.info("Application facade shutdown successfully")
            return all(stop_results.values())
        except Exception as e:
            logger.error(f"Failed to shutdown application facade: {e}")
            return False
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get application health status."""
        system_status_result = self.application_service.get_system_status()
        return system_status_result.to_dict() if system_status_result.success else {"error": system_status_result.error}


