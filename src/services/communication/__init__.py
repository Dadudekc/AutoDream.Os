#!/usr/bin/env python3
"""
Communication Coordinator Package - V2 Standards Compliant
Modular communication coordination system for agent management
"""

from .coordinator_types import (
    CommunicationMode,
    TaskPriority,
    TaskStatus,
    CaptaincyTerm,
    CoordinationTask,
    CoordinationMessage,
    AgentCapability,
    CoordinationSession
)

from .message_coordinator import MessageCoordinator
from .channel_manager import ChannelManager, CommunicationChannel, ProtocolHandler
from .coordinator_cli import CoordinatorCLI

__all__ = [
    # Types and enums
    'CommunicationMode',
    'TaskPriority',
    'TaskStatus',
    'CaptaincyTerm',
    'CoordinationTask',
    'CoordinationMessage',
    'AgentCapability',
    'CoordinationSession',
    
    # Core classes
    'MessageCoordinator',
    'ChannelManager',
    'CommunicationChannel',
    'ProtocolHandler',
    
    # CLI interface
    'CoordinatorCLI'
]

__version__ = "2.0.0"
__author__ = "Agent Cellphone V2 Team"
__description__ = "V2 Standards Compliant Communication Coordinator"
