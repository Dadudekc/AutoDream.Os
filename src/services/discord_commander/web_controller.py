"""
Discord Commander Web Controller
V2 Compliant web controller interface
"""

from .web_controller_main import DiscordCommanderController
from .web_controller_models import WebControllerConfig, AgentStatus, MessageData, SystemHealth

__all__ = [
    'DiscordCommanderController',
    'WebControllerConfig', 
    'AgentStatus',
    'MessageData',
    'SystemHealth'
]
