"""
Messaging Protocol Routers - V2 Compliant Modular Architecture
=============================================================

Modular router system for messaging protocol optimization.
Each module handles a specific aspect of routing.

V2 Compliance: < 300 lines per module, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

from .messaging_protocol_router import MessagingProtocolRouter
from .route_analyzer import RouteAnalyzer
from .route_cache import RouteCache

__all__ = [
    'MessagingProtocolRouter',
    'RouteAnalyzer',
    'RouteCache'
]
