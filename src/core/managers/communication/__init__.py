#!/usr/bin/env python3
"""
Communication Package - V2 Modular Architecture
==============================================

Modular communication management system following V2 standards.
Follows V2 standards: OOP design, SRP, no strict LOC limits.

Author: Agent-4 (Captain)
Task: TASK 4H - Communication Manager Modularization
License: MIT
"""

# Core communication components
from .communication_core import CommunicationManager
from .channel_manager import ChannelManager
from .message_processor import MessageProcessor
from .api_manager import APIManager
from .websocket_manager import WebSocketManager
from .routing_manager import RoutingManager
from .reporting_manager import ReportingManager

# Emergency restoration and testing capabilities (integrated from communications workspace)
from .emergency_restoration_manager import EmergencyRestorationManager
from .interaction_testing_manager import InteractionTestingManager

# Data models and types
from .models import Channel, ChannelType, APIConfig
from .types import CommunicationTypes

__all__ = [
    # Core components
    'CommunicationManager',
    'ChannelManager',
    'MessageProcessor',
    'APIManager',
    'WebSocketManager',
    'RoutingManager',
    'ReportingManager',
    
    # Data models
    'Channel',
    'ChannelType',
    'APIConfig',
    
    # Types
    'CommunicationTypes'
]

