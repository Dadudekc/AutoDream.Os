"""
Messaging Module - Extracted from v2_comprehensive_messaging_system.py

This module contains the extracted messaging functionality organized into focused components:
- router: Message routing logic
- validator: Message validation
- formatter: Message formatting
- storage: Message persistence

Original file: src/core/v2_comprehensive_messaging_system.py
Extraction date: 2024-12-19
"""

from .router import V2MessageRouter
from .validator import V2MessageValidator
from .formatter import V2MessageFormatter
from .storage import V2MessageStorage

__all__ = [
    'V2MessageRouter',
    'V2MessageValidator', 
    'V2MessageFormatter',
    'V2MessageStorage'
]
