"""
Communication Restoration Package - Emergency communication management
==================================================================

This package provides emergency communication restoration capabilities,
breaking down the large monolithic file into focused, maintainable modules.

Modules:
- types: Communication types and enums
- models: Core communication data models
- channels: Communication channel management
- protocols: Coordination protocol management
- monitoring: Monitoring and alerting system
- testing: Interaction testing capabilities
"""

from .types import CommunicationStatus, MessagePriority
from .models import CommunicationChannel, CoordinationProtocol, MonitoringAlert
from .channels import CommunicationChannelManager
from .protocols import CoordinationProtocolManager
from .monitoring import MonitoringSystem
from .testing import InteractionTestingSystem

__all__ = [
    'CommunicationStatus', 'MessagePriority',
    'CommunicationChannel', 'CoordinationProtocol', 'MonitoringAlert',
    'CommunicationChannelManager', 'CoordinationProtocolManager',
    'MonitoringSystem', 'InteractionTestingSystem'
]
