#!/usr/bin/env python3
"""
Repository Layer Architecture
=============================

Repository pattern implementation for data access layer.
Provides clean separation between business logic and data persistence.

V2 Compliance: < 400 lines, single responsibility
Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

import logging
import json
from typing import Any, Dict, List, Optional, Type, TypeVar, Generic
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from pathlib import Path
import threading
from datetime import datetime

from ..core.shared_logging import get_module_logger
from .design_patterns_v2 import Repository, InMemoryRepository

logger = get_module_logger(__name__)

T = TypeVar('T')


@dataclass
class Entity:
    """Base entity class."""
    id: str
    created_at: datetime = None
    updated_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()


@dataclass
class AgentEntity(Entity):
    """Agent entity."""
    name: str
    status: str = "active"
    last_seen: Optional[datetime] = None
    capabilities: List[str] = None
    
    def __post_init__(self):
        super().__post_init__()
        if self.capabilities is None:
            self.capabilities = []


@dataclass
class MessageEntity(Entity):
    """Message entity."""
    from_agent: str
    to_agent: str
    content: str
    priority: str = "NORMAL"
    status: str = "sent"
    tags: List[str] = None
    
    def __post_init__(self):
        super().__post_init__()
        if self.tags is None:
            self.tags = []


@dataclass
class TaskEntity(Entity):
    """Task entity."""
    title: str
    description: str
    assigned_agent: str
    status: str = "pending"
    priority: str = "NORMAL"
    due_date: Optional[datetime] = None


class FileRepository(Repository[T]):
    """File-based repository implementation."""
    
    def __init__(self, file_path: Path, entity_type: Type[T]):
        self.file_path = file_path
        self.entity_type = entity_type
        self._entities: Dict[str, T] = {}
        self._lock = threading.Lock()
        self._load_from_file()
    
    def _load_from_file(self) -> None:
        """Load entities from file."""
        try:
            if self.file_path.exists():
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for entity_data in data:
                        entity = self._dict_to_entity(entity_data)
                        self._entities[entity.id] = entity
                logger.info(f"Loaded {len(self._entities)} entities from {self.file_path}")
        except Exception as e:
            logger.error(f"Failed to load entities from file: {e}")
    
    def _save_to_file(self) -> None:
        """Save entities to file."""
        try:
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.file_path, 'w', encoding='utf-8') as f:
                data = [self._entity_to_dict(entity) for entity in self._entities.values()]
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Failed to save entities to file: {e}")
    
    def _entity_to_dict(self, entity: T) -> Dict[str, Any]:
        """Convert entity to dictionary."""
        return asdict(entity)
    
    def _dict_to_entity(self, data: Dict[str, Any]) -> T:
        """Convert dictionary to entity."""
        # Handle datetime fields
        for field in ['created_at', 'updated_at', 'last_seen', 'due_date']:
            if field in data and data[field]:
                data[field] = datetime.fromisoformat(data[field])
        
        return self.entity_type(**data)
    
    def save(self, entity: T) -> T:
        """Save entity."""
        with self._lock:
            entity.updated_at = datetime.now()
            self._entities[entity.id] = entity
            self._save_to_file()
            return entity
    
    def find_by_id(self, entity_id: str) -> Optional[T]:
        """Find entity by ID."""
        with self._lock:
            return self._entities.get(entity_id)
    
    def find_all(self) -> List[T]:
        """Find all entities."""
        with self._lock:
            return list(self._entities.values())
    
    def delete(self, entity_id: str) -> bool:
        """Delete entity."""
        with self._lock:
            if entity_id in self._entities:
                del self._entities[entity_id]
                self._save_to_file()
                return True
            return False
    
    def find_by_field(self, field_name: str, value: Any) -> List[T]:
        """Find entities by field value."""
        with self._lock:
            results = []
            for entity in self._entities.values():
                if hasattr(entity, field_name) and getattr(entity, field_name) == value:
                    results.append(entity)
            return results
    
    def count(self) -> int:
        """Get entity count."""
        with self._lock:
            return len(self._entities)


class AgentRepository(FileRepository[AgentEntity]):
    """Agent repository implementation."""
    
    def __init__(self, file_path: Path = Path("data/agents.json")):
        super().__init__(file_path, AgentEntity)
    
    def find_by_name(self, name: str) -> Optional[AgentEntity]:
        """Find agent by name."""
        agents = self.find_by_field("name", name)
        return agents[0] if agents else None
    
    def find_active_agents(self) -> List[AgentEntity]:
        """Find all active agents."""
        return self.find_by_field("status", "active")
    
    def update_last_seen(self, agent_id: str) -> bool:
        """Update agent last seen timestamp."""
        agent = self.find_by_id(agent_id)
        if agent:
            agent.last_seen = datetime.now()
            self.save(agent)
            return True
        return False


class MessageRepository(FileRepository[MessageEntity]):
    """Message repository implementation."""
    
    def __init__(self, file_path: Path = Path("data/messages.json")):
        super().__init__(file_path, MessageEntity)
    
    def find_by_agent(self, agent_id: str) -> List[MessageEntity]:
        """Find messages by agent (sent or received)."""
        sent_messages = self.find_by_field("from_agent", agent_id)
        received_messages = self.find_by_field("to_agent", agent_id)
        return sent_messages + received_messages
    
    def find_by_priority(self, priority: str) -> List[MessageEntity]:
        """Find messages by priority."""
        return self.find_by_field("priority", priority)
    
    def find_recent_messages(self, hours: int = 24) -> List[MessageEntity]:
        """Find recent messages within specified hours."""
        cutoff_time = datetime.now().timestamp() - (hours * 3600)
        with self._lock:
            recent_messages = []
            for message in self._entities.values():
                if message.created_at.timestamp() > cutoff_time:
                    recent_messages.append(message)
            return recent_messages


class TaskRepository(FileRepository[TaskEntity]):
    """Task repository implementation."""
    
    def __init__(self, file_path: Path = Path("data/tasks.json")):
        super().__init__(file_path, TaskEntity)
    
    def find_by_agent(self, agent_id: str) -> List[TaskEntity]:
        """Find tasks assigned to agent."""
        return self.find_by_field("assigned_agent", agent_id)
    
    def find_by_status(self, status: str) -> List[TaskEntity]:
        """Find tasks by status."""
        return self.find_by_field("status", status)
    
    def find_overdue_tasks(self) -> List[TaskEntity]:
        """Find overdue tasks."""
        now = datetime.now()
        with self._lock:
            overdue_tasks = []
            for task in self._entities.values():
                if task.due_date and task.due_date < now and task.status != "completed":
                    overdue_tasks.append(task)
            return overdue_tasks


class RepositoryManager:
    """Repository manager for coordinating repositories."""
    
    def __init__(self):
        self.repositories: Dict[str, Repository] = {}
        self._lock = threading.Lock()
    
    def register_repository(self, name: str, repository: Repository) -> None:
        """Register repository."""
        with self._lock:
            self.repositories[name] = repository
            logger.info(f"Repository registered: {name}")
    
    def get_repository(self, name: str) -> Optional[Repository]:
        """Get repository by name."""
        with self._lock:
            return self.repositories.get(name)
    
    def get_agent_repository(self) -> AgentRepository:
        """Get agent repository."""
        if "agents" not in self.repositories:
            self.register_repository("agents", AgentRepository())
        return self.repositories["agents"]
    
    def get_message_repository(self) -> MessageRepository:
        """Get message repository."""
        if "messages" not in self.repositories:
            self.register_repository("messages", MessageRepository())
        return self.repositories["messages"]
    
    def get_task_repository(self) -> TaskRepository:
        """Get task repository."""
        if "tasks" not in self.repositories:
            self.register_repository("tasks", TaskRepository())
        return self.repositories["tasks"]
    
    def get_all_repositories(self) -> Dict[str, Repository]:
        """Get all repositories."""
        with self._lock:
            return self.repositories.copy()
