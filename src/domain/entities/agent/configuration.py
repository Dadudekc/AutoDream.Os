#!/usr/bin/env python3
"""
Agent Configuration - Clean OOP Design
=====================================

Agent configuration following clean object-oriented principles.
Single responsibility: Manage agent configuration settings.

Author: Agent-1 (Integration Specialist)
License: MIT
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from .enums import AgentCapability


@dataclass
class AgentConfiguration:
    """Agent configuration settings."""
    
    # Basic settings
    name: str
    agent_type: str
    capabilities: List[AgentCapability] = field(default_factory=list)
    
    # Performance settings
    max_concurrent_tasks: int = 5
    task_timeout_seconds: int = 300
    retry_attempts: int = 3
    
    # Communication settings
    message_queue_size: int = 100
    heartbeat_interval: int = 30
    response_timeout: int = 60
    
    # Resource limits
    max_memory_mb: int = 512
    max_cpu_percent: int = 80
    max_disk_mb: int = 1024
    
    # Security settings
    require_authentication: bool = True
    allowed_commands: List[str] = field(default_factory=list)
    blocked_commands: List[str] = field(default_factory=list)
    
    # Custom settings
    custom_settings: Dict[str, Any] = field(default_factory=dict)
    
    def add_capability(self, capability: AgentCapability):
        """Add a capability to the agent."""
        if capability not in self.capabilities:
            self.capabilities.append(capability)
    
    def remove_capability(self, capability: AgentCapability):
        """Remove a capability from the agent."""
        if capability in self.capabilities:
            self.capabilities.remove(capability)
    
    def has_capability(self, capability: AgentCapability) -> bool:
        """Check if agent has a specific capability."""
        return capability in self.capabilities
    
    def set_custom_setting(self, key: str, value: Any):
        """Set a custom configuration setting."""
        self.custom_settings[key] = value
    
    def get_custom_setting(self, key: str, default: Any = None) -> Any:
        """Get a custom configuration setting."""
        return self.custom_settings.get(key, default)
    
    def is_command_allowed(self, command: str) -> bool:
        """Check if a command is allowed."""
        if command in self.blocked_commands:
            return False
        if self.allowed_commands and command not in self.allowed_commands:
            return False
        return True
    
    def validate_configuration(self) -> List[str]:
        """Validate configuration and return any errors."""
        errors = []
        
        if not self.name:
            errors.append("Agent name is required")
        
        if self.max_concurrent_tasks <= 0:
            errors.append("Max concurrent tasks must be positive")
        
        if self.task_timeout_seconds <= 0:
            errors.append("Task timeout must be positive")
        
        if self.max_memory_mb <= 0:
            errors.append("Max memory must be positive")
        
        if self.max_cpu_percent <= 0 or self.max_cpu_percent > 100:
            errors.append("Max CPU percent must be between 1 and 100")
        
        return errors
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            'name': self.name,
            'agent_type': self.agent_type,
            'capabilities': [cap.value for cap in self.capabilities],
            'max_concurrent_tasks': self.max_concurrent_tasks,
            'task_timeout_seconds': self.task_timeout_seconds,
            'retry_attempts': self.retry_attempts,
            'message_queue_size': self.message_queue_size,
            'heartbeat_interval': self.heartbeat_interval,
            'response_timeout': self.response_timeout,
            'max_memory_mb': self.max_memory_mb,
            'max_cpu_percent': self.max_cpu_percent,
            'max_disk_mb': self.max_disk_mb,
            'require_authentication': self.require_authentication,
            'allowed_commands': self.allowed_commands,
            'blocked_commands': self.blocked_commands,
            'custom_settings': self.custom_settings
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AgentConfiguration':
        """Create configuration from dictionary."""
        from .enums import AgentCapability
        
        capabilities = [AgentCapability(cap) for cap in data.get('capabilities', [])]
        
        return cls(
            name=data['name'],
            agent_type=data['agent_type'],
            capabilities=capabilities,
            max_concurrent_tasks=data.get('max_concurrent_tasks', 5),
            task_timeout_seconds=data.get('task_timeout_seconds', 300),
            retry_attempts=data.get('retry_attempts', 3),
            message_queue_size=data.get('message_queue_size', 100),
            heartbeat_interval=data.get('heartbeat_interval', 30),
            response_timeout=data.get('response_timeout', 60),
            max_memory_mb=data.get('max_memory_mb', 512),
            max_cpu_percent=data.get('max_cpu_percent', 80),
            max_disk_mb=data.get('max_disk_mb', 1024),
            require_authentication=data.get('require_authentication', True),
            allowed_commands=data.get('allowed_commands', []),
            blocked_commands=data.get('blocked_commands', []),
            custom_settings=data.get('custom_settings', {})
        )