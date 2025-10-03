"""
Agent Directory Module - V2 Compliant
=====================================

Centralized agent directory management for V2_SWARM system.
Provides agent discovery, registration, health monitoring, and status tracking.

Components:
- AgentDirectoryManager: Agent discovery and registration
- AgentRegistry: Central agent registry and capability mapping
- AgentHealthMonitor: Health monitoring and alerting

Author: Agent-4 (Captain)
License: MIT
"""

from .agent_directory_manager import AgentDirectoryManager, AgentInfo
from .agent_registry import AgentRegistry, AgentCapability, AgentRole
from .agent_health_monitor import AgentHealthMonitor, HealthCheck

__all__ = [
    "AgentDirectoryManager",
    "AgentInfo", 
    "AgentRegistry",
    "AgentCapability",
    "AgentRole",
    "AgentHealthMonitor",
    "HealthCheck"
]
