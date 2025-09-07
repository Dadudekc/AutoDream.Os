"""
Gaming & Entertainment Module

This module provides comprehensive gaming and entertainment functionality
for the Agent Cellphone V2 system, including alert management, integration
core, and test running capabilities.

Author: Agent-6 - Gaming & Entertainment Specialist
"""

try:
    from .gaming_alert_manager import GamingAlertManager
except Exception:  # pragma: no cover - degraded environment
    GamingAlertManager = None

from .integration.core import GamingIntegrationCore

try:
    from .gaming_test_runner import GamingTestRunner
except Exception:  # pragma: no cover - degraded environment
    GamingTestRunner = None

__version__ = "1.0.0"
__author__ = "Agent-6 - Gaming & Entertainment Specialist"

__all__ = [
    "GamingAlertManager",
    "GamingIntegrationCore", 
    "GamingTestRunner"
]
