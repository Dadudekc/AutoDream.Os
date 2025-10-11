"""
ChatGPT Integration - V2 Compliant
==================================

Browser automation for ChatGPT interaction and conversation extraction.
Extends V2's existing browser infrastructure with ChatGPT-specific capabilities.

V2 Compliance: All files ≤400 lines, SOLID principles, comprehensive error handling.

Author: Agent-1 - Browser Automation Specialist
License: MIT
"""

from .navigator import ChatGPTNavigator
from .session import BrowserSessionManager
from .extractor import ConversationExtractor

__all__ = [
    'ChatGPTNavigator',
    'BrowserSessionManager',
    'ConversationExtractor',
]

__version__ = "2.0.0"
__author__ = "Agent-1 - Browser Automation Specialist"
