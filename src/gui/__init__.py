"""
GUI System - V2 Compliant
========================

Desktop GUI interfaces for agent management and monitoring.
Optional layer over V2's CLI-first design with PyAutoGUI integration.

V2 Compliance: All files ≤400 lines, SOLID principles, comprehensive error handling.

Author: Agent-1 - GUI Specialist
License: MIT
"""

from .app import DreamOSGUI
from .controllers.base import BaseGUIController
from .components.agent_card import AgentCard
from .components.status_panel import StatusPanel
from .styles.themes import DarkTheme, LightTheme

__all__ = [
    "DreamOSGUI",
    "BaseGUIController",
    "AgentCard",
    "StatusPanel",
    "DarkTheme",
    "LightTheme",
]

__version__ = "2.0.0"
__author__ = "Agent-1 - GUI Specialist"

