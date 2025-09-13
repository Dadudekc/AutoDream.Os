"""
Thea Services - V2 Compliant Thea Integration System
====================================================

Modular, clean, and scalable Thea communication system following V2_SWARM standards.

Architecture:
- config/: Configuration management
- authentication/: Login and cookie management
- browser/: Browser automation and control
- messaging/: Message sending and receiving
- responses/: Response detection and capture
- core/: Main orchestration service

Author: Agent-4 (Captain) - V2_SWARM
License: MIT
"""

from .config.thea_config import TheaConfig, get_thea_config
from .core.thea_communication_manager import TheaCommunicationManager
from .commander.thea_commander_manager import CommanderTheaManager

__version__ = "2.1.0"
__all__ = [
    "TheaCommunicationManager",
    "CommanderTheaManager",
    "TheaConfig",
    "get_thea_config"
]
