"""
Emergency Protocol Handlers Package
===================================

Modular handlers for emergency protocol operations.
Extracted from protocols.py for V2 compliance.

Author: Agent-8 (SSOT & System Integration Specialist)
License: MIT
"""

from .protocol_registry import ProtocolRegistry
from .protocol_initializer import ProtocolInitializer
from .protocol_executor import ProtocolExecutor

__all__ = [
    'ProtocolRegistry',
    'ProtocolInitializer',
    'ProtocolExecutor'
]
